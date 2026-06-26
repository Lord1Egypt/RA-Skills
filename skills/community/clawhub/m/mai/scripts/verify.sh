#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
DATA_FILE="$TMP_DIR/mai.json"

python3 "$ROOT_DIR/scripts/mai.py" --help >/dev/null
python3 "$ROOT_DIR/scripts/mai_registry.py" --help >/dev/null
bash "$ROOT_DIR/scripts/install.sh" --both --dry-run >/dev/null
python3 -m unittest discover -s "$ROOT_DIR/tests"
node --test "$ROOT_DIR/tests/mai_plugin.test.mjs"

python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" merchant create \
  --id seller-a \
  --name "West Lake Tea" \
  --city Hangzhou \
  --contact "wechat:westlake" \
  --tags "tea,gift"
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" merchant create \
  --id seller-b \
  --name "City Tea Market" \
  --city Shanghai \
  --contact "phone:10086" \
  --tags "tea,wholesale"
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" product add \
  --merchant seller-a \
  --sku tea-a \
  --title "Longjing Gift Box" \
  --price 88 \
  --stock 5 \
  --category tea \
  --tags "longjing,gift"
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" product add \
  --merchant seller-b \
  --sku tea-b \
  --title "Longjing Family Pack" \
  --price 96 \
  --stock 4 \
  --category tea \
  --tags "longjing,value"
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" review add \
  --buyer alice \
  --merchant seller-a \
  --sku tea-a \
  --rating 5 \
  --comment "Fast delivery."

python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" search products \
  --query "longjing tea" \
  --max-price 100 \
  --format json >"$TMP_DIR/search.json"
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" compare \
  --skus tea-a,tea-b \
  --format json >"$TMP_DIR/compare.json"

python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order create \
  --buyer alice \
  --merchant seller-a \
  --sku tea-a \
  --quantity 2 \
  --offer-price 86
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order quote \
  --merchant seller-a \
  --order ORD-0001 \
  --unit-price 86 \
  --payment-url "https://pay.example/orders/ORD-0001" \
  --terms "External payment tracking."
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order update \
  --order ORD-0001 \
  --status confirmed \
  --actor merchant
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order update \
  --order ORD-0001 \
  --status paid_external \
  --actor buyer \
  --payment-reference wx-demo-1
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order update \
  --order ORD-0001 \
  --status fulfilled \
  --actor merchant \
  --tracking SF123
python3 "$ROOT_DIR/scripts/mai.py" --data "$DATA_FILE" order update \
  --order ORD-0001 \
  --status completed \
  --actor buyer

python3 - "$ROOT_DIR" "$DATA_FILE" "$TMP_DIR/search.json" "$TMP_DIR/compare.json" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
search = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
compare = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))

assert search["results"][0]["sku"] == "tea-a"
assert compare["best_value"]["sku"] == "tea-a"
assert data["products"]["tea-a"]["stock"] == 3
assert data["orders"]["ORD-0001"]["status"] == "completed"
assert data["orders"]["ORD-0001"]["payment_reference"] == "wx-demo-1"
assert data["sync"]["mode"] == "local-first"

skill = (root / "SKILL.md").read_text(encoding="utf-8")
assert "name: mai" in skill
assert "TODO" not in skill

package = json.loads((root / "package.json").read_text(encoding="utf-8"))
clawhub = json.loads((root / "clawhub.json").read_text(encoding="utf-8"))
assert package["name"] == clawhub["name"] == "mai"
assert package["version"] == clawhub["version"]
plugin_package = json.loads((root / "plugins" / "mai-plugin" / "package.json").read_text(encoding="utf-8"))
plugin = json.loads((root / "plugins" / "mai-plugin" / "openclaw.plugin.json").read_text(encoding="utf-8"))
assert plugin_package["name"] == plugin["id"] == "mai-plugin"
assert plugin["version"] == plugin_package["version"] == package["version"]
assert plugin_package["openclaw"]["extensions"] == ["./index.js"]
assert plugin_package["openclaw"]["compat"]["pluginApi"] == ">=2026.5.2"
assert plugin_package["openclaw"]["build"]["openclawVersion"] == "2026.5.2"
assert (root / "Dockerfile").exists()
assert (root / "docker-compose.yml").exists()
assert (root / "registry.example.env").exists()

openai_yaml = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
assert 'display_name: "Mai"' in openai_yaml
assert "$mai" in openai_yaml

print("verification ok")
PY
