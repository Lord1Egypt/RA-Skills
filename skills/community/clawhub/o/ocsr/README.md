# MolVision Molecular Image Recognition (OCSR)

Uses PatSight MolVision to perform optical chemical structure recognition (OCSR) on molecular structure images, extract SMILES/SDF, compute RDKit molecular properties, and generate visualization reports.

## Getting started (first-time users)

**Don't have a PatSight account?** This skill requires a PatSight account for API authentication. Please register at [PatSight](https://patent.xinsight-ai.com/home) first. After registration, use your account credentials to obtain an OPS token and run this skill.

## Features

- **Input**: 1-N molecular structure images (PNG, JPG, WebP, BMP, TIFF, etc.)
- **Output**:
  - `ocsr_result_<timestamp>.json`: Raw API response + enriched data (including RDKit properties)
  - `ocsr_dashboard_<timestamp>.png`: Visualization report (original image, recognized molecule, molecular properties)

## Usage

### 1. Configure authentication

This skill calls the PatSight Patent Extractor API and requires an OPS token.

**Don't have a PatSight account?** Register at [PatSight](https://patent.xinsight-ai.com/home) to get started. After registration, use your account credentials below.

Choose one of the following:

**Option A: Environment variables**

```bash
export PATSIGHT_ACCOUNT="your-account"
export PATSIGHT_PASSWORD="your-password"
```

**Option B: Command-line arguments**

```bash
uv run python skills/ocsr/scripts/run_ocsr.py image.png --token "your-token"
# or
uv run python skills/ocsr/scripts/run_ocsr.py image.png --account "xxx" --password "xxx"
```

### 2. Run

```bash
uv run python skills/ocsr/scripts/run_ocsr.py <image1> <image2> ... [options]
```

**Common options**:

| Option | Description | Default |
|--------|--------------|----------|
| `--outdir` | Output directory | `./ocsr_output` |
| `--request-id` | Request ID | Timestamp in ms |
| `--base-url` | API base URL | `PATSIGHT_BASE_URL` or patent.xinsight-ai.com |
| `--timeout` | HTTP timeout (seconds) | 180 |
| `--panel-image-size` | Molecule block size in report | 300 |

### 3. Examples

```bash
# Single image
uv run python skills/ocsr/scripts/run_ocsr.py mol.png

# Multiple images, specify output directory
uv run python skills/ocsr/scripts/run_ocsr.py mol1.png mol2.jpg --outdir ./reports
```

## Dependencies

- Python 3.9+
- `requests`, `Pillow`
- `rdkit` (optional, for molecular property calculation; properties are unavailable if not installed)

Install:

```bash
uv sync
# or
pip install requests Pillow rdkit
```

## Output example

**JSON structure** (`ocsr_result_*.json`):

```json
{
  "raw_response": { "data": [...] },
  "enriched_data": [
    {
      "smiles": "Cl.NC(=O)...",
      "sdf_str": "mol block ...",
      "score": 0.76,
      "rdkit": {
        "formula": "C10H12N2O",
        "exact_mw": 176.0949,
        "logp": 1.23,
        "tpsa": 45.2,
        ...
      },
      "source_image": "/path/to/mol.png"
    }
  ]
}
```

**Report image** (`ocsr_dashboard_*.png`): Contains original image, recognized molecule structure, and molecular property table.

## Troubleshooting

### No PatSight account

If you are a first-time user or do not have a PatSight account, please register at [PatSight](https://patent.xinsight-ai.com/home). This skill requires a valid PatSight account to obtain an OPS token for API authentication.

### Token invalid or expired

- Check if `PATSIGHT_TOKEN` is valid, or configure `PATSIGHT_OPS_ACCOUNT` + `PATSIGHT_OPS_PASSWORD` for automatic refresh
- The script validates the token first; if it fails, it will attempt to refresh using account/password

### 405 / 500 errors

- Confirm base_url is correct (default `https://patent.xinsight-ai.com/patent/api`)
- Confirm the token is valid and has permission to access the Patent Extractor API

### Unsupported image format

- Supported: `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tif`, `.tiff`
- For other formats, convert to one of the supported formats first

### RDKit properties unavailable

- Install rdkit: `pip install rdkit`
- If SMILES cannot be parsed by RDKit, `rdkit_ok` is false and property fields are null
