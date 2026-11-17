# LYGO Automation Workflows — quickstart

```bash
python scripts/self_check.py
python scripts/workflow_planner.py demo

python scripts/workflow_planner.py audit-task \
  --name "Touch deadman heartbeat" \
  --minutes 2 --frequency-per-month 60 --repetitive

python scripts/workflow_planner.py plan \
  --name "Local witness pack" \
  --trigger "New sealed folder of pages" \
  --condition "files are local only" \
  --action "pdw digest --file" \
  --action "continuum seal claims" \
  --field path --field sha256 \
  --tool lygo-pure-data-witness --tool lygo-continuum \
  --write ./plan.json --i-consent
```
