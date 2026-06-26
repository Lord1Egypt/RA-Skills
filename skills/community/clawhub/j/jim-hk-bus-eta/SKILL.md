---
name: hk-bus-eta
description: Query Hong Kong bus ETA/stop data and MTR heavy rail ETA from natural-language transport questions using official KMB/LWB, Citybus, and MTR open-data endpoints. Use when the user asks in Cantonese, Chinese, or English things like「74X 幾多分鐘後喺九龍灣有車」「A41 去機場而家幾時到青衣站」「城巴 20 喺啟德幾耐到」「火炭站去金鐘方向幾點有車」「金鐘去北角下一班港島線幾時」or any message that combines a bus route with a stop/place, or an MTR station with a destination/direction/ETA intent.
---

# HK Bus ETA / MTR ETA

Use the bundled script to answer Hong Kong bus route + stop queries and MTR heavy rail station + direction queries quickly and consistently.

## Quick start

Run the bundled script from the skill directory:

### Bus

Legacy bus invocation still works:

```bash
python3 scripts/hk_bus_eta.py <route> <stop-keyword>
```

Equivalent explicit subcommand:

```bash
python3 scripts/hk_bus_eta.py bus <route> <stop-keyword>
```

Examples:

```bash
python3 scripts/hk_bus_eta.py 74X 九龍灣
python3 scripts/hk_bus_eta.py bus A41 青衣 --operator lwb
python3 scripts/hk_bus_eta.py bus 20 啟德 --operator citybus
python3 scripts/hk_bus_eta.py bus 20 "Kai Tak" --operator citybus --direction outbound
python3 scripts/hk_bus_eta.py bus 74X 九龍灣 --direction outbound
python3 scripts/hk_bus_eta.py bus 74X 九龍灣 --json
```

### MTR heavy rail

Structured station-to-station query:

```bash
python3 scripts/hk_bus_eta.py mtr <origin-station> <destination-station>
```

Natural-language prompt parsing:

```bash
python3 scripts/hk_bus_eta.py mtr-text "火炭站去金鐘方向幾點有車"
```

Examples:

```bash
python3 scripts/hk_bus_eta.py mtr 火炭 金鐘
python3 scripts/hk_bus_eta.py mtr 火炭 金鐘 --line EAL
python3 scripts/hk_bus_eta.py mtr-text "火炭站去金鐘方向幾點有車"
python3 scripts/hk_bus_eta.py mtr-text "金鐘去北角下一班港島線幾時"
python3 scripts/hk_bus_eta.py mtr-text "荃灣站往中環方向有冇車" --json
```

Or use an absolute path rooted at the installed skill folder if needed.

## Extraction workflow

### A. Bus queries

1. Extract the route first.
   - Examples: `74X`, `A41`, `20`, `NA31`.
2. Extract the stop or area keyword next.
   - Accept stop names, stations, estates, landmarks, districts, malls, piers, airports, hospitals, short area names, or a shared live location / latitude+longitude pair.
   - Treat messages like `74X 九龍灣幾耐到`, `A41 青衣站有冇車`, `城巴20啟德幾時到` as route + place queries.
   - If the user provides coordinates or a live location, prefer using that location to identify the nearest relevant stop on the route instead of guessing from a broad area name.
3. Infer operator if the user says it explicitly.
   - `九巴` → `--operator kmb`
   - `龍運` / `Long Win` → `--operator lwb`
   - `城巴` / `Citybus` → `--operator citybus`
   - If the user does not say, default to KMB. If the route obviously looks like a Citybus-only route or the first attempt fails, retry with `--operator citybus`.
4. If the user hints at direction or destination, pass it through.
   - `去機場`, `往尖沙咀`, `outbound`, `返去` often imply direction disambiguation.
   - Use `--direction outbound` or `--direction inbound` when the user's wording clearly prefers one side.
5. If a live location or latitude+longitude pair is available, resolve the nearest stop candidates on the target route first.
   - Compare the shared coordinates against stops on the requested route and preferred direction.
   - Prefer the physically nearest stop that matches the intended destination direction.
   - Tell the user which stop was selected and approximately how far away it is when that helps.
6. Run the bus query.
7. If multiple stop matches appear, summarize each clearly with operator, direction, stop name, sequence, and destination.
8. Report ETA in natural language, usually in minutes first.
9. If no match appears, say so and ask for a more specific stop name, estate, station, direction, or live location.

### B. MTR heavy rail queries

1. Detect that the prompt is station + destination/direction based, not bus-route based.
   - Strong triggers: `X站去Y方向`, `X去Y下一班`, `往Y有冇車`, `X站到Y幾點有車`.
2. Extract the origin station and target station/direction anchor.
   - Examples:
     - `火炭站去金鐘方向幾點有車` → origin `火炭`, target `金鐘`
     - `金鐘去北角下一班港島線幾時` → origin `金鐘`, target `北角`, line hint `ISL`
     - `荃灣站往中環方向有冇車` → origin `荃灣`, target `中環`
3. If the message names a line, pass it as `--line`.
   - Common mappings:
     - `東鐵線` → `EAL`
     - `港島線` → `ISL`
     - `荃灣線` → `TWL`
     - `觀塘線` → `KTL`
     - `將軍澳線` → `TKL`
     - `屯馬線` → `TML`
     - `東涌線` → `TCL`
     - `機場快綫` / `Airport Express` → `AEL`
     - `南港島線` → `SIL`
     - `迪士尼線` → `DRL`
4. Prefer `mtr-text` when the user phrased the request naturally and it fits the built-in patterns.
5. If parsing feels ambiguous, use `mtr <origin> <destination>` directly instead of guessing from a messy sentence.
6. The script resolves line/station mapping from the official MTR lines-and-stations CSV, then filters trains from the official MTR schedule endpoint that actually pass the requested target station.
7. If multiple line candidates remain, list them instead of pretending certainty.

## Reporting guidance

- Prefer a concise answer like `74X 喺九龍灣下一班大約 3 分鐘後到。` or `火炭去金鐘方向下一班東鐵線大約 2 分鐘後到，4 號月台。`
- If there are multiple likely matches, list them instead of guessing.
- If there is no ETA, say that clearly rather than implying no service.
- Use `--json` only when structured output is easier for follow-up processing.

## Operator / data-source notes

- `kmb`: official `data.etabus.gov.hk` KMB endpoints.
- `lwb`: handled through the same KMB-family endpoint structure used by Long Win routes in the KMB dataset.
- `citybus`: official `rt.data.gov.hk/v2/transport/citybus` endpoints.
- `mtr`: official `rt.data.gov.hk/v1/transport/mtr/getSchedule.php` endpoint plus the official MTR lines/stations CSV from `opendata.mtr.com.hk`.

## Matching behavior

- Bus stop matching is flexible substring/token matching against Traditional Chinese, Simplified Chinese, and English stop names.
- If the user shares live location coordinates, bus-stop selection should prefer distance-to-stop over fuzzy text matching alone.
- MTR station matching is flexible against Chinese name, English name, and station code.
- For MTR, destination matching is by path logic, not just terminal-code equality: trains are kept only if their displayed destination would carry the passenger past the requested target station on that line.
- If the user gives only a broad area or a very ambiguous station name, refine from the returned candidates or from shared coordinates.

## Scope and limitations

- Bus coverage here remains KMB, Long Win, and Citybus only.
- MTR coverage added here is heavy rail only. Light Rail, buses branded under MTR, and airport/feeder bus services are out of scope.
- `mtr-text` handles common natural-language forms like `X站去Y方向幾點有車`, `X去Y下一班`, and `X往Y有冇車`; unusual phrasings may need manual extraction with `mtr <origin> <destination>`.
- Very ambiguous interchange stations or cross-line phrasing may return multiple candidates and need clarification.
- The script does not plan multi-leg journeys; it answers next-train ETA for a specific origin station toward a target station on a line that passes both.

## scripts/

- `scripts/hk_bus_eta.py` — query KMB/LWB/Citybus bus ETA, and MTR heavy rail ETA using either structured station arguments or a short natural-language MTR prompt.
