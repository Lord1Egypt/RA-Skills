"""Generates a ~200 line config.yaml with port: 8080 buried inside."""
from pathlib import Path

SETUP = Path(__file__).parent / "setup"
SETUP.mkdir(parents=True, exist_ok=True)

lines = ["# server config", "server:"]
for i in range(1, 95):
    lines.append(f"  setting_{i:03d}: value_{i:03d}")
lines.append("  port: 8080")
for i in range(95, 195):
    lines.append(f"  setting_{i:03d}: value_{i:03d}")
(SETUP / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"a20 config.yaml lines: {len(lines)}")
