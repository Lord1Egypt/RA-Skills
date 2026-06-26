import json
from pathlib import Path

root = Path(__file__).resolve().parent
scenarios = json.loads((root / "scenarios.json").read_text())

for item in scenarios["scenarios"]:
    print(f"{item['name']}: expected HTTP {item['expect_http']}")
