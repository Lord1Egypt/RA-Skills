---
name: late-brake
version: 0.0.3
description: Pure CLI racing lap data analysis tool. Supports NMEA/VBO import, auto lap splitting, lap comparison, outputs structured comparison results for AI coaching. Use when you need to analyze racing lap data files, compare two laps, and get structured comparison results.
metadata:
  openclaw:
    requires:
      python: ">=3.10"
      dependencies:
        - click>=8.0
        - pydantic>=2.0
        - numpy>=1.24
        - geographiclib>=2.0
        - jsonschema>=4.0
        - wcwidth>=0.2.0
---

# Late Brake - Racing Lap Data Analysis Skill

Late Brake is a pure command-line (CLI) racing lap data analysis tool that provides:
- Import lap data in NMEA 0183 / RaceChrono VBO formats
- Auto split laps based on track start/finish line
- Compare any two laps for time/speed differences by sector and corner
- Output structured JSON comparison results ready for AI coach analysis

## Dependencies

- Python >= 3.10
- Dependencies: click, pydantic, numpy, geographiclib, jsonschema, wcwidth

Dependencies are declared in SKILL.md, OpenClaw will handle automatic installation.

## Entry Points

Source code is directly in `scripts/` directory, can be imported directly:

```python
import sys
import os
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from late_brake.cli import main as late_brake_main
```

Or execute directly as command-line:

```bash
# Load data file, list all laps
python -m late_brake.cli load <file> --json

# Compare two laps, output JSON result
python -m late_brake.cli compare <file1> <lap1> <file2> <lap2> --json
```

## Features

| Feature | Command | Description |
|---------|---------|-------------|
| Load data file | `late-brake load <file>` | Parse data, auto split laps, list all detected laps |
| Compare two laps | `late-brake compare <file1> <lap1> <file2> <lap2>` | Compare lap differences, output text table or JSON |
| Track management | `late-brake track list/info/add` | Manage built-in/custom tracks |

## JSON Output Schema

Full JSON schema definition: [compare-json-schema.md](references/compare-json-schema.md)

## Use Cases

- Racing drivers upload lap data files for comparison analysis
- AI racing coach needs structured comparison data to give advice
- Batch processing multiple lap data files
