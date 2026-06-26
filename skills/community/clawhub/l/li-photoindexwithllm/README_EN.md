# Photo Search Skill - English

📸 Smart photo indexing and semantic search powered by VL (Vision-Language) models

## Overview

PhotoIndexWithLLM is a smart photo indexing and search system powered by Vision-Language (VL) large models.

## Quick Start

```bash
# Install dependencies
pip install requests

# Scan photos
python skill.py scan --dir /home/user/Photos

# Search photos
python skill.py search "beach sunset"

# JSON output
python skill.py search "beach" --format json
```

## Supported Platforms

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Supported Image Formats (17 types)

| Type | Formats |
|------|---------|
| Common | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Other RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Privacy Protection

- Local-only by default
- Photos never leave your machine
- Remote transfer requires user consent

## Full Commands

```bash
# Scan photos
python skill.py scan --dir /home/user/Photos

# Search photos
python skill.py search "beach sunset"

# Scan and search
python skill.py scan_and_search --dir /home/user/Photos --query "beach"

# Annotate
python skill.py annotate --photo /photos/img001.jpg --type person --name John

# Train model
python skill.py train

# View stats
python skill.py stats

# Test connection
python skill.py test
```

## Contact

**Author**: Beijing Lao Li (beijingLL)
**ClawHub ID**: 43622283
