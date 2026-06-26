---
name: image-annotation-qc
description: Image Annotation Quality Control Tool - Automatically detect quality issues in bounding box and polygon segmentation annotations, generate visual reports. Supports COCO/YOLO/VOC/LabelMe formats, suitable for autonomous driving, industrial inspection, security monitoring and other AI training data quality control scenarios.
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python3"],"pip":["Pillow","openpyxl"]}}}
---

# Image Annotation QC Tool

Automatically detect quality issues in image annotations and generate detailed reports with visualization.

## Features

- ✅ **Multi-format Support**: COCO / YOLO / VOC / LabelMe
- ✅ **Auto-detection**: Automatically identify format without specification
- ✅ **Scene-specific QC**: general / road / industrial / security
- ✅ **Auto-save Reports**: Save to `qc_report/` directory automatically
- ✅ **Visualization**: Generate images with error annotations (red boxes)
- ✅ **Multi-format Reports**: TXT / JSON / Excel

## Quick Start

```bash
# Basic usage (auto-detect format)
python3 scripts/qc_tool.py -i <image_dir> -a <annotation_dir>

# Specify format
python3 scripts/qc_tool.py -i ./images -a ./annotations -f labelme

# Industrial inspection scenario
python3 scripts/qc_tool.py -i ./images -a ./annotations -d industrial

# Sample 100 images
python3 scripts/qc_tool.py -i ./images -a ./annotations -s 100

# Specify output directory
python3 scripts/qc_tool.py -i ./images -a ./annotations -o ./my_report

# Generate Excel report
python3 scripts/qc_tool.py -i ./images -a ./annotations --formats txt json xlsx
```

### Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--image-dir` | `-i` | Image directory | (required) |
| `--annotation` | `-a` | Annotation file or directory | (required) |
| `--format` | `-f` | Annotation format | `auto` |
| `--domain` | `-d` | Application scenario | `general` |
| `--sample` | `-s` | Sample size | all |
| `--output` | `-o` | Output directory | `./qc_report` |
| `--formats` | - | Report formats | `txt json` |
| `--no-visual` | - | Disable visualization | false |

### Scenarios

- **general**: General purpose
- **road**: Autonomous driving (small objects, occlusions)
- **industrial**: Industrial inspection (micro-defects)
- **security**: Security monitoring

## Output Example

```
╔══════════════════════════════════════════╗
║           Image Annotation QC              ║
╠══════════════════════════════════════════╣
║  Images: 1000   Annotations: 4523         ║
║  Errors: 127    Quality Score: 85.5       ║
║  Accuracy: 97.2%                          ║
╚══════════════════════════════════════════╝
```

## Output Files

After QC completes, the following files are generated in the annotation directory:

```
annotations/
├── qc_report/
│   ├── qc_report.txt      # Text report
│   ├── qc_report.json     # JSON detailed report
│   ├── qc_report.xlsx     # Excel report (optional)
│   └── visual/            # Visualization images
│       ├── frame_001_qc.png
│       └── frame_002_qc.png
```

## Error Types

| Error | Description | Weight |
|-------|-------------|--------|
| Missing | Obvious targets not labeled | 1.0 |
| Wrong | Annotation region doesn't match target | 0.8 |
| Offset | Box edge deviates >10px | 0.5 |
| Too Large | Box significantly larger than target | 0.3 |
| Too Small | Box doesn't fully contain target | 0.5 |
| Duplicate | Same object annotated multiple times | 0.5 |
| Label Error | Wrong class label | 0.8 |

## Quality Score

```
Score = 100 × (annotations - errors×weight) / annotations

Grading:
- 90+: Excellent
- 80-89: Good
- 70-79: Pass
- <70: Fail
```

## Installation

```bash
pip install Pillow openpyxl
```

## As Module

```python
from qc_tool import AnnotationQC

qc = AnnotationQC('images/', 'annotations/', format='labelme')
data = qc.load_annotations()
result = qc.check_annotations(data)
qc.generate_report(result, formats=['txt', 'json'])
qc.visualize_errors(result)
print(f"Quality Score: {result.quality_score}")
```
