# VBO Format Specification

> **Late Brake Project Documentation**
>
> This document defines the parsing rules for VBO format files exported by RaceChrono Pro, and the mapping to Late Brake internal data format.
> VBO is a text log format exported by RaceChrono Pro, supporting GPS + multi-sensor data logging.

## 1. File Structure

VBO file is a text log exported by RaceChrono Pro, structured as follows:

1. **File Header**: Multiple lines of descriptive text, includes creation time, software version, etc.
2. **Field Definition Section**: After `[column names]` lists all data column names
3. **Data Section**: After `[data]` each line is one data sample, fields separated by spaces

When parsing, skip the file header, find the `[data]` section, then start parsing actual data lines.

## 2. Key Field Description

VBO stores coordinates in `DDMM.NNNNN` format, time in `HHMMSS.ss` format:

| Column Name | Type | Description |
|-------------|------|-------------|
| `time` | string | Time, format `HHMMSS.ss` |
| `lat` | float | Latitude, format `DDMM.NNNNN`, sign indicates north/south |
| `long` | float | Longitude, format `DDDMM.NNNNN`, sign indicates east/west |
| `velocity` | float | Speed, unit km/h |

**Other Fields**: VBO supports many optional fields (acceleration, gyro, OBD data, etc.), v1 does not parse these yet, can be extended in future iterations.

## 3. Conversion Rules

### 3.1 Coordinate Conversion

Original format: `DDMM.NNNNN` for latitude, `DDDMM.NNNNN` for longitude:

Conversion formula:
```
Decimal degrees = abs(original value) / 60
Preserve original sign in final result:
  - Latitude: positive = North, negative = South
  - Longitude: positive = East, negative = West
```

### 3.2 Time Conversion

Convert original time `HHMMSS.ss` to relative time (relative to first data point):

```python
# Example input: 053855.06 → 05 hours 38 minutes 55.06 seconds
hours = int(time_str / 10000)
minutes = int((time_str - hours * 10000) / 100)
seconds = time_str - hours * 10000 - minutes * 100
total_seconds = hours * 3600 + minutes * 60 + seconds
timestamp = total_seconds - start_total_seconds
```

### 3.3 Distance Calculation

Cumulative distance is calculated using GeographicLib geodesic formula between adjacent points and accumulated, consistent with NMEA parsing.

## 4. Internal Format Mapping

| VBO Field | Internal Field | Conversion Notes |
|-----------|----------------|------------------|
| time | timestamp | Convert to relative time (seconds) |
| lat | latitude | DDMM.NNNNN → decimal degrees |
| long | longitude | DDDMM.NNNNN → decimal degrees |
| velocity | speed | Already in km/h, use directly |
| (computed) | distance | Accumulate distance between adjacent coordinates, unit meters |

## 5. Error Handling

- Skip all lines before `[data]`
- Skip lines with insufficient number of fields
- Skip lines with parsing errors (numeric conversion failed)
- Don't crash, just skip bad lines
