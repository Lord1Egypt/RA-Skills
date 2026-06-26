# Location Service — Detailed Specifications

> Part of information-services skill.

---

## 1. Supported Methods

| Method | Accuracy | Use Case | API Key Required |
|--------|----------|----------|-----------------|
| **GPS** | 3-10m | Outdoor, navigation | No |
| **System** | 10m–1km | Indoor/outdoor, OS-managed | No |
| **IP** | 1-50km | City-level, quick detection | No |
| **WiFi** | 10-100m | Indoor, urban environments | Optional |
| **Cellular** | 100m-3km | Rural, GPS-denied | Optional |
| **Triangulated** | Weighted centroid | Multi-method fusion | No |

## 2. Triangulation Algorithm

When multiple methods return results:
1. Collect coordinates from each successful method
2. Weight by inverse variance (accuracy-based weighting)
3. Compute weighted centroid as final position
4. Estimate combined accuracy from residual dispersion
5. Report confidence score (0–100%)

### Output Format
```json
{
  "latitude": 39.9042,
  "longitude": 116.4074,
  "accuracy_meters": 15,
  "confidence": 0.92,
  "method": "triangulated",
  "sources": {
    "gps": {"lat": 39.9045, "lon": 116.4071, "accuracy": 5, "weight": 0.6},
    "wifi": {"lat": 39.9039, "lon": 116.4078, "accuracy": 30, "weight": 0.3},
    "ip": {"lat": 39.9042, "lon": 116.4074, "accuracy": 5000, "weight": 0.1}
  },
  "timestamp": "2026-04-26T10:30:00Z"
}
```

## 3. Command Interface

```bash
# Get location using all available methods
python scripts/locate.py

# Use specific method(s)
python scripts/locate.py --method gps
python scripts/locate.py --method system,ip,wifi

# Output format
python scripts/locate.py --format json
python scripts/locate.py --format text
```

## 4. Optional API Keys

For enhanced accuracy, configure in environment:
```bash
export GOOGLE_GEOLOCATION_API_KEY="your-key"
export MLS_API_KEY="your-key"
export UNWIRED_API_KEY="your-key"
```

## 5. Platform Notes

- **Windows:** GeoCoordinateWatcher via PowerShell (WiFi + IP + GPS fusion)
- **macOS:** CoreLocation via locationd daemon
- **Linux:** GeoClue2 via D-Bus (Wi-Fi + cell fusion)