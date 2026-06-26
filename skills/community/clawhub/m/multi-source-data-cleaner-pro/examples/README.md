# Examples · 示例

`dirty_sample.csv` includes:
- Duplicate row (张三 写了两次)
- 4 different date formats
- Phone numbers in 2 formats
- Mixed Chinese/English booleans
- Blank row

```bash
python3 ../scripts/run_pipeline.py \
  --input dirty_sample.csv --output-dir /tmp/cleaned --pii-policy mask --dedup-keys name,phone
cat /tmp/cleaned/cleaned.json
```

Expected: 4 rows (1 duplicate removed), all dates ISO, all phones +86 + masked, names masked.
