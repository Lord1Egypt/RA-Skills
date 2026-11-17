# Quickstart

```bash
python scripts/self_check.py
python scripts/lygo_lora.py plain
python scripts/lygo_lora.py encode --badge examples/demo_badge.json
python scripts/lygo_lora.py decode --pulse "LY1/LF_HOME/833e6a87eb4406935d626480ae116db51ab3790921840f81fe7c53bc7c3b90c1/A/0"
python scripts/lygo_lora.py probe
```

No board → `NAMED_SHADOW`. Flash stock Meshtastic, then paste a received `LY1/...` line into a file and `probe --pulse-file that.txt`.
