# Hong Kong MTR Next-Train ETA - Technical Reference

> ⚠️ **For complete documentation, please refer to the [main README.md](https://github.com/tomfong/hk-mtr-next-train-skill)**
> 
> This file contains technical reference information for the Hong Kong MTR Next-Train skill.

## Quick Links

- **[Main Documentation](https://github.com/tomfong/hk-mtr-next-train-skill/blob/master/README.md)** - Complete user guide with installation, usage examples, and features
- **[SKILL.md](./SKILL.md)** - Technical specification for AI agents
- **[Scripts Directory](./scripts/)** - Python scripts for MTR data queries

## Technical Overview

**Skill Name:** `hk-mtr-next-train`  
**Version:** 1.0.1  
**Last Updated:** 2026-03-22  
**Compatibility:** OpenClaw and compatible AI agents

### Core Components

1. **`mtr_eta.py`** - Main query script for MTR next-train ETA lookups
2. **`sync_mtr_stations.py`** - Data (CSV) initialization and sync script

### API Endpoints

**Data Sources:**
- **MTR Trains ETA**: `https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php`
- **MTR Stations Data (CSV)**: `https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv`

## Script Usage
### Main Query Script
```bash
python3 mtr_eta.py {STATION_NAME} {LINE_NAME(optional)} {LANG(optional)} {TO_STATION(optional)}
```

**Parameters:**
- `STATION_NAME`: Station name (e.g., "Central", "Tsim Sha Tsui", "旺角")
- `LINE_NAME`: Line name (e.g., "Island Line", "East Rail Line", "觀塘線")
- `LANG`: Output language - `tc` (Traditional Chinese) or `en` (English)
- `TO_STATION`: Explicit station name of train's destination (e.g., "LOHAS Park", "Lo Wu")

**Examples:**
```bash
# Chinese output
python3 mtr_eta.py 旺角 觀塘線 tc 調景嶺

# English output  
python3 mtr_eta.py Airport Airport Express en Hong Kong
```

### CSV Sync Script
```bash
python3 sync_mtr_stations.py
```

---

**For complete user documentation, examples, and installation guide, please see the [main README.md](https://github.com/tomfong/hk-mtr-next-train-skill/blob/main/README.md)**

## Author

**Tom FONG** - [GitHub](https://github.com/tomfong)

Built with Usagi (Tom's OpenClaw Agent)

---

_SIMPLE DEV · SIMPLER WORLD_
