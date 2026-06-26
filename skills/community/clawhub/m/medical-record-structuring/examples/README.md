# Examples · 示例

## admission_input.txt
A canonical admission note in Chinese. Run:

```bash
python3 ../scripts/run_pipeline.py --input admission_input.txt --record-type admission
```

Expected output structure (`extraction_report.entities_count`):
- patient: 1
- vitals: 5 (T, P, R, systolic_bp, diastolic_bp)
- diagnosis: 3
- medication: 3
