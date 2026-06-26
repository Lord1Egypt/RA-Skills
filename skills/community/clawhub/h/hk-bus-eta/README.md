# 🚌 Hong Kong Bus ETA - Technical Reference

> ⚠️ **For complete documentation, please refer to the [main README.md](../README.md)**
> 
> This file contains technical reference information for the Hong Kong Bus ETA skill.

## Quick Links | 快速連結

- **[Main Documentation](../README.md)** - Complete user guide with installation, usage examples, and features
- **[SKILL.md](./SKILL.md)** - Technical specification for AI agents
- **[Scripts Directory](./scripts/)** - Python scripts for bus ETA queries

## Technical Overview | 技術概述

**Skill Name:** `hk-bus-eta`  
**Version:** 1.0.2  
**Last Updated:** 2026-03-14  
**Compatibility:** OpenClaw and compatible AI agents

### Core Components | 核心組件

1. **`eta.py`** - Main query script for bus ETA lookups
2. **`sync_bus_stops.py`** - Database initialization and sync script
3. **`bus_query.py`** - Internal API query module
4. **`bus_stops.db`** - SQLite database for bus stop data

### API Endpoints | API 端點

**Data Sources:**
- **KMB/LWB**: `https://data.etabus.gov.hk/v1/transport/kmb/`
- **Citybus**: `https://rt.data.gov.hk/v2/transport/citybus/`
- **Bus Stop Data**: `https://data.gov.hk/` (開放數據平台)

### Database Schema | 數據庫結構

The SQLite database (`bus_stops.db`) contains:
- `bus_stops` - Bus stop information with coordinates
- `stop_clusters` - Clustered stops within 50m radius
- `location_aliases` - Area name to coordinate mappings

## Script Usage | 腳本使用

### Main Query Script
```bash
python3 eta.py {ROUTE} {STOP_NAME} [LANGUAGE]
```

**Parameters:**
- `ROUTE`: Bus route number (e.g., "1A", "A21", "690")
- `STOP_NAME`: Bus stop name or area (e.g., "尖沙咀", "Central", "機場")
- `LANGUAGE`: Output language - `tc` (Traditional Chinese) or `en` (English)

**Examples:**
```bash
# Chinese output
python3 eta.py 1A 尖沙咀 tc

# English output  
python3 eta.py A21 Airport en
```

### Database Sync Script
```bash
python3 sync_bus_stops.py
```

**Purpose:** Downloads and builds local bus stop database from DATA.GOV.HK

## Technical Architecture | 技術架構

### Data Flow
1. **User Query** → Natural language or direct command
2. **Location Matching** → Fuzzy match stop name to coordinates
3. **API Query** → Parallel requests to KMB and Citybus APIs
4. **Data Processing** → Merge, filter, and format results
5. **Output** → Formatted ETA information

### Performance Features
- **Parallel API Calls**: Simultaneous KMB and Citybus queries
- **Local Cache**: SQLite database for fast stop lookups
- **Stop Clustering**: 50m radius grouping for duplicate stops
- **Fuzzy Matching**: Smart location association

## File Structure | 文件結構

```
hk-bus-eta/
├── README.md          # This file (technical reference)
├── SKILL.md           # AI agent specification
└── scripts/
    ├── eta.py         # Main ETA query script
    ├── sync_bus_stops.py  # Database sync script
    └── bus_query.py   # Internal API module
```

## Development Notes | 開發筆記

### Key Dependencies
- `requests` - HTTP API calls
- `sqlite3` - Local database
- `concurrent.futures` - Parallel processing

### Error Handling
- **API Timeouts**: 10-second timeout for API requests
- **Fallback Messages**: "尾班車已過或未有班次資料" (Chinese) / "Service hours have passed" (English)
- **Database Recovery**: Auto-rebuild on corruption detection

### Performance Metrics
- **Initial Setup**: 1-2 minutes (20MB download)
- **Query Time**: 2-5 seconds typical
- **Database Size**: ~20MB (compressed), ~50MB (uncompressed)
- **Stop Count**: 2250+ bus stops cached

---

**For complete user documentation, examples, and installation guide, please see the [main README.md](../README.md)**
- Multi-name support
- Terminus marking
- Auto background sync (7-day cycle) (BETA)
- 30s timeout enforcement

## Author

**Tom FONG** - [GitHub](https://github.com/tomfong)

Built with Mr. Usagi (Tom's OpenClaw Agent)

---

_SIMPLE DEV, SIMPLER WORLD_
