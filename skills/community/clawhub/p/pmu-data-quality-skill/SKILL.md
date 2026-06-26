---
name: pmu-data-quality
description: Run data quality checks on PMU (Phasor Measurement Unit) data. Use when the user asks to validate, check, or audit PMU measurements including frequency, voltage magnitude, and phasor angle data against security limits. Also triggers for keywords like "data quality", "PMU check", "out of range", "bad data", or "security limit".
allowed-tools: [Bash, Read, Write, Glob]
---

# PMU Data Quality Checker

Performs automated data quality checks on PMU (Phasor Measurement Unit) CSV data files against configurable security limits defined in IEEE/NERC standards.

## What This Skill Checks

1. **Frequency Data** — Checks if frequency measurements stay within the nominal range (default: 59.95–60.05 Hz for 60 Hz systems)
2. **Voltage Magnitude Data** — Checks if voltage magnitudes stay within acceptable per-unit limits (default: 0.95–1.05 pu)
3. **Phasor Angle Data** — Checks if phasor angles stay within expected bounds (default: -180° to +180°, with rate-of-change check)
4. **Missing / NaN Data** — Flags rows with missing or null values
5. **Timestamp Continuity** — Detects gaps in the reporting rate (e.g., expected 30 samples/sec or 60 samples/sec)

## How to Use

### Quick check on a CSV file:
```bash
python <skill_base_path>/scripts/pmu_quality_check.py path/to/data.csv
```

### With custom limits config:
```bash
python <skill_base_path>/scripts/pmu_quality_check.py path/to/data.csv --config <skill_base_path>/templates/limits_config.json
```

### On the template sample data (for testing):
```bash
python <skill_base_path>/scripts/pmu_quality_check.py <skill_base_path>/templates/sample_pmu_data.csv
```

## Expected CSV Format

The input CSV should have columns similar to:

| timestamp | frequency | voltage_mag | voltage_angle | current_mag | current_angle |
|-----------|-----------|-------------|---------------|-------------|---------------|

- `timestamp` — ISO 8601 or Unix epoch
- `frequency` — in Hz
- `voltage_mag` — in per-unit (pu) or kV (specify in config)
- `voltage_angle` / `current_angle` — in degrees
- `current_mag` — in per-unit (pu) or Amps

Column names are configurable via the limits config JSON. If the user's CSV uses different column names (like those from openHistorian or FNET exports), update the `column_mapping` section in the config.

## Output

The script produces:
- A **summary report** printed to stdout
- A **flagged rows CSV** saved alongside the input (e.g., `data_flagged.csv`)
- An optional **HTML report** with charts if `--html` flag is passed

## Workflow

1. Ask the user for their PMU data file (CSV)
2. Check if the column names match the expected format; if not, ask or auto-detect
3. Run the quality check script
4. Present the summary and ask if the user wants to adjust limits or dig deeper into flagged data
