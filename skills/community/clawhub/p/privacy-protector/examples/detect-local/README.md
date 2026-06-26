# Detect-Local Examples

These example JSON files are meant to be copied and adjusted for real detector tuning.

- `allowlist.json` exempts known-safe values from detection.
- `blocklist.json` forces detection for high-signal values that should always be masked.
- `thresholds.json` overrides per-type confidence thresholds.

Run them with:

```bash
python3 scripts/detect_local.py \
  --input "Reach support@example.com for status updates" \
  --allowlist-file examples/detect-local/allowlist.json \
  --json
```
