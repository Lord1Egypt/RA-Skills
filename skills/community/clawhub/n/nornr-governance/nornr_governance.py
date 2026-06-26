import sys

try:
    from agentpay.openclaw import openclaw_cli
except ImportError as exc:  # pragma: no cover - install-time guard
    sys.stderr.write(
        "Missing dependency: agentpay\n"
        "Install the pinned NORNR SDK dependency first:\n"
        "  python -m pip install -r requirements.txt\n"
        "Pinned package release:\n"
        "  nornr-agentpay==0.1.0\n"
    )
    raise SystemExit(1) from exc


if __name__ == "__main__":
    raise SystemExit(openclaw_cli())
