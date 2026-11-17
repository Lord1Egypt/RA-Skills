#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TraumaCodex core — ClawHub-safe, pure local stdlib.

No network. No subprocess. No LYGO_STACK_ROOT code loading.
All logic is in this package for SkillSpector / security review.

Pipeline:
  IBI ms list → entropy seed (HMAC) → LDQ-style waveform params
  → offline package + online summary → mirror dig → optional local seal files

NOT medical. Healing codes = protocol digests only.
Signature: Delta9Phi963-TRAUMACODEX-v1.0.2
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import random
import struct
import wave
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-TRAUMACODEX-v1.0.2"
VERSION = "1.0.2"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
STATE = SKILL / "state"
DEFAULT_SALT = b"LYGO-P7-LHL-SALT-v1"


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_json(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return sha_bytes(raw)


def synthetic_ibi(n: int = 32, base_hr: float = 72.0, noise: float = 35.0) -> list[float]:
    rng = random.Random(963)
    out: list[float] = []
    for i in range(n):
        mod = 8.0 * math.sin(i / 5.0)
        out.append(60000.0 / base_hr + mod + rng.uniform(-noise, noise))
    return out


def load_ibi(path: Path | None) -> list[float]:
    if path is None:
        return synthetic_ibi()
    text = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            return [float(x) for x in data]
        if isinstance(data, dict):
            for k in ("ibi_ms", "ibi", "samples"):
                if k in data:
                    return [float(x) for x in data[k]]
        raise SystemExit("JSON IBI needs a list or {ibi_ms:[...]}")
    return [float(x) for x in text.replace(",", " ").split() if x.strip()]


def high_pass_detrend(ibi_ms: list[float], alpha: float = 0.9) -> list[float]:
    if not ibi_ms:
        return []
    out: list[float] = []
    prev = ibi_ms[0]
    for x in ibi_ms:
        prev = alpha * (prev + x - (out[-1] if out else x)) + (1 - alpha) * x
        out.append(x - prev)
    return out


def estimate_min_entropy(ibi_ms: list[float], bins: int = 8) -> float:
    if len(ibi_ms) < 2:
        return 0.0
    lo, hi = min(ibi_ms), max(ibi_ms)
    span = hi - lo or 1.0
    counts = Counter(int((v - lo) / span * (bins - 1)) for v in ibi_ms)
    n = sum(counts.values())
    p_max = max(counts.values()) / n
    return max(0.0, -math.log2(p_max))


def extract_seed(ibi_ms: list[float]) -> dict[str, Any]:
    detrended = high_pass_detrend(ibi_ms)
    h_min = estimate_min_entropy(detrended or ibi_ms)
    payload = ",".join(f"{x:.3f}" for x in (detrended or ibi_ms))
    seed = hmac.new(DEFAULT_SALT, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return {
        "h_min": round(h_min, 4),
        "entropy_sufficient": h_min >= 1.0,
        "seed_256": seed,
        "ibi_count": len(ibi_ms),
        "ibi_sha256": sha_bytes(payload.encode("utf-8")),
    }


def harmonic_params(seed_hex: str) -> dict[str, float]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    s = int(seed_hex[:16], 16)
    bpm = 72.0 + (s % 48) + (s >> 8) % 12
    root = 110.0 * (phi ** ((s % 7) - 3))
    root = max(55.0, min(880.0, root))
    intensity = 0.35 + ((s >> 16) % 1000) / 1000.0 * 0.55
    return {"bpm": float(bpm), "root_frequency": float(root), "intensity": float(intensity), "phi": phi}


def structure_blocks(seed_hex: str, n: int = 8) -> list[dict[str, Any]]:
    s = int(seed_hex[:16], 16)
    blocks = []
    for i in range(n):
        x = (s >> (i * 3)) ^ (i * 0x9E3779B9)
        blocks.append(
            {
                "block": i,
                "accent": bool(x & 1),
                "density": 0.25 + ((x >> 1) % 8) / 16.0,
                "gate": [3, 6, 9][(x >> 4) % 3],
            }
        )
    return blocks


def synthesize_samples(seed_hex: str, samples: int = 24000, sr: int = 12000) -> tuple[list[float], dict]:
    """Pure-math mono waveform (no numpy)."""
    params = harmonic_params(seed_hex)
    structure = structure_blocks(seed_hex)
    root = params["root_frequency"]
    bpm = params["bpm"]
    intensity = params["intensity"]
    block_len = samples // max(1, len(structure))
    out: list[float] = [0.0] * samples
    peak = 1e-9
    for bi, blk in enumerate(structure):
        a = bi * block_len
        b = samples if bi == len(structure) - 1 else (bi + 1) * block_len
        dens = float(blk["density"])
        gate = int(blk["gate"])
        for i in range(a, b):
            t = i / sr
            pulse = 0.5 + 0.5 * (1.0 if math.sin(2 * math.pi * (bpm / 60.0) * t * (gate / 6.0)) >= 0 else -1.0)
            v = dens * math.sin(2 * math.pi * root * t)
            v += 0.45 * dens * math.sin(2 * math.pi * root * 1.5 * t)
            v += 0.25 * dens * math.sin(2 * math.pi * root * 2.0 * t + (0.3 if blk["accent"] else 0.0))
            env = (0.4 + 0.6 * ((i - a) / max(1, b - a))) * (0.55 + 0.45 * pulse)
            y = math.tanh(v * env * intensity * 1.618)
            # soft clip
            thr = 0.7
            if abs(y) > thr:
                y = math.copysign(thr - (abs(y) - thr) * 0.35, y)
            out[i] = y
            peak = max(peak, abs(y))
    scale = 0.89 / peak
    for i in range(samples):
        out[i] *= scale
    step = max(1, samples // 64)
    fingerprint = [round(out[i], 5) for i in range(0, samples, step)][:64]
    # float32-ish bytes for sha
    raw = b"".join(struct.pack("<f", float(x)) for x in out)
    meta = {
        "params": params,
        "structure": structure,
        "sample_rate": sr,
        "samples": samples,
        "fingerprint64": fingerprint,
        "waveform_sha256": sha_bytes(raw),
    }
    return out, meta


def write_wav(path: Path, samples: list[float], sr: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        frames = b"".join(
            struct.pack("<h", max(-32767, min(32767, int(x * 32767)))) for x in samples
        )
        w.writeframes(frames)


def healing_codes(seed: str, wave_sha: str, mirror_dig: str, params: dict) -> list[dict[str, str]]:
    materials = [
        ("OPEN_CONTINUANCE", f"{seed[:24]}|{params.get('bpm')}|{params.get('root_frequency')}"),
        ("SCAR_INTERVAL", f"{wave_sha[:32]}|{params.get('intensity')}"),
        ("MIRROR_DIG", mirror_dig),
        ("DELTA9_ANCHOR", f"D9P963|{mirror_dig[:32]}|{seed[24:48]}"),
        ("OFFLINE_BROADCAST", f"local|{wave_sha[32:64]}|{seed[48:64]}"),
    ]
    codes = []
    for name, mat in materials:
        d = sha_bytes(mat.encode("utf-8"))
        codes.append(
            {
                "code_id": name,
                "seal": d[:32],
                "full_sha256": d,
                "kind": "lattice_healing_code",
                "disclaimer": "Protocol digest only — not medical advice or treatment.",
            }
        )
    return codes


def resolve_out_dir(out: Path | None, consent: bool) -> Path:
    if out is not None:
        return out
    if consent:
        STATE.mkdir(parents=True, exist_ok=True)
        return STATE
    # default: cwd/traumacodex_out (explicit local)
    d = Path.cwd() / "traumacodex_out"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run(
    *,
    ibi: list[float],
    out_dir: Path,
    write_wav_file: bool = True,
) -> dict[str, Any]:
    ent = extract_seed(ibi)
    seed = ent["seed_256"]
    samples, wave_meta = synthesize_samples(seed)
    params = wave_meta["params"]

    offline = {
        "signature": SIG,
        "version": VERSION,
        "channel": "OFFLINE",
        "generated_at": utc(),
        "entropy": {
            "h_min": ent["h_min"],
            "entropy_sufficient": ent["entropy_sufficient"],
            "seed_256": seed,
            "ibi_count": ent["ibi_count"],
            "ibi_sha256": ent["ibi_sha256"],
        },
        "waveform": {k: v for k, v in wave_meta.items() if k != "structure"}
        | {"structure": wave_meta["structure"]},
        "protection": {
            "local_is_authority": True,
            "not_medical": True,
            "raw_ibi_stored": False,
            "no_subprocess": True,
            "no_network": True,
            "in_package_only": True,
        },
    }
    offline_sha = sha_json(offline)

    online = {
        "signature": SIG,
        "version": VERSION,
        "channel": "ONLINE_SUMMARY",
        "generated_at": utc(),
        "entropy_sufficient": ent["entropy_sufficient"],
        "h_min": ent["h_min"],
        "seed_prefix": seed[:16],
        "waveform_sha256": wave_meta["waveform_sha256"],
        "params_bpm": params["bpm"],
        "params_root": params["root_frequency"],
        "fingerprint_head": wave_meta["fingerprint64"][:8],
        "protection": {
            "summaries_only": True,
            "no_raw_biometrics": True,
            "no_subprocess": True,
            "no_network": True,
        },
    }
    online_sha = sha_json(online)
    mirror_dig = sha_bytes(f"{offline_sha}|{online_sha}|D9P963".encode("utf-8"))
    codes = healing_codes(seed, wave_meta["waveform_sha256"], mirror_dig, params)
    offline["mirror_dig"] = mirror_dig
    offline["healing_codes"] = codes
    online["mirror_dig"] = mirror_dig
    online["healing_code_seals"] = [c["seal"] for c in codes]

    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    off_p = out_dir / "offline_package.json"
    on_p = out_dir / "online_summary.json"
    off_p.write_text(json.dumps(offline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    on_p.write_text(json.dumps(online, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    paths["offline_package"] = str(off_p)
    paths["online_summary"] = str(on_p)
    if write_wav_file:
        wav_p = out_dir / "traumacodex_waveform.wav"
        write_wav(wav_p, samples, int(wave_meta["sample_rate"]))
        paths["waveform_wav"] = str(wav_p)

    seal = {
        "signature": "Delta9Phi963-TRAUMACODEX-LOCAL-SEAL-v1",
        "sealed_at": utc(),
        "mirror_dig": mirror_dig,
        "offline_sha256": offline_sha,
        "online_sha256": online_sha,
        "healing_code_seals": [c["seal"] for c in codes],
        "not_medical": True,
        "in_package_only": True,
    }
    seal_p = out_dir / "local_seal.json"
    seal_p.write_text(json.dumps(seal, indent=2) + "\n", encoding="utf-8")
    paths["local_seal"] = str(seal_p)

    # verify
    match = offline.get("mirror_dig") == online.get("mirror_dig") and bool(mirror_dig)
    report = {
        "signature": SIG,
        "version": VERSION,
        "ok": match and len(codes) >= 4,
        "verdict": "ALIGNED" if match and len(codes) >= 4 else "FAIL",
        "mirror_dig": mirror_dig,
        "offline_sha256": offline_sha,
        "online_sha256": online_sha,
        "bpm": params["bpm"],
        "root_frequency": params["root_frequency"],
        "entropy_sufficient": ent["entropy_sufficient"],
        "h_min": ent["h_min"],
        "healing_codes": codes,
        "paths": paths,
        "security": {
            "subprocess": False,
            "network": False,
            "external_stack_exec": False,
            "in_package_only": True,
        },
    }
    (out_dir / "last_run.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "TraumaCodex (ClawHub-safe): map IBI timing list to dual offline/online "
            "digests + optional WAV. Pure local stdlib. No network, no subprocess. "
            "Not medical."
        )
    )
    ap.add_argument(
        "--ibi-file",
        type=Path,
        default=None,
        help="Optional path to IBI milliseconds (txt list or JSON {ibi_ms:[...]}). Demo set if omitted.",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: ./traumacodex_out)",
    )
    ap.add_argument(
        "--i-consent",
        action="store_true",
        help="Allow writes under skill state/ when --out is omitted and you prefer skill-local state",
    )
    ap.add_argument("--no-wav", action="store_true")
    ap.add_argument("--verify", action="store_true", help="Verify last packages under --out/default dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    out_dir = resolve_out_dir(args.out, args.i_consent)

    if args.verify:
        off = out_dir / "offline_package.json"
        on = out_dir / "online_summary.json"
        ok = off.is_file() and on.is_file()
        verdict = "FAIL"
        mirror = None
        if ok:
            o = json.loads(off.read_text(encoding="utf-8"))
            n = json.loads(on.read_text(encoding="utf-8"))
            mirror = o.get("mirror_dig")
            ok = o.get("mirror_dig") == n.get("mirror_dig") and bool(mirror)
            verdict = "ALIGNED" if ok else "FAIL"
        rep = {"verdict": verdict, "all_pass": ok, "mirror_dig": mirror, "out": str(out_dir)}
        print(json.dumps(rep, indent=2) if args.json else f"verdict={verdict}")
        return 0 if ok else 1

    ibi = load_ibi(args.ibi_file)
    report = run(ibi=ibi, out_dir=out_dir, write_wav_file=not args.no_wav)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"TraumaCodex {SIG} v{VERSION}")
        print(f"  verdict:    {report['verdict']}")
        print(f"  mirror_dig: {report['mirror_dig'][:40]}…")
        print(f"  bpm/root:   {report['bpm']:.1f} / {report['root_frequency']:.1f} Hz")
        print(f"  security:   no subprocess · no network · in-package only")
        print(f"  out:        {out_dir}")
        print("  not medical: healing codes are protocol digests only")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
