"""Generates a ~500 line README for a19."""
from pathlib import Path

SETUP = Path(__file__).parent / "setup"
SETUP.mkdir(parents=True, exist_ok=True)

lines = ["# Demo Project README", ""]
lines.append("A small demo project used to evaluate how agents read files.")
lines.append("")
for i in range(1, 495):
    lines.append(f"Section {i}: This is filler content line number {i} describing some imaginary feature of the project.")
(SETUP / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"a19 README lines: {len(lines)}")
