#!/usr/bin/env python3
"""
OpenClaw Memory Pensieve — MCP Server v4.0.0

Single-file MCP server. Replaces all prior scripts.

Configuration via environment variables:
  OPENCLAW_WORKSPACE        Workspace root (default: ~/.openclaw/workspace)
  ALGORAND_WALLET_ADDRESS   Algorand account address
  ALGORAND_WALLET_MNEMONIC  25-word mnemonic  ← keep in env, never log
  ALGORAND_NOTE_KEY_HEX     32-byte AES-GCM key as 64 hex chars
  ALGORAND_ALGOD_URL        Algod endpoint (default: https://mainnet-api.algonode.cloud)
  ALGORAND_ALGOD_TOKEN      Algod token (default: empty)
  ALGORAND_INDEXER_URL      Indexer endpoint (default: https://mainnet-idx.algonode.cloud)
  ALGORAND_INDEXER_TOKEN    Indexer token (default: empty)

Fallback: if the env vars for wallet/key are absent, reads from
  <workspace>/.secrets/algorand-wallet-nox.json  and
  <workspace>/.secrets/algorand-note-key.bin

External dependencies: algosdk, cryptography, mcp
All other operations use the Python stdlib only.

v4 optimizations (vs v2):
  L1 — zlib compression before AES-GCM: 65-80% payload reduction.
  L2 — Events-only anchor: hash fields stripped (recomputable on recovery),
       semantic/procedural/self_model omitted (regeneratable via dream_cycle).
  L3 — Priority ordering: events sorted by importance desc before chunking,
       so TX 1 always contains the highest-value content.
  L4 — Chain-link: prev_anchor_txid embedded in every anchor enables full
       blockchain-only recovery without onchain-anchors.jsonl.

Cost model (0.001 ALGO per TX, mainnet 2026, v4 format):
  ~10  events/day →  1 TX/day  → ~0.37 ALGO/yr   (92% less than v2)
  ~50  events/day →  7 TX/day  → ~2.6  ALGO/yr   (88% less than v2)
  ~200 events/day → 23 TX/day  → ~8.4  ALGO/yr   (90% less than v2)
  Use pensieve_anchor(dry_run=True) for exact estimates before committing.
  Keep a dedicated low-balance anchoring wallet; top up as needed.
"""

import base64
import hashlib
import json
import os
import zlib
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── Chunk-size arithmetic ──────────────────────────────────────────────────────
# Algorand note field max: 1024 bytes (after base64 decode by SDK)
# AES-GCM envelope: NXP3(4) + nonce(12) + auth_tag(16) = 32 bytes overhead
# Usable compressed plaintext per note: 1024 − 32 = 992 bytes
# Continuation-chunk JSON overhead (keys + date + part/total + chunk_hash): ~200 bytes
# chunk_b64_len = ⌈chunk_bytes / 3⌉ × 4
# Constraint: 200 + ⌈chunk_bytes/3⌉×4 ≤ 992  →  chunk_bytes ≤ 594
# Use 500 bytes for a comfortable margin. Chunks are compressed-content bytes.
_CHUNK_SIZE = 500
_NOTE_USABLE = 992  # max compressed plaintext bytes that fit in one encrypted note


# ── Workspace & paths ─────────────────────────────────────────────────────────

def _ws() -> Path:
    return Path(os.getenv("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace")))


def _mem() -> Path:
    return _ws() / "memory"


# ── Secrets ───────────────────────────────────────────────────────────────────

def _load_wallet() -> tuple[str, str]:
    """Return (address, mnemonic). Env vars take priority over the .secrets file."""
    addr = os.getenv("ALGORAND_WALLET_ADDRESS", "").strip()
    mnemo = os.getenv("ALGORAND_WALLET_MNEMONIC", "").strip()
    if addr and mnemo:
        return addr, mnemo
    # Fallback to file (local dev only — prefer env vars in all deployments)
    f = _ws() / ".secrets" / "algorand-wallet-nox.json"
    if f.exists():
        import sys
        print("WARNING: using .secrets file fallback; set env vars for production", file=sys.stderr)
        d = json.loads(f.read_text(encoding="utf-8"))
        return d["address"], d["mnemonic"]
    raise RuntimeError(
        "Wallet not configured. Set ALGORAND_WALLET_ADDRESS and "
        "ALGORAND_WALLET_MNEMONIC environment variables."
    )


def _load_note_key() -> bytes:
    """Return 32-byte AES key. Env var (hex) takes priority over the .secrets file."""
    hex_key = os.getenv("ALGORAND_NOTE_KEY_HEX", "").strip()
    if hex_key:
        key = bytes.fromhex(hex_key)
        if len(key) != 32:
            raise RuntimeError("ALGORAND_NOTE_KEY_HEX must be 64 hex chars (32 bytes)")
        return key
    # Fallback to file
    f = _ws() / ".secrets" / "algorand-note-key.bin"
    if f.exists():
        import sys
        print("WARNING: using .secrets file fallback; set env vars for production", file=sys.stderr)
        key = f.read_bytes()
        if len(key) != 32:
            raise RuntimeError("Note key file must be exactly 32 bytes")
        return key
    raise RuntimeError(
        "Note key not configured. Set ALGORAND_NOTE_KEY_HEX env var (64 hex chars)."
    )


# ── JSONL helpers ─────────────────────────────────────────────────────────────

def _read_jsonl(path: Path) -> list:
    if not path.exists() or path.stat().st_size == 0:
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ── Hash chain ────────────────────────────────────────────────────────────────

def _ledger_tip(mem: Path) -> str:
    ledger = mem / "ledger.jsonl"
    if not ledger.exists() or ledger.stat().st_size == 0:
        return "GENESIS"
    last = None
    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                last = line
    return json.loads(last)["chain_hash"] if last else "GENESIS"


def _entry_hash(event: dict) -> str:
    """SHA-256 of the canonical base fields (no hash fields)."""
    base = {
        k: event[k]
        for k in ["id", "ts", "type", "source", "importance", "tags", "content"]
        if k in event
    }
    return hashlib.sha256(
        json.dumps(base, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _strip_hashes(event: dict) -> dict:
    """Return event without chain fields. Used in anchor payload (L2).
    Hash fields are recomputable from content via _entry_hash()."""
    return {k: v for k, v in event.items()
            if k not in ("entry_hash", "prev_hash", "chain_hash")}


# ── Encryption (NXP3: zlib + AES-GCM) ────────────────────────────────────────

def _encrypt(payload: bytes, key: bytes) -> bytes:
    """zlib-compress then AES-GCM encrypt. Returns NXP3 note bytes. (L1)"""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    nonce = os.urandom(12)
    compressed = zlib.compress(payload, level=9)
    ct = AESGCM(key).encrypt(nonce, compressed, None)
    return b"NXP3" + nonce + ct


def _decrypt(note_b64: str, key: bytes) -> dict:
    """Decrypt a note. Handles NXP1/NXP2 (legacy, no compression) and NXP3 (compressed)."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raw = base64.b64decode(note_b64)
    header = raw[:4]
    if header not in (b"NXP1", b"NXP2", b"NXP3"):
        raise ValueError(f"Unknown note header: {header!r}")
    nonce, ct = raw[4:16], raw[16:]
    plaintext = AESGCM(key).decrypt(nonce, ct, None)
    if header == b"NXP3":
        plaintext = zlib.decompress(plaintext)
    return json.loads(plaintext.decode("utf-8"))


# ── Algorand clients ──────────────────────────────────────────────────────────

def _algod():
    from algosdk.v2client import algod
    return algod.AlgodClient(
        os.getenv("ALGORAND_ALGOD_TOKEN", ""),
        os.getenv("ALGORAND_ALGOD_URL", "https://mainnet-api.algonode.cloud"),
    )


def _indexer():
    from algosdk.v2client import indexer
    return indexer.IndexerClient(
        os.getenv("ALGORAND_INDEXER_TOKEN", ""),
        os.getenv("ALGORAND_INDEXER_URL", "https://mainnet-idx.algonode.cloud"),
    )


def _send_tx(client, sender: str, sk, note: bytes) -> str:
    from algosdk.transaction import PaymentTxn
    sp = client.suggested_params()
    txn = PaymentTxn(sender=sender, sp=sp, receiver=sender, amt=0, note=note)
    return client.send_transaction(txn.sign(sk))


# ── Note fetch (shared by validate + recover) ─────────────────────────────────

def _get_note(row: dict, idx=None) -> str:
    """Fetch note from blockchain (preferred) or local note_b64 cache (fallback)."""
    txid = row.get("txid")
    if txid:
        try:
            client = idx if idx is not None else _indexer()
            tx = client.transaction(txid)
            note = tx.get("transaction", {}).get("note")
            if note:
                return note
        except Exception:
            pass
    note_local = row.get("note_b64")
    if note_local:
        return note_local
    raise ValueError(f"No note available for txid={txid!r}")


# ── Anchor helpers ────────────────────────────────────────────────────────────

def _last_anchor_txid(anchors_path: Path) -> str | None:
    """Return txid of the most recent part-1 (or single-TX) anchor. (L4)"""
    records = _read_jsonl(anchors_path)
    if not records:
        return None
    anchored = [
        r for r in records
        if r.get("status") == "anchored" and int(r.get("part", 1) or 1) == 1
    ]
    if not anchored:
        return None
    return max(anchored, key=lambda r: r.get("ts", "")).get("txid")


# ── Date helpers ──────────────────────────────────────────────────────────────

def _date_rows(path: Path, date_key: str) -> list:
    return [r for r in _read_jsonl(path) if str(r.get("ts", "")).startswith(date_key)]


# ── MCP server ────────────────────────────────────────────────────────────────

mcp = FastMCP("pensieve")


@mcp.tool()
def pensieve_capture(
    content: str,
    source: str = "manual",
    importance: float = 0.7,
    tags: list[str] | None = None,
) -> dict:
    """
    Capture an event into the append-only hash-chained memory ledger.

    Deduplicates by content hash — safe to call multiple times for the same
    content. Returns status='captured' or status='duplicate'.
    """
    if tags is None:
        tags = []
    mem = _mem()
    mem.mkdir(parents=True, exist_ok=True)
    events_path = mem / "events.jsonl"
    ledger_path = mem / "ledger.jsonl"

    # Deduplication
    target = hashlib.sha256(content.strip().encode()).hexdigest()
    for row in _read_jsonl(events_path):
        if hashlib.sha256(row.get("content", "").strip().encode()).hexdigest() == target:
            return {"ok": True, "status": "duplicate", "id": row.get("id")}

    prev_hash = _ledger_tip(mem)
    now = datetime.now(timezone.utc).isoformat()
    uid = hashlib.sha256(f"{now}{content}".encode()).hexdigest()[:36]

    event = {
        "id": uid,
        "ts": now,
        "type": "events",
        "source": source,
        "importance": importance,
        "tags": tags,
        "content": content,
    }
    eh = _entry_hash(event)
    ch = hashlib.sha256(f"{prev_hash}{eh}".encode()).hexdigest()
    event["entry_hash"] = eh
    event["prev_hash"] = prev_hash
    event["chain_hash"] = ch

    _append_jsonl(events_path, event)
    _append_jsonl(
        ledger_path,
        {"ts": now, "entry_hash": eh, "prev_hash": prev_hash, "chain_hash": ch, "source": source},
    )
    return {"ok": True, "status": "captured", "id": uid}


@mcp.tool()
def pensieve_dream_cycle() -> dict:
    """
    Run the daily dream cycle: scan last 24 h of events and promote recurring
    patterns into semantic, procedural, and self_model layers.
    Also detects active/superseded contradictions in semantic.
    """
    mem = _mem()
    mem.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    ts_str = now.isoformat()

    events = [
        e for e in _read_jsonl(mem / "events.jsonl")
        if datetime.fromisoformat(e.get("ts", "1970-01-01T00:00:00+00:00")) >= cutoff
    ]

    tag_counts = Counter(t for e in events for t in e.get("tags", []))
    src_counts = Counter(e.get("source", "unknown") for e in events)
    promoted_sem, promoted_proc, promoted_self = [], [], []

    for tag, n in tag_counts.items():
        if n >= 3:
            _append_jsonl(mem / "semantic.jsonl", {
                "id": f"sem-{int(now.timestamp())}-{tag}",
                "ts": ts_str, "type": "semantic", "source": "dream_cycle",
                "importance": 0.7, "tags": [tag], "status": "active",
                "content": f"Recurring focus: {tag} ({n} events/24h).",
            })
            promoted_sem.append({"tag": tag, "count": n})

    for src, n in src_counts.items():
        if src not in ("unknown", "manual") and n >= 3:
            _append_jsonl(mem / "procedural.jsonl", {
                "id": f"proc-{int(now.timestamp())}-{src}",
                "ts": ts_str, "type": "procedural", "source": "dream_cycle",
                "importance": 0.65, "tags": ["workflow", src], "status": "active",
                "content": f"Repeated workflow: source={src} appeared {n} times/24h.",
            })
            promoted_proc.append({"source": src, "count": n})

    if tag_counts.get("memory", 0) >= 5:
        _append_jsonl(mem / "self_model.jsonl", {
            "id": f"self-{int(now.timestamp())}-memory",
            "ts": ts_str, "type": "self_model", "source": "dream_cycle",
            "importance": 0.8, "tags": ["identity", "memory"], "status": "active",
            "content": "Prioritize durable memory consistency and append-only integrity.",
        })
        promoted_self.append({"rule": "memory-consistency"})

    # Contradiction detection (active vs superseded for same normalized content)
    contradictions = []
    by_content: dict = defaultdict(set)
    for r in _read_jsonl(mem / "semantic.jsonl")[-500:]:
        c = " ".join((r.get("content") or "").strip().lower().split())
        if c:
            by_content[c].add(r.get("status", "active"))
    for c, statuses in by_content.items():
        if "active" in statuses and "superseded" in statuses:
            contradictions.append({"content": c[:120], "statuses": sorted(statuses)})

    _append_jsonl(mem / "consolidation-log.jsonl", {
        "ts": ts_str, "source": "dream_cycle", "window_hours": 24,
        "events_scanned": len(events),
        "promoted": {"semantic": promoted_sem, "procedural": promoted_proc, "self_model": promoted_self},
        "contradictions": contradictions,
        "status": "ok",
    })

    return {
        "ok": True,
        "events_scanned": len(events),
        "promoted_semantic": len(promoted_sem),
        "promoted_procedural": len(promoted_proc),
        "promoted_self_model": len(promoted_self),
        "contradictions": len(contradictions),
    }


@mcp.tool()
def pensieve_anchor(date: str = "", dry_run: bool = False) -> dict:
    """
    Encrypt and anchor a day's memory to Algorand (v4 format). Idempotent.

    v4 optimizations applied automatically:
      L1 — zlib compression before AES-GCM (65-80% payload reduction)
      L2 — Events-only payload: hash fields stripped (recomputable),
           semantic/procedural/self_model omitted (regeneratable via dream_cycle)
      L3 — Priority ordering: events sorted by importance desc so TX 1
           always contains the highest-value content
      L4 — Chain-link: prev_anchor_txid in every anchor for blockchain-only recovery

    dry_run=True: returns compression and TX-count estimates without
    submitting any transaction. Safe to call without wallet configured.

    Uses a single TX when the compressed payload fits (≤992 bytes);
    falls back to chunked multi-TX otherwise (each TX = 0.001 ALGO).
    """
    mem = _mem()
    date_key = date or datetime.now(timezone.utc).date().isoformat()

    events_raw  = _date_rows(mem / "events.jsonl",    date_key)
    semantic    = _date_rows(mem / "semantic.jsonl",   date_key)
    procedural  = _date_rows(mem / "procedural.jsonl", date_key)
    self_model  = _date_rows(mem / "self_model.jsonl", date_key)

    # Ledger tip + total entry count
    ledger_tip, entries = "GENESIS", 0
    ledger_path = mem / "ledger.jsonl"
    if ledger_path.exists():
        for line in ledger_path.open("r", encoding="utf-8"):
            line = line.strip()
            if line:
                entries += 1
                ledger_tip = json.loads(line)["chain_hash"]

    anchors_path = mem / "onchain-anchors.jsonl"

    # L2: events-only, strip recomputable hash fields
    # semantic/procedural/self_model regeneratable via pensieve_dream_cycle after recovery
    # L3: sort by importance desc — highest-value events land in TX 1
    events_for_anchor = sorted(
        [_strip_hashes(e) for e in events_raw],
        key=lambda e: e.get("importance", 0),
        reverse=True,
    )

    content = {"events": events_for_anchor}
    content_bytes = json.dumps(content, separators=(",", ":"), ensure_ascii=False).encode()
    content_hash = hashlib.sha256(content_bytes).hexdigest()

    # L1: compress content before chunking (multi-TX) or full payload (single TX)
    compressed_content = zlib.compress(content_bytes, level=9)
    raw_bytes  = len(content_bytes)
    comp_bytes = len(compressed_content)

    # L4: chain-link to previous anchor
    prev_txid = _last_anchor_txid(anchors_path)

    base_meta = {
        "v": 4, "mode": "daily-consolidation", "date": date_key,
        "ledger_tip": ledger_tip, "entries": entries,
        "events_count": len(events_raw),
        "semantic_count": len(semantic),
        "procedural_count": len(procedural),
        "self_model_count": len(self_model),
        "root_hash": hashlib.sha256(
            f"{date_key}:{ledger_tip}:{entries}".encode()
        ).hexdigest(),
        "content_hash": content_hash,
        "prev_anchor_txid": prev_txid,
    }

    # Idempotency — checked after payload is built so dry_run always returns fresh stats
    if not dry_run:
        for row in _read_jsonl(anchors_path):
            if row.get("date") == date_key and row.get("ledger_tip") == ledger_tip:
                return {"ok": True, "status": "noop_already_anchored", "date": date_key}

    # ── dry_run: return sizing stats, skip TX submission ───────────────────────
    if dry_run:
        single_bytes = json.dumps(
            {**base_meta, "multi_tx": False, "content": content},
            separators=(",", ":"), ensure_ascii=False,
        ).encode()
        single_compressed_len = len(zlib.compress(single_bytes, level=9))
        fits_single = single_compressed_len <= _NOTE_USABLE
        est_txs = 1 if fits_single else max(1, -(-comp_bytes // _CHUNK_SIZE))
        return {
            "ok": True,
            "dry_run": True,
            "date": date_key,
            "events": len(events_raw),
            "content_bytes_raw": raw_bytes,
            "content_bytes_compressed": comp_bytes,
            "compression_pct": round((1 - comp_bytes / raw_bytes) * 100, 1) if raw_bytes else 0,
            "single_tx_payload_raw": len(single_bytes),
            "single_tx_payload_compressed": single_compressed_len,
            "fits_single_tx": fits_single,
            "estimated_txs": est_txs,
            "estimated_cost_algo": round(est_txs * 0.001, 4),
        }

    # Load secrets — validate mnemonic matches address before any TX
    addr, mnemo = _load_wallet()
    note_key = _load_note_key()
    from algosdk import account, mnemonic as algo_mnemonic
    sk = algo_mnemonic.to_private_key(mnemo)
    if account.address_from_private_key(sk) != addr:
        raise RuntimeError("Wallet mismatch: mnemonic does not match address")

    client = _algod()
    now_ts = datetime.now(timezone.utc).isoformat()

    # ── Single TX: compress the full payload (meta + content together) ─────────
    single_bytes = json.dumps(
        {**base_meta, "multi_tx": False, "content": content},
        separators=(",", ":"), ensure_ascii=False,
    ).encode()
    if len(zlib.compress(single_bytes, level=9)) <= _NOTE_USABLE:
        enc = _encrypt(single_bytes, note_key)
        if len(enc) > 1024:
            raise RuntimeError(f"Encrypted note {len(enc)} > 1024 bytes — reduce payload")
        txid = _send_tx(client, addr, sk, enc)
        _append_jsonl(anchors_path, {
            "ts": now_ts, "date": date_key, "txid": txid,
            "ledger_tip": ledger_tip, "entries": entries,
            "root_hash": base_meta["root_hash"], "content_hash": content_hash,
            "multi_tx": False,
            "note_b64": base64.b64encode(enc).decode("ascii"),
            "status": "anchored",
        })
        return {
            "ok": True, "status": "anchored", "date": date_key, "txid": txid,
            "multi_tx": False,
            "events": len(events_raw),
            "note_bytes": len(enc),
            "content_bytes_raw": raw_bytes,
            "content_bytes_compressed": comp_bytes,
            "compression_pct": round((1 - comp_bytes / raw_bytes) * 100, 1) if raw_bytes else 0,
            "cost_algo_estimate": 0.001,
        }

    # ── Multi-TX: chunk the compressed content bytes (L1 + L3 already applied) ─
    chunks = [
        compressed_content[i : i + _CHUNK_SIZE]
        for i in range(0, len(compressed_content), _CHUNK_SIZE)
    ]
    total_parts = len(chunks)
    txids = []

    for i, chunk in enumerate(chunks):
        part_num = i + 1
        chunk_hash = hashlib.sha256(chunk).hexdigest()
        chunk_b64  = base64.b64encode(chunk).decode("ascii")

        if i == 0:
            payload = {
                **base_meta,
                "multi_tx": True, "content_compressed": True,
                "total_parts": total_parts, "part": part_num,
                "chunk_hash": chunk_hash, "chunk": chunk_b64,
            }
        else:
            payload = {
                "v": 4, "mode": "daily-consolidation-part", "date": date_key,
                "part": part_num, "total_parts": total_parts,
                "chunk_hash": chunk_hash, "chunk": chunk_b64,
            }

        payload_bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
        # Safety: confirm the wrapper JSON fits after NXP3 compression
        if len(zlib.compress(payload_bytes, level=9)) > _NOTE_USABLE:
            raise RuntimeError(
                f"Chunk {part_num} compressed payload exceeds {_NOTE_USABLE} bytes. "
                "Decrease _CHUNK_SIZE."
            )

        enc  = _encrypt(payload_bytes, note_key)
        txid = _send_tx(client, addr, sk, enc)
        txids.append(txid)

        _append_jsonl(anchors_path, {
            "ts": now_ts, "date": date_key, "txid": txid,
            "ledger_tip": ledger_tip, "entries": entries,
            "root_hash": base_meta["root_hash"], "content_hash": content_hash,
            "multi_tx": True, "part": part_num, "total_parts": total_parts,
            "note_b64": base64.b64encode(enc).decode("ascii"),
            "status": "anchored",
        })

    return {
        "ok": True, "status": "anchored", "date": date_key,
        "txids": txids, "multi_tx": True, "total_parts": total_parts,
        "events": len(events_raw),
        "content_bytes_raw": raw_bytes,
        "content_bytes_compressed": comp_bytes,
        "compression_pct": round((1 - comp_bytes / raw_bytes) * 100, 1) if raw_bytes else 0,
        "cost_algo_estimate": round(total_parts * 0.001, 4),
    }


@mcp.tool()
def pensieve_validate(date: str = "") -> dict:
    """
    Run v4 hardening validation for a date (default: today).

    Checks:
      1. Local event hash-chain integrity
      2. Anchor payload decrypt + decompress (NXP3) or legacy (NXP1/NXP2)
      3. Per-chunk hash verification (multi-TX)
      4. Full content_hash verification
      5. Event count parity (local vs on-chain)
      6. entry_hash set parity (recomputed from on-chain events for v4)
      7. Probable content truncation warnings

    Returns ok=true only when all checks pass.
    """
    mem = _mem()
    date_key = date or datetime.now(timezone.utc).date().isoformat()
    issues: list[str] = []
    warnings: list[str] = []

    # 1 — Local chain integrity
    day_events = _date_rows(mem / "events.jsonl", date_key)
    for i, e in enumerate(day_events):
        expected_eh = _entry_hash(e)
        if e.get("entry_hash") != expected_eh:
            issues.append(f"event[{i}] entry_hash mismatch")
        if i > 0 and e.get("prev_hash") != day_events[i - 1].get("chain_hash"):
            issues.append(f"event[{i}] prev_hash not linked to previous chain_hash")
        expected_ch = hashlib.sha256(
            f"{e.get('prev_hash', '')}{e.get('entry_hash', '')}".encode()
        ).hexdigest()
        if e.get("chain_hash") != expected_ch:
            issues.append(f"event[{i}] chain_hash mismatch")

    # 2 — Anchor recoverability
    try:
        note_key = _load_note_key()
    except RuntimeError as e:
        return {"ok": False, "date": date_key, "issues": [str(e)], "warnings": []}

    day_anchors = [
        r for r in _read_jsonl(mem / "onchain-anchors.jsonl")
        if r.get("date") == date_key and r.get("status") == "anchored"
    ]
    if not day_anchors:
        issues.append("no anchored rows for date")
        return {
            "ok": False, "date": date_key,
            "local_events": len(day_events), "onchain_events": 0,
            "issues": issues, "warnings": warnings,
            "recovery_verdict": "FAIL",
        }

    latest_ts = max(r.get("ts", "") for r in day_anchors)
    latest = sorted(
        [r for r in day_anchors if r.get("ts") == latest_ts],
        key=lambda r: int(r.get("part", 0) or 0),
    )

    idx = _indexer()

    try:
        first_payload = _decrypt(_get_note(latest[0], idx), note_key)
    except Exception as e:
        issues.append(f"anchor decrypt failed: {e}")
        return {
            "ok": False, "date": date_key,
            "local_events": len(day_events), "onchain_events": 0,
            "issues": issues, "warnings": warnings,
            "recovery_verdict": "FAIL",
        }

    is_multi = bool(first_payload.get("multi_tx", False))
    anchor_v = int(first_payload.get("v", 2) or 2)
    anchored_events: list = []

    if not is_multi:
        content = first_payload.get("content") or {}
        anchored_events = content.get("events", []) if isinstance(content, dict) else []
        # Verify content_hash for v4+ single TX
        if anchor_v >= 4:
            content_bytes = json.dumps(
                content, separators=(",", ":"), ensure_ascii=False
            ).encode()
            if hashlib.sha256(content_bytes).hexdigest() != first_payload.get("content_hash"):
                issues.append("content_hash mismatch (single TX)")
    else:
        expected_total = int(first_payload.get("total_parts", 0) or 0)
        if len(latest) != expected_total:
            issues.append(
                f"incomplete anchor set: got {len(latest)}, expected {expected_total}"
            )

        chunks_by_part: dict[int, bytes] = {}
        for row in latest:
            try:
                p = _decrypt(_get_note(row, idx), note_key)
                pnum = int(p.get("part", 0) or 0)
                chunk = base64.b64decode(p.get("chunk", ""))
                if hashlib.sha256(chunk).hexdigest() != p.get("chunk_hash"):
                    issues.append(f"chunk hash mismatch at part {pnum}")
                chunks_by_part[pnum] = chunk
            except Exception as e:
                issues.append(f"part decrypt/hash error: {e}")

        missing = [p for p in range(1, expected_total + 1) if p not in chunks_by_part]
        if missing:
            issues.append(f"missing parts: {missing}")
        else:
            raw_assembled = b"".join(chunks_by_part[p] for p in range(1, expected_total + 1))
            # v4 multi-TX: chunks are compressed content bytes; decompress to verify
            content_compressed = bool(first_payload.get("content_compressed", False))
            if content_compressed:
                try:
                    full_bytes = zlib.decompress(raw_assembled)
                except Exception as e:
                    issues.append(f"content decompression failed: {e}")
                    full_bytes = b""
            else:
                full_bytes = raw_assembled
            if full_bytes:
                if hashlib.sha256(full_bytes).hexdigest() != first_payload.get("content_hash"):
                    issues.append("content_hash mismatch after reassembly")
                else:
                    anchored_events = json.loads(full_bytes.decode("utf-8")).get("events", [])

    # 3 — Event count parity
    if len(anchored_events) != len(day_events):
        issues.append(
            f"events count mismatch local={len(day_events)} onchain={len(anchored_events)}"
        )

    # 4 — entry_hash set parity
    # v4+: on-chain events have no hash fields; recompute from content for comparison
    local_hashes = {e.get("entry_hash") for e in day_events}
    if anchor_v >= 4:
        onchain_hashes = {_entry_hash(e) for e in anchored_events}
    else:
        onchain_hashes = {e.get("entry_hash") for e in anchored_events}
    if local_hashes != onchain_hashes:
        issues.append("entry_hash set mismatch local vs onchain")

    # 5 — Truncation check
    for ev in anchored_events:
        c = (ev.get("content") or "").strip()
        if c and c[-1] not in '.!?"\'`\n}]0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            warnings.append(f"probable truncation in event {str(ev.get('id', '?'))[:12]}")

    return {
        "ok": len(issues) == 0,
        "date": date_key,
        "anchor_v": anchor_v,
        "local_events": len(day_events),
        "onchain_events": len(anchored_events),
        "issues": issues,
        "warnings": warnings,
        "recovery_verdict": "PASS" if len(issues) == 0 else "FAIL",
    }


@mcp.tool()
def pensieve_recover(
    date: str = "",
    restore: bool = False,
    start_txid: str = "",
    walk_chain: bool = False,
) -> dict:
    """
    Recover memory from Algorand blockchain.

    Normal mode (date provided):
      Recover a specific date's memory. Prefers on-chain note via txid;
      falls back to locally cached note_b64 if indexer is unreachable.
      Verifies content_hash before returning.
      restore=True: write recovered JSONL files to memory/recovered/.

    Walk-chain mode (walk_chain=True, start_txid provided):
      Given any known anchor txid, walk backward through prev_anchor_txid
      links to rebuild the onchain-anchors.jsonl index from the blockchain
      alone — no local state required. Use this after a fatal loss of the
      workspace to rediscover all anchored dates before running normal recovery.
      Returns a list of discovered anchors with their dates and event counts.
    """
    mem = _mem()
    note_key = _load_note_key()
    idx = _indexer()

    # ── Walk-chain mode ────────────────────────────────────────────────────────
    if walk_chain:
        if not start_txid:
            return {"ok": False, "error": "walk_chain requires start_txid"}
        anchors_path = mem / "onchain-anchors.jsonl"
        discovered = []
        current_txid = start_txid
        seen: set[str] = set()

        while current_txid and current_txid not in seen:
            seen.add(current_txid)
            try:
                tx = idx.transaction(current_txid)
                note = tx.get("transaction", {}).get("note")
                if not note:
                    break
                payload = _decrypt(note, note_key)
            except Exception as e:
                discovered.append({"txid": current_txid, "error": str(e)})
                break

            anchor_date  = payload.get("date", "unknown")
            anchor_v     = payload.get("v", "?")
            is_multi     = bool(payload.get("multi_tx", False))
            events_count = payload.get("events_count", 0)
            ledger_tip   = payload.get("ledger_tip", "")
            root_hash    = payload.get("root_hash", "")
            content_hash = payload.get("content_hash", "")
            prev_txid    = payload.get("prev_anchor_txid")

            entry = {
                "ts": tx.get("transaction", {}).get("round-time", ""),
                "date": anchor_date,
                "txid": current_txid,
                "ledger_tip": ledger_tip,
                "entries": payload.get("entries", 0),
                "root_hash": root_hash,
                "content_hash": content_hash,
                "multi_tx": is_multi,
                "part": int(payload.get("part", 1) or 1),
                "total_parts": int(payload.get("total_parts", 1) or 1),
                "note_b64": note,
                "status": "anchored",
            }

            # Save to local index if not already present
            existing = _read_jsonl(anchors_path)
            already = any(
                r.get("txid") == current_txid for r in existing
            )
            if not already:
                _append_jsonl(anchors_path, entry)

            discovered.append({
                "date": anchor_date,
                "txid": current_txid,
                "anchor_v": anchor_v,
                "events_count": events_count,
                "multi_tx": is_multi,
                "total_parts": int(payload.get("total_parts", 1) or 1),
            })

            current_txid = prev_txid or ""

        return {
            "ok": True,
            "walk_chain": True,
            "anchors_discovered": len(discovered),
            "anchors": discovered,
            "note": "Run pensieve_recover(date=...) for full content recovery of each date.",
        }

    # ── Normal recovery mode ───────────────────────────────────────────────────
    if not date:
        return {"ok": False, "error": "date required for normal recovery (YYYY-MM-DD)"}

    records = [
        r for r in _read_jsonl(mem / "onchain-anchors.jsonl")
        if r.get("date") == date and r.get("status") == "anchored"
    ]
    if not records:
        return {"ok": False, "error": f"No anchors found for date {date}"}

    latest_ts = max(r.get("ts", "") for r in records)
    selected  = sorted(
        [r for r in records if r.get("ts") == latest_ts],
        key=lambda r: int(r.get("part", 0) or 0),
    )

    first_payload = _decrypt(_get_note(selected[0], idx), note_key)
    is_multi  = bool(first_payload.get("multi_tx", False))
    anchor_v  = int(first_payload.get("v", 2) or 2)

    if not is_multi:
        if anchor_v == 1:
            return {"ok": True, "date": date, "version": 1, "content": None,
                    "note": "v1 anchor: no content stored on-chain"}
        content = first_payload.get("content") or {}
        content_bytes = json.dumps(
            content, separators=(",", ":"), ensure_ascii=False
        ).encode()
        verified = hashlib.sha256(content_bytes).hexdigest() == first_payload.get("content_hash")
    else:
        expected_total = int(first_payload.get("total_parts", 0) or 0)
        if len(selected) != expected_total:
            return {
                "ok": False,
                "error": f"Incomplete anchor: {len(selected)}/{expected_total} parts",
            }

        chunks_by_part: dict[int, bytes] = {}
        for row in selected:
            p    = _decrypt(_get_note(row, idx), note_key)
            pnum = int(p.get("part", 0))
            chunk = base64.b64decode(p["chunk"])
            if hashlib.sha256(chunk).hexdigest() != p.get("chunk_hash"):
                return {"ok": False, "error": f"Chunk hash mismatch at part {pnum}"}
            chunks_by_part[pnum] = chunk

        raw_assembled = b"".join(chunks_by_part[p] for p in range(1, expected_total + 1))

        # v4 multi-TX: chunks are compressed content bytes
        content_compressed = bool(first_payload.get("content_compressed", False))
        if content_compressed:
            full_bytes = zlib.decompress(raw_assembled)
        else:
            full_bytes = raw_assembled

        verified = hashlib.sha256(full_bytes).hexdigest() == first_payload.get("content_hash")
        if not verified:
            return {"ok": False, "error": "content_hash mismatch — data may be corrupted"}
        content = json.loads(full_bytes.decode("utf-8"))

    result: dict = {
        "ok": True, "date": date,
        "version": anchor_v,
        "multi_tx": is_multi,
        "verified": verified,
        "anchor_ts": selected[0].get("ts"),
        "events": len(content.get("events", [])) if isinstance(content, dict) else 0,
        "semantic": len(content.get("semantic", [])) if isinstance(content, dict) else 0,
        "procedural": len(content.get("procedural", [])) if isinstance(content, dict) else 0,
        "self_model": len(content.get("self_model", [])) if isinstance(content, dict) else 0,
    }

    if anchor_v >= 4:
        result["note"] = (
            "v4 anchor: semantic/procedural/self_model not stored on-chain. "
            "Run pensieve_dream_cycle() after restoring events to regenerate them."
        )

    if restore and content:
        out = mem / "recovered"
        out.mkdir(parents=True, exist_ok=True)
        written = []
        for layer, rows in content.items():
            if rows:
                p = out / f"{layer}_recovered_{date}.jsonl"
                with p.open("w", encoding="utf-8") as f:
                    for row in rows:
                        f.write(json.dumps(row, ensure_ascii=False) + "\n")
                written.append(str(p))
        result["restored_files"] = written

    return result


@mcp.tool()
def pensieve_status() -> dict:
    """
    Return current memory state: layer counts, chain tip, last anchor date,
    and a cost estimate for anchoring today's accumulated data (v4 format).
    """
    mem = _mem()

    def _count(path: Path) -> int:
        return sum(1 for _ in _read_jsonl(path))

    today = datetime.now(timezone.utc).date().isoformat()
    today_events   = _date_rows(mem / "events.jsonl",    today)
    today_sem      = _date_rows(mem / "semantic.jsonl",   today)
    today_proc     = _date_rows(mem / "procedural.jsonl", today)
    today_self     = _date_rows(mem / "self_model.jsonl", today)

    # Cost estimate uses v4 payload: events-only, no hash fields, compressed
    events_for_estimate = [_strip_hashes(e) for e in today_events]
    content_raw = json.dumps(
        {"events": events_for_estimate}, separators=(",", ":"), ensure_ascii=False
    ).encode()
    raw_bytes  = len(content_raw)
    comp_bytes = len(zlib.compress(content_raw, level=9)) if raw_bytes else 0
    est_txs    = max(1, -(-comp_bytes // _CHUNK_SIZE))  # ceiling division
    est_cost   = round(est_txs * 0.001, 4)

    anchors = _read_jsonl(mem / "onchain-anchors.jsonl")
    last_anchor = (
        max(anchors, key=lambda r: r.get("ts", "")).get("date")
        if anchors else None
    )

    return {
        "ok": True,
        "workspace": str(mem),
        "totals": {
            "events":     _count(mem / "events.jsonl"),
            "semantic":   _count(mem / "semantic.jsonl"),
            "procedural": _count(mem / "procedural.jsonl"),
            "self_model": _count(mem / "self_model.jsonl"),
        },
        "chain_tip": _ledger_tip(mem),
        "last_anchor_date": last_anchor,
        "today": {
            "date": today,
            "events": len(today_events),
            "content_bytes_raw": raw_bytes,
            "content_bytes_compressed": comp_bytes,
            "compression_pct": round((1 - comp_bytes / raw_bytes) * 100, 1) if raw_bytes else 0,
            "estimated_txs": est_txs,
            "estimated_cost_algo": est_cost,
        },
    }


if __name__ == "__main__":
    mcp.run()
