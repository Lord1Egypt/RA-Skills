# Parking Spot Memory

**"Where did I park?" — answered in one command, because you logged it in 10 seconds before walking away.**

Circling level 4 of an airport garage at 1 AM is a memory-systems
failure, not a navigation one: parking markers are low-distinctiveness
codes, encoded while distracted, retrieved jet-lagged days later.
This tool is the capture ritual (level/row/section/photo/paid-until
at park time) plus instant retrieval with level-first search
guidance and a meter-expiry watch.

## What it does

- **park** — 10-second capture: location, level, row, section, plate,
  photo reference, paid-until, landmark notes
- **find** — full record with elapsed time + ordered search guidance
  (level first, elevator bank, row, photo check); `--location`
  filters history
- **expiry** — active paid sessions: minutes left (LOW flag <30),
  EXPIRED warnings with minutes overdue
- **list** — recent parking history and your per-location patterns

## Quick start

```bash
python3 scripts/parking_memory.py park --location "Airport T2 garage" \
    --level P3 --row D --section blue --photo IMG_4812.jpg \
    --paid-until "2026-10-19 17:16" --notes "near elevator 2"

python3 scripts/parking_memory.py find
```

```
Last parked: 2026-10-19 15:16 (0 min ago)
  location : Airport T2 garage
  level   : P3
  row     : D
  ...
Finding tips:
  - Head to level P3 first; elevator banks are usually near rows' start.
```

## Why it works

- **Say the marker out loud** (phonological encoding) + **one photo**
  with marker, car, and landmark in frame — three anchors, one shot
- **Log before leaving the car** — detail recall collapses within
  minutes of walking away
- **External storage beats recall** under context shift (tired,
  night, jet-lagged)
- Rental plate in the log turns "which white Corolla" into a lookup

## Install

No dependencies. Python 3.8+. Log is plain JSON (local, editable).

## License

MIT © Denis Voronin
