# Data IO Patterns - Google Colab

## Source Approval Matrix

| Source | Best For | Validation Gate |
|--------|----------|-----------------|
| Google Drive | Shared datasets and quick iteration | Mount success plus path checksum |
| Google Cloud Storage | Large datasets and pipeline handoff | Bucket path validation and object count check |
| HTTPS URL | Public references and snapshots | Hash or size check after download |
| Manual upload | Small ad hoc samples | File name and schema check before use |

## Pre-Run Validation Checklist

Before training or full inference:
- verify source path exists and permissions are valid
- sample first rows and confirm required columns
- check class balance or target distribution
- confirm train/validation split is deterministic

## Output Discipline

For outputs and artifacts:
- write to timestamped folder
- include metrics summary and config snapshot
- avoid overwriting prior experiment outputs

## Failure Signals

Stop and investigate when:
- row count changes unexpectedly between runs
- required columns appear as all-null
- split leakage is detected
