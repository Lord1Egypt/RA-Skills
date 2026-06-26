---
name: ocsr
description: >-
  PatSight MolVision molecular image recognition: calls Patent Extractor API on 1-N
  structure images, returns SMILES/SDF and compute properties by rdkit. First-time users: register at https://patent.xinsight-ai.com/home.
  Use when the user uploads 1-n molecular structure images or wants ocsr recognition, smiles/sdf extraction.
metadata: {"openclaw":{"emoji":"https://patent.xinsight-ai.com/assets/logo-4-DizspTVJ.png", "homepage": "https://patent.xinsight-ai.com/home","requires":{"bins":["uv", "python"],"env":["PATSIGHT_ACCOUNT", "PATSIGHT_PASSWORD"]}}}
---

# MolVision Molecular Image Recognition (OCSR)

Uses PatSight **MolVision** to perform optical chemical structure recognition (OCSR) on molecular structure images, extract SMILES/SDF, compute  molecular properties by RDKit, and generate visualization dashboard image.

## Authentication

This skill calls the PatSight Patent Extractor API and **requires patsight account and password**.

**First-time users**: Register at [PatSight](https://patent.xinsight-ai.com/home).

Add to your OpenClaw config:

```json
{
  "skills": {
    "entries": {
      "ocsr": {
        "enabled": true,
         "env": {
          "PATSIGHT_ACCOUNT": "PATSIGHT_ACCOUNT",
          "PATSIGHT_PASSWORD": "PATSIGHT_PASSWORD,
        },
      }
    }
  }
}
```

Or set environment variables:

```bash
export PATSIGHT_ACCOUNT="your_account"
export PATSIGHT_PASSWORD="your_password"
```

## Quick Start

### Using the Script

```bash
uv run python skills/ocsr/scripts/run_ocsr.py patent <image1> <image2> ...
uv run python skills/ocsr/scripts/run_ocsr.py mol1.png mol2.png --outdir ./ocsr_output
uv run python skills/ocsr/scripts/run_ocsr.py patent image.jpg --token <token>
```

### Examples

```bash
# Basic OCSR on images (backward compatible: omit "patent" subcommand)
uv run python skills/ocsr/scripts/run_ocsr.py mol1.png mol2.png

# With output directory
uv run python skills/ocsr/scripts/run_ocsr.py patent mol1.png mol2.png --outdir ./ocsr_output

# With token
uv run python skills/ocsr/scripts/run_ocsr.py patent image.jpg --token $PATSIGHT_TOKEN

# With account credentials
uv run python skills/ocsr/scripts/run_ocsr.py patent image.png --account user --password pass
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--outdir <dir>` | Output directory | `./ocsr_output` |
| `--request-id <id>` | Request ID for tracking | timestamp (ms) |
| `--base-url <url>` | API base URL | `PATSIGHT_BASE_URL` or `https://patent.xinsight-ai.com/patent/api` |
| `--account <account>` | patsight account (auto-fetch token) | `PATSIGHT_ACCOUNT` |
| `--password <password>` | patsight password (auto-fetch token) | `PATSIGHT_PASSWORD` |
| `--timeout <sec>` | HTTP timeout in seconds | 180 |
| `--panel-image-size <px>` | Molecule block size in report image | 300 |

## Supported Image Formats

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tif`, `.tiff`

## Output

- `ocsr_result_<timestamp>.json`: Raw API response + enriched RDKit properties
- `ocsr_dashboard_<timestamp>.png`: Visualization report

Each result includes `smiles`, `sdf_str`, `score`, and RDKit-derived properties (formula, MW, LogP, TPSA, etc.).

## API Reference

### Endpoint

```
POST {base_url}/v1/u/extractor/image/molecules?request_id=<id>
```

- `base_url`: Default `https://patent.xinsight-ai.com/patent/api`
- Requires `Authorization: <token>` header

### Multipart fields

- `image`: Image file(s) (one `image` field per file, multiple allowed)
- `label`: Fixed as `molvision`

### Response format

API returns `{"code":1, "data":{"data":[...], "msg":"SUCCESS", ...}}`. The script converts it to `{"data": [...]}` for downstream processing. Each record contains `smiles`, `sdf_str`, `score`, `idx`, `page_idx`, `rect`, etc.

## Tips

- **1-N images**: Accept multiple image files in one run
- **Token priority**: Command-line `--token` > `PATSIGHT_TOKEN` > `--account`/`--password` > env vars
- **RDKit**: If parsing fails, raw result is preserved and properties marked unavailable
- **Partial failure**: If some files fail, processing continues and reports partial success
