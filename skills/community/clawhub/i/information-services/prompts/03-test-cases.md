# Information Services — Test Cases

## Location Tests

### TC-01: GPS Location
- Input: service=location, method=gps
- Expected: lat/lon with accuracy < 20m
- Pass: confidence > 0.7

### TC-02: IP Fallback
- Input: service=location, no GPS available
- Expected: city-level coordinates
- Pass: confidence > 0.5

### TC-03: Triangulation
- Input: service=location, methods=[gps,wifi,ip]
- Expected: weighted centroid with combined confidence
- Pass: confidence > max(individual_sources)

## Weather Tests

### TC-04: Current Weather
- Input: service=weather, location="Shanghai"
- Expected: temp, conditions, humidity, wind
- Pass: all fields populated, confidence > 0.7

### TC-05: Forecast
- Input: service=weather, days=3
- Expected: 3-day forecast array
- Pass: array of 3 entries with date/temp/conditions

### TC-06: API Fallback
- Input: service=weather, primary API unreachable
- Expected: data from backup API
- Pass: same fields, possibly lower confidence

## Time Tests

### TC-07: System Time
- Input: service=time
- Expected: current datetime with timezone
- Pass: within 2s of actual time

### TC-08: NTP Precision
- Input: service=time, precision=high
- Expected: accuracy_ms < 50
- Pass: confidence > 0.95

### TC-09: Timezone Conversion
- Input: service=time, timezone="Europe/London"
- Expected: correct local time for timezone
- Pass: matches public time API

## Combined Tests

### TC-10: All Services
- Input: service=all
- Expected: location + weather + time in single response
- Pass: all three data objects present