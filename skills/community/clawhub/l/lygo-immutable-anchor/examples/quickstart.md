# Quickstart

```bash
python scripts/self_check.py
python scripts/anchor_cli.py demo
python scripts/anchor_cli.py seal-geodesic \
  --truth "Truth continuous" --light "Light stable" --chaos "Next vector"
python scripts/anchor_cli.py worker-plan
```

Stack (separate, human):

```bash
python tools/run_anchor_audit.py
python tools/anchor_autonomy_worker.py --loop --interval 300 --slm-each-pulse
```
