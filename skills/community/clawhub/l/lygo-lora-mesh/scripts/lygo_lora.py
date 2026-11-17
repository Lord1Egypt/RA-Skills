#!/usr/bin/env python3
"""LYGO LoRa mesh — compact Layer D pulse. No network. No subprocess. No radio driver."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-LYGO-LORA-MESH-v1.0.0"
VERSION = "1.0.0"
PREFIX = "LY1"
MAX_PAYLOAD = 200
MAX_NODE = 16
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
NODE_RE = re.compile(r"^[A-Za-z0-9_-]{1,16}$")
STATUS = {"A": "ALIGNED", "F": "FORK_VISIBLE", "Q": "QUARANTINE", "S": "NAMED_SHADOW"}
STATUS_FROM = {v: k for k, v in STATUS.items()}
MESHTASTIC = "https://meshtastic.org/docs/"
FIRMWARE = "https://github.com/meshtastic/firmware"
CLAWHUB = "https://clawhub.ai/deepseekoracle/skills/lygo-lora-mesh"
INSTALL = "npx clawhub@latest install deepseekoracle/lygo-lora-mesh"
LIVING = "https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh"
DEPLOY = "https://clawhub.ai/deepseekoracle/skills/lygo-mesh-deploy"

DEMO_DIGEST = "833e6a87eb4406935d626480ae116db51ab3790921840f81fe7c53bc7c3b90c1"
DEMO_NODE = "LF_HOME"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def urls() -> dict[str, str]:
    return {
        "meshtastic_docs": MESHTASTIC,
        "firmware": FIRMWARE,
        "clawhub": CLAWHUB,
        "install": INSTALL,
        "living_mesh": LIVING,
        "mesh_deploy": DEPLOY,
    }


def status_code(raw: str) -> str:
    s = str(raw or "").strip().upper()
    if s in STATUS:
        return s
    if s in STATUS_FROM:
        return STATUS_FROM[s]
    if "SHADOW" in s:
        return "S"
    if "QUARANTINE" in s:
        return "Q"
    if "FORK" in s:
        return "F"
    return "A"


def encode_pulse(node_id: str, roots_digest: str, status: str = "A", hop: int = 0) -> str:
    node = str(node_id or "NODE").strip().replace(" ", "_")[:MAX_NODE]
    if not NODE_RE.match(node):
        node = re.sub(r"[^A-Za-z0-9_-]", "", node)[:MAX_NODE] or "NODE"
    digest = str(roots_digest or "").strip().lower()
    if not DIGEST_RE.match(digest):
        raise ValueError("roots_digest must be 64 lowercase hex chars")
    hop_i = int(hop)
    if hop_i < 0 or hop_i > 7:
        raise ValueError("hop must be 0..7 (Meshtastic relay cap)")
    pulse = f"{PREFIX}/{node}/{digest}/{status_code(status)}/{hop_i}"
    n = len(pulse.encode("ascii"))
    if n > MAX_PAYLOAD:
        raise ValueError(f"pulse {n} bytes exceeds {MAX_PAYLOAD}")
    return pulse


def decode_pulse(text: str) -> dict[str, Any]:
    raw = str(text or "").strip()
    if not raw:
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "empty pulse"}
    parts = raw.split("/")
    if len(parts) != 5 or parts[0] != PREFIX:
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "not a LY1 pulse"}
    _pfx, node, digest, st, hop_s = parts
    if not NODE_RE.match(node):
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "bad node_id"}
    if not DIGEST_RE.match(digest.lower()):
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "bad roots_digest"}
    if st not in STATUS:
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "bad status"}
    try:
        hop = int(hop_s)
    except ValueError:
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "bad hop"}
    if hop < 0 or hop > 7:
        return {"ok": False, "yield": "NAMED_SHADOW", "reason": "hop out of range"}
    return {
        "ok": True,
        "yield": STATUS[st],
        "prefix": PREFIX,
        "node_id": node,
        "roots_digest": digest.lower(),
        "status": st,
        "hop": hop,
        "bytes": len(raw.encode("ascii")),
    }


def pulse_from_badge(badge: dict[str, Any]) -> str:
    lm = badge.get("living_mesh") if isinstance(badge, dict) else None
    if not isinstance(lm, dict):
        lm = {}
    node = str(badge.get("node_id") or lm.get("node_id") or "NODE")
    digest = str(lm.get("roots_digest") or "")
    status = str(lm.get("local_status") or badge.get("status") or "ALIGNED")
    return encode_pulse(node, digest, status, 0)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON object required")
    return data


def probe(pulse_file: Path | None) -> dict[str, Any]:
    if pulse_file is None or not pulse_file.is_file():
        return {
            "ok": True,
            "yield": "NAMED_SHADOW",
            "board": False,
            "reason": "no pulse file — radio absent or not paired",
            "hint": "Paste a LY1/... line from the Meshtastic app into a file and pass --pulse-file",
        }
    text = pulse_file.read_text(encoding="utf-8").strip().splitlines()
    line = ""
    for row in text:
        row = row.strip()
        if row.startswith(PREFIX + "/"):
            line = row
            break
    if not line:
        line = text[0] if text else ""
    decoded = decode_pulse(line)
    decoded["board"] = True
    decoded["pulse_file"] = str(pulse_file)
    return decoded


def compare(local_digest: str, remote: dict[str, Any]) -> dict[str, Any]:
    if not remote.get("ok"):
        return {
            "verdict": "NAMED_SHADOW",
            "local_roots_digest": local_digest,
            "remote": remote,
        }
    same = str(local_digest or "").lower() == str(remote.get("roots_digest") or "")
    if remote.get("status") == "Q":
        verdict = "QUARANTINE_SIGNAL"
    elif same:
        verdict = "HARMONIC"
    else:
        verdict = "FORK_VISIBLE"
    return {
        "verdict": verdict,
        "local_roots_digest": local_digest,
        "remote_node": remote.get("node_id"),
        "remote_roots_digest": remote.get("roots_digest"),
        "remote_status": remote.get("yield"),
        "hop": remote.get("hop"),
        "live_star_chart_ingest": False,
    }


def map_payload() -> dict[str, Any]:
    demo = encode_pulse(DEMO_NODE, DEMO_DIGEST, "A", 0)
    return {
        "signature": SIG,
        "version": VERSION,
        "channel": "CLAWHUB_PUBLIC_TENTACLE",
        "class": "RESOURCE",
        "layer": "D-RF",
        "transport": "meshtastic_lora",
        "max_payload_bytes": MAX_PAYLOAD,
        "meshtastic_cap_bytes": 237,
        "live_star_chart_ingest": False,
        "generated_utc": utc_now(),
        "demo_pulse": demo,
        "demo_bytes": len(demo.encode("ascii")),
        "urls": urls(),
        "hardware": [
            "Heltec WiFi LoRa 32 V3",
            "LILYGO T-Beam / T-Beam Supreme",
            "RAK WisBlock Meshtastic starter",
        ],
        "region": "NA 915 MHz (CA/US ISM). EU 868 MHz. Do not mix regions.",
        "forbidden": [
            "fork Meshtastic firmware into a LYGO radio OS",
            "egg payloads on RF",
            "agent cards on RF",
            "LYGO TV / video on LoRa",
            "silent Star Chart ingest",
            "auto git/HF/ClawHub/social publish",
            "subprocess serial flash",
        ],
    }


def plain() -> str:
    demo = encode_pulse(DEMO_NODE, DEMO_DIGEST, "A", 0)
    return "\n".join(
        [
            "LYGO LoRa mesh — Layer D compact pulse on Meshtastic",
            "",
            "This package does not drive a radio. Stock Meshtastic firmware does.",
            "IP up: living-mesh HTTP gossip. IP down: send this text packet.",
            "",
            "Pulse: " + demo,
            "Bytes: " + str(len(demo.encode("ascii"))) + " / " + str(MAX_PAYLOAD) + " (Meshtastic cap ~237)",
            "",
            "1. Flash stock firmware from " + MESHTASTIC,
            "2. NA boards: 915 MHz. Heltec V3, T-Beam, or RAK WisBlock.",
            "3. encode a living-mesh badge → paste the LY1 line as a Meshtastic text message.",
            "4. On the far node: save the received line → decode / compare.",
            "5. No board = NAMED_SHADOW. Never fake a peer.",
            "",
            "Eggs, TV, and Star Chart stay off RF.",
            "Install: " + INSTALL,
        ]
    )


def hardware() -> dict[str, Any]:
    return {
        "firmware": "stock Meshtastic — do not fork",
        "docs": MESHTASTIC,
        "source": FIRMWARE,
        "boards": [
            {"name": "Heltec WiFi LoRa 32 V3", "notes": "USB-C, common starter"},
            {"name": "LILYGO T-Beam / T-Beam Supreme", "notes": "GPS-capable handheld"},
            {"name": "RAK WisBlock Meshtastic starter", "notes": "modular, solar-friendly later"},
        ],
        "region_na": "915 MHz",
        "region_eu": "868 MHz",
        "pairing": "Meshtastic app over Bluetooth or USB serial — human pairs the board",
        "payload": "text message = LY1 pulse. Not MQTT. Not HTTPS.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LYGO LoRa mesh pulse codec")
    p.add_argument(
        "cmd",
        nargs="?",
        default="plain",
        choices=("plain", "urls", "map", "demo", "hardware", "encode", "decode", "probe", "compare"),
    )
    p.add_argument("--badge", type=str, default="", help="living-mesh badge JSON")
    p.add_argument("--pulse", type=str, default="", help="LY1 pulse string")
    p.add_argument("--pulse-file", type=str, default="", help="file containing a received LY1 line")
    p.add_argument("--node", type=str, default=DEMO_NODE)
    p.add_argument("--digest", type=str, default=DEMO_DIGEST)
    p.add_argument("--status", type=str, default="A")
    p.add_argument("--hop", type=int, default=0)
    args = p.parse_args(argv)

    if args.cmd == "plain":
        sys.stdout.write(plain() + "\n")
        return 0
    if args.cmd == "urls":
        print(json.dumps(urls(), indent=2))
        return 0
    if args.cmd == "hardware":
        print(json.dumps(hardware(), indent=2))
        return 0
    if args.cmd in ("map", "demo"):
        print(json.dumps(map_payload(), indent=2))
        return 0
    if args.cmd == "encode":
        try:
            if args.badge:
                pulse = pulse_from_badge(load_json(Path(args.badge)))
            else:
                pulse = encode_pulse(args.node, args.digest, args.status, args.hop)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(json.dumps({"ok": False, "yield": "NAMED_SHADOW", "error": str(e)}, indent=2))
            return 1
        print(json.dumps({"ok": True, "pulse": pulse, "bytes": len(pulse.encode("ascii"))}, indent=2))
        return 0
    if args.cmd == "decode":
        print(json.dumps(decode_pulse(args.pulse), indent=2))
        return 0 if decode_pulse(args.pulse).get("ok") else 1
    if args.cmd == "probe":
        pf = Path(args.pulse_file) if args.pulse_file else None
        out = probe(pf)
        print(json.dumps(out, indent=2))
        return 0
    local = args.digest
    if args.badge:
        try:
            b = load_json(Path(args.badge))
            lm = b.get("living_mesh") if isinstance(b.get("living_mesh"), dict) else {}
            local = str(lm.get("roots_digest") or local)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(json.dumps({"verdict": "NAMED_SHADOW", "error": str(e)}, indent=2))
            return 1
    remote = decode_pulse(args.pulse) if args.pulse else probe(Path(args.pulse_file) if args.pulse_file else None)
    print(json.dumps(compare(local, remote), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
