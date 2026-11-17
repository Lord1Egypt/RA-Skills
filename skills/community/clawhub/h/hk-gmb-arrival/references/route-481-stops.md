# Route 481 — GMB Stops & Test Results

## Route Info
- **Route**: 481
- **Region**: NT (New Territories)
- **Direction 1**: Fo Tan (Shan Mei Street) → Tsuen Wan Market Street
- **Direction 2**: Tsuen Wan Market Street → Fo Tan (Shan Mei Street)
- **Route ID**: 2003209

## Stop Sequence (Direction 1: Fo Tan → Tsuen Wan)

| Seq | Stop ID | English Name | Chinese Name |
|-----|---------|--------------|--------------|
| 1 | 20002176 | Shan Mei Street Bus Terminus | 山尾街巴士總站 |
| 2 | 20002177 | Fo Tan Road opposite to Fo Tan Village | 火炭路火炭村對面 |
| 3 | 20002178 | Tsuen Wan Market Street | 荃灣街市街 |

## Stop Sequence (Direction 2: Tsuen Wan → Fo Tan)

| Seq | Stop ID | English Name | Chinese Name |
|-----|---------|--------------|--------------|
| 1 | 20002178 | Tsuen Wan Market Street | 荃灣街市街 |
| 2 | 20002179 | (intermediate) | — |
| 3 | 20002176 | Shan Mei Street Bus Terminus | 山尾街巴士總站 |

## Test Results (2026-09-17 15:50 HKT)

### Direction 1 (Fo Tan → Tsuen Wan)
```bash
python3 gmb_arrival.py getGMBArrival 481 1 "Shan Mei Street Bus Terminus" NT
```
```json
{
  "stopId": "20002176",
  "stopName": "Shan Mei Street Bus Terminus",
  "arrivals": ["15:55 HKT", "16:00 HKT", "16:06 HKT"]
}
```

```bash
python3 gmb_arrival.py getGMBArrival 481 1 "Tsuen Wan Market Street" NT
```
```json
{
  "stopId": "20002178",
  "stopName": "Tsuen Wan Market Street",
  "arrivals": ["15:49 HKT", "15:56 HKT", "16:04 HKT"]
}
```

### Direction 2 (Tsuen Wan → Fo Tan)
```bash
python3 gmb_arrival.py getGMBArrival 481 2 "Tsuen Wan Market Street" NT
```
```json
{
  "stopId": "20002178",
  "stopName": "Tsuen Wan Market Street",
  "arrivals": ["15:55 HKT", "16:05 HKT", "16:20 HKT"]
}
```

## Fuzzy Match Test
```bash
python3 gmb_arrival.py getGMBArrival 481 1 "Shan Mei" NT
```
```json
{
  "error": "Stop not found on this route.",
  "suggestions": {
    "Shan Mei Street Bus Terminus": "20002176"
  }
}
```

## Notes
- Stop names must match exactly (case-insensitive) or fuzzy match with cutoff 0.6
- Chinese names also work: `"山尾街巴士總站"`, `"荃灣街市街"`
- Route 481 has variants 481A, 481B, 481X — different service types