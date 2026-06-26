---
name: metdata-nasa-access
description: Fetch NASA POWER meteorological data for wind and solar energy, output Excel files.
homepage: https://power.larc.nasa.gov
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["curl"],"python":["openpyxl"]}}}
---

# MetData-NASA-Access

Fetch NASA POWER meteorological data for wind and solar energy analysis, output structured Excel files.

## Trigger

User provides a location name or coordinates, e.g.:
- "上海市闵行区申虹路虹桥天地3号楼"
- "31.1932, 121.3111"
- "西安"

## Workflow

### Step 1: Resolve Coordinates

If user provides a location name, resolve to lat/lon using Nominatim geocoding:

```bash
curl -s -G "https://nominatim.openstreetmap.org/search" \
  --data-urlencode "q=<LOCATION>" \
  --data-urlencode "format=json" \
  --data-urlencode "limit=1" \
  -H "User-Agent: MetData-NASA-Access/1.0"
```

Parse JSON response to get `lat` and `lon`. If user already provides coordinates, skip this step.

### Step 2: Run the Script

Use the Python script at `scripts/fetch_metdata.py`:

```bash
python3 scripts/fetch_metdata.py \
  --lat <LAT> \
  --lon <LON> \
  --start <YEAR> \
  --end <YEAR> \
  --output <OUTPUT_PATH>
```

**Parameters:**
- `--lat`, `--lon`: Coordinates (required)
- `--start`, `--end`: Year range (default: 2016, 2017)
- `--output`: Excel output path (default: `~/.openclaw/workspace/output/metdata/`)
- `--params`: Comma-separated custom parameter list (default: wind+ solar defaults)
- `--granularity`: `monthly`, `daily`, `climatology`, or `all` (default: `all`)

### Step 3: Report to User

Confirm the file path and summarize key findings (e.g., average wind speed, average solar irradiance).

## Default Parameters

**Solar (PV):** ALLSKY_SFC_SW_DWN, CLRSKY_SFC_SW_DWN, ALLSKY_TOA_SW_DWN, ALLSKY_SFC_LW_DWN, KT, KT_CLEAR

**Temperature:** T2M, T2M_MAX, T2M_MIN, T10M, T10M_MAX, T10M_MIN, TS, TS_MAX, TS_MIN

**Humidity:** RH2M, QV2M, T2MDEW

**Wind:** WSC, WS50M, WS50M_MAX, WS50M_MIN, WS10M, WS10M_MAX, WS10M_MIN, WD50M, WD10M

**Pressure:** PSC, PS

**Other:** PRECTOT, TQV, FROST_DAYS

## Output Format

Excel with sheets:
- **月度数据**: Monthly averages
- **日均数据**: Daily values
- **气候平均数据**: 20-year climatological means (2001-2020)

## Notes

- NASA POWER data uses MERRA-2 reanalysis, ~0.5° resolution
- `community=RE` = Renewable Energy application
- Temperature: °C, Wind: m/s, Radiation: kWh/m²/day
- Time standard: LST (Local Standard Time)
- For monthly data, row "201613" = annual mean within that year
- For climatology, months are JAN-DEC + ANN (annual mean)
- Fetching all 3 granularities with 32 params takes ~5-8 minutes
- Use `--granularity monthly` for faster results
