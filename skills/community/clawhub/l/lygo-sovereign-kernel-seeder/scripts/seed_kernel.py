#!/usr/bin/env python3
"""
LYGO Sovereign Kernel Seeder — plant a Merkle-anchored egg that self-verifies on insert.

Zero external network. Consent-gated. Atomic: insert rolls back if verify fails.

Signature: Delta9Phi963-SOVEREIGN-KERNEL-SEEDER-v1.0
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-SOVEREIGN-KERNEL-SEEDER-v1.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def merkle_root(leaf_hexes: list[str]) -> str:
    """Binary Merkle root over SHA-256 leaf digests (hex). Empty → zero hash."""
    if not leaf_hexes:
        return sha256_bytes(b"")
    level = [bytes.fromhex(x) for x in sorted(leaf_hexes)]
    while len(level) > 1:
        nxt: list[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(hashlib.sha256(left + right).digest())
        level = nxt
    return level[0].hex()


def default_seed_root() -> Path:
    env = os.environ.get("LYGO_SEED_ROOT") or os.environ.get("LYGO_STACK_ROOT")
    if env:
        return Path(env) / "data" / "sovereign_seeds"
    # skill-local default (zero stack dependency)
    return Path(__file__).resolve().parents[1] / "local_seeds"


def consent_ok(args: argparse.Namespace) -> bool:
    if args.i_consent:
        return True
    return os.environ.get("LYGO_KERNEL_SEED_CONSENT", "").strip().lower() in ("1", "yes", "true")


def build_egg(
    egg_id: str,
    kind: str,
    title: str,
    summary: str,
    files: list[Path],
    hooks: list[str],
    depends_on: list[str],
    version: str,
) -> dict[str, Any]:
    modules = []
    for fp in files:
        raw = fp.read_bytes()
        digest = sha256_bytes(raw)
        # bound inline size 48 KiB per module for transport
        inline = None
        if len(raw) <= 48 * 1024:
            inline = base64.b64encode(raw).decode("ascii")
        modules.append(
            {
                "path": fp.name,
                "sha256": digest,
                "bytes": len(raw),
                **({"inline_b64": inline} if inline else {}),
                "role": "module",
            }
        )

    payload = {
        "title": title,
        "summary": summary,
        "modules": modules,
        "hooks": hooks,
        "depends_on": depends_on,
    }
    # content hash over payload only (stable)
    content_sha = sha256_bytes(canonical_json(payload))
    leaf = sha256_bytes(
        canonical_json(
            {
                "egg_id": egg_id,
                "version": version,
                "kind": kind,
                "content_sha256": content_sha,
            }
        )
    )
    egg = {
        "egg_id": egg_id,
        "version": version,
        "kind": kind,
        "signature": f"Delta9Phi963-EGG-{egg_id}-v{version}",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "steward": "Lightfather / Excavationpro / DeepSeekOracle",
        "content_sha256": content_sha,
        "payload": payload,
        "seal": {
            "alg": "sha256",
            "leaf_hash": leaf,
            "sovereign": True,
            "zero_external_surface": True,
            "self_verify_on_insert": True,
        },
        "meta": {
            "seeder": SIG,
            "sealed": True,
        },
    }
    return egg


def verify_egg_object(egg: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for k in ("egg_id", "version", "kind", "content_sha256", "payload", "seal"):
        if k not in egg:
            errors.append(f"missing field {k}")
    if errors:
        return errors
    payload = egg["payload"]
    calc = sha256_bytes(canonical_json(payload))
    if calc != egg["content_sha256"]:
        errors.append("content_sha256 mismatch")
    leaf = sha256_bytes(
        canonical_json(
            {
                "egg_id": egg["egg_id"],
                "version": egg["version"],
                "kind": egg["kind"],
                "content_sha256": egg["content_sha256"],
            }
        )
    )
    if egg.get("seal", {}).get("leaf_hash") != leaf:
        errors.append("seal.leaf_hash mismatch")
    if not egg.get("seal", {}).get("sovereign"):
        errors.append("seal.sovereign must be true")
    for m in payload.get("modules") or []:
        b64 = m.get("inline_b64")
        if b64:
            raw = base64.b64decode(b64)
            if sha256_bytes(raw) != m.get("sha256"):
                errors.append(f"module {m.get('path')} sha256 mismatch")
    return errors


def load_registry(reg_path: Path) -> dict[str, Any]:
    if reg_path.is_file():
        return json.loads(reg_path.read_text(encoding="utf-8"))
    return {
        "signature": "Delta9Phi963-SOVEREIGN-SEED-REGISTRY-v1",
        "version": "1.0.0",
        "updated_utc": None,
        "registry_merkle_root": sha256_bytes(b""),
        "eggs": {},
    }


def recompute_root(registry: dict[str, Any]) -> str:
    leaves = []
    for eid, meta in sorted(registry.get("eggs", {}).items()):
        leaves.append(meta.get("leaf_hash") or meta.get("content_sha256") or "")
    leaves = [x for x in leaves if x]
    return merkle_root(leaves)


def atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".seed_", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def seed(args: argparse.Namespace) -> int:
    if not consent_ok(args):
        print("CONSENT_REQUIRED: pass --i-consent or set LYGO_KERNEL_SEED_CONSENT=yes", file=sys.stderr)
        return 2

    root = Path(args.root) if args.root else default_seed_root()
    eggs_dir = root / "eggs"
    reg_path = root / "registry.json"
    eggs_dir.mkdir(parents=True, exist_ok=True)

    files = [Path(p) for p in (args.file or [])]
    for fp in files:
        if not fp.is_file():
            print(f"missing file: {fp}", file=sys.stderr)
            return 1

    if not files and args.manifest:
        # empty seed allowed with summary only — create placeholder note
        note = eggs_dir / f"{args.egg_id}.seed.txt"
        note.write_text(
            f"# {args.egg_id}\n{args.summary or args.title}\nseeder={SIG}\n",
            encoding="utf-8",
        )
        files = [note]

    if not files:
        print("Provide --file PATH or --manifest with --title/--summary", file=sys.stderr)
        return 1

    egg = build_egg(
        egg_id=args.egg_id,
        kind=args.kind,
        title=args.title or args.egg_id,
        summary=args.summary or "",
        files=files,
        hooks=[h for h in (args.hook or [])],
        depends_on=[d for d in (args.depends or [])],
        version=args.version,
    )

    # SELF-VERIFY BEFORE INSERT
    errs = verify_egg_object(egg)
    if errs:
        print("PRE_INSERT_VERIFY_FAIL:", "; ".join(errs), file=sys.stderr)
        return 3

    egg_path = eggs_dir / f"{args.egg_id}.egg.json"
    # write egg then registry atomically as a transaction
    registry = load_registry(reg_path)
    backup = json.loads(json.dumps(registry))

    registry["eggs"][args.egg_id] = {
        "egg_id": args.egg_id,
        "version": egg["version"],
        "kind": egg["kind"],
        "content_sha256": egg["content_sha256"],
        "leaf_hash": egg["seal"]["leaf_hash"],
        "path": str(egg_path.name),
        "created_utc": egg["created_utc"],
        "signature": egg["signature"],
    }
    registry["registry_merkle_root"] = recompute_root(registry)
    registry["updated_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    registry["seeder"] = SIG

    try:
        atomic_write_json(egg_path, egg)
        atomic_write_json(reg_path, registry)

        # POST-INSERT VERIFY (mandatory)
        reloaded = json.loads(egg_path.read_text(encoding="utf-8"))
        errs2 = verify_egg_object(reloaded)
        reg2 = load_registry(reg_path)
        root2 = recompute_root(reg2)
        if errs2 or root2 != reg2.get("registry_merkle_root"):
            # rollback
            if args.egg_id in backup.get("eggs", {}):
                atomic_write_json(reg_path, backup)
            else:
                # remove new egg entry
                atomic_write_json(reg_path, backup)
            if egg_path.is_file():
                egg_path.unlink()
            print("POST_INSERT_VERIFY_FAIL → rolled back", errs2 or "merkle root", file=sys.stderr)
            return 3
    except Exception as e:
        atomic_write_json(reg_path, backup)
        print(f"SEED_ABORT: {e}", file=sys.stderr)
        return 1

    out = {
        "status": "SEEDED_ALIGNED",
        "egg_id": args.egg_id,
        "content_sha256": egg["content_sha256"],
        "leaf_hash": egg["seal"]["leaf_hash"],
        "registry_merkle_root": registry["registry_merkle_root"],
        "path": str(egg_path),
        "registry": str(reg_path),
        "seeder": SIG,
        "zero_external_surface": True,
    }
    print(json.dumps(out, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="LYGO Sovereign Kernel Seeder")
    p.add_argument("--i-consent", action="store_true", help="Explicit human consent this turn")
    p.add_argument("--egg-id", required=True, help="Egg id (lowercase)")
    p.add_argument("--kind", default="seed", choices=[
        "protocol", "agent", "champion", "driver", "skill-pin", "memory", "policy", "tool", "seed"
    ])
    p.add_argument("--version", default="1.0.0")
    p.add_argument("--title", default="")
    p.add_argument("--summary", default="")
    p.add_argument("--file", action="append", help="Module file to seal (repeatable)")
    p.add_argument("--hook", action="append", help="Stack hook name (repeatable)")
    p.add_argument("--depends", action="append", help="Dependency egg_id (repeatable)")
    p.add_argument("--manifest", action="store_true", help="Allow title/summary-only seed note")
    p.add_argument("--root", default="", help="Seed root (default LYGO_SEED_ROOT or skill local_seeds)")
    args = p.parse_args()
    return seed(args)


if __name__ == "__main__":
    sys.exit(main())
