---
name: hk-mtr-next-train
description: Fast, reliable, and token-efficient Hong Kong MTR next-train ETA lookup with fuzzy station matching and bilingual output (zh-HK/en). Use for queries like next train / ETA / arrival time at station(s), including multi-station requests. 港鐵實時到站資訊，支援站名容錯、多線查詢、同方向多總站拆分等功能。
metadata: {"openclaw":{"emoji":"🚈","requires":{"bins":["python3"]},"keywords":["mtr", "hong kong mtr","mtr eta","next train","arrival time","real-time mtr","港鐵","香港鐵路","到站時間","下一班","列車"],"locale":["zh-HK","en"],"category":"transport","quality":{"latency":"1-5s","fallback":true,"fuzzyMatch":true,"multiRoute":true},"securityNotes":{"purpose":"Read-only ETA query + local cache refresh for HK MTR data","allowedDomains":["opendata.mtr.com.hk","rt.data.gov.hk"],"writeScope":["scripts/mtr_lines_and_stations.csv","scripts/__pycache__/"],"noSecrets":true}}}
user-invocable: true
---

# Hong Kong MTR Next Train (v1.0.1)

## Post-Install Recommendation

**Recommend to run once after install to sync station dictionary:**

```bash
cd {skill_dir}/scripts
python3 sync_mtr_stations.py
```

## Data Refresh Rule
- If user explicitly asks to update line/station data (新站、改名、線路更新), run:

```bash
cd {skill_dir}/scripts
python3 sync_mtr_stations.py
```

- If user did not ask for refresh, prefer local CSV for faster matching.

## Allowed Commands
- `python3 scripts/mtr_eta.py {STATION_NAME} {LINE_NAME(optional)} {LANG(optional)} {TO_STATION(optional)}`
- `python3 scripts/sync_mtr_stations.py`

## Safety Scope
- Allowed domains:
  - `https://rt.data.gov.hk/*`
  - `https://opendata.mtr.com.hk/*`
- Write scope (skill-local only):
  - `scripts/mtr_lines_and_stations.csv`
  - `scripts/__pycache__/`
- Do not access sensitive files outside skill directory.
- Never request/store/output secrets.

## Language Handling
- Chinese query → `TC`
- English/non-Chinese query → `EN`

## Features
- **Real-time ETA**: Live MTR train arrival times from DATA.GOV.HK
- **Fuzzy Matching**: Smart station name matching (e.g., "旺角" matches "Mong Kok")
- **Bilingual Output**: Traditional Chinese and English support
- **Token Efficient**: Local CSV cache minimizes API calls and token usage
- **Multi-line**: Supports all 10 MTR lines including Airport Express

## Usage
- Station + line: query that combo directly.
- Station only: query all lines serving that station.
- Line only: ask user which station (suggest 1–2 stations on that line).
- Neither line nor station: ask user which station.
- Line-station conflict: state mismatch, then show all lines at that station.

## Output Policy
- Never fabricate ETA values.
- Keep output concise, data-first.
- Global rule: for each direction, use API-available departures (up to 4) as source set, then split by destination if needed.
- Do not down-sample to only 1 train when more data exists.

### ETA wording
- Within 1 minute: `即將到達` / `Arriving`
- At 0 minute: `即將離開` / `Departing`
- Departed within 0–2 minutes: `已離開` / `Departed`
- Departed > 2 minutes: do not show

### Station output format (default)
- Title once:
  - `tc`: `🚈 {站名}的列車班次如下：`
  - `en`: `🚈 Next trains at {Station}:`
- Then one section per line: `{LineName} {LineEmoji}`
- One blank line between platform blocks
- Section divider between line sections: `--------------`
- If output contains multiple stations in one reply, add one extra station divider between station blocks: `====================`
- Block format:
  - `tc`:
    - `• {月台}號月台｜往{總站}`
    - `{ETA1}、{ETA2}、{ETA3}、{ETA4}`
  - `en`:
    - `• Platform {N} | to {Destination}`
    - `{ETA1}, {ETA2}, {ETA3}, {ETA4}`
- If platform changes within same destination block, include platform inline per ETA.

### Line emoji mapping
- AEL 機場快線: ✈️
- TCL 東涌線: 🟠
- TML 屯馬線: 🤎
- TKL 將軍澳線: 🟣
- EAL 東鐵線: 🩵
- SIL 南港島線: 🔰
- TWL 荃灣線: 🔴
- ISL 港島線: 🔵
- KTL 觀塘線: 🟢
- Fallback: 🚇

### Source footer
- Add one blank line, then:
  - `tc`: `資料來源：開放數據平台`
  - `en`: `Source: DATA GOV HK`

## Fallback
If no result after matching/retry:
- `tc`: `{站名} @ {線路}：尾班車已過或未有班次資料`
- `en`: `{Station} @ {Line}: Service hours have passed / No information found`

---

## Changelog

### 2026-03-22 · v1.0.1
- Update docs

### 2026-03-18 · v1.0.0
- First stable release