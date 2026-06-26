#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def run(cmd, payload):
    proc = subprocess.run(cmd, input=json.dumps(payload).encode(), stdout=subprocess.PIPE, check=True)
    return json.loads(proc.stdout.decode())


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: paper_runner.py <config.json> <market.json> <context.json>")
        return 2
    base = Path(__file__).resolve().parent
    config = json.loads(Path(sys.argv[1]).read_text())
    market = json.loads(Path(sys.argv[2]).read_text())
    context = json.loads(Path(sys.argv[3]).read_text())

    features = run([sys.executable, str(base / "compute_features.py")], market)
    signal = run([sys.executable, str(base / "compute_signal.py")], {"features": features, "context": context})
    confluence = run([sys.executable, str(base / "compute_confluence.py")], {"checks": context.get("checks", {})})
    leverage = run([sys.executable, str(base / "recommend_leverage.py")], {
        "min_leverage": config["min_leverage"],
        "max_leverage": config["max_leverage"],
        "confidence": confluence["confidence"],
        "high_volatility": context.get("high_volatility", False)
    })

    output = {
        "mode": config["mode"],
        "signal": signal["signal"],
        "confluence": confluence,
        "leverage": leverage,
        "note": "paper runner only; no live order placement"
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
