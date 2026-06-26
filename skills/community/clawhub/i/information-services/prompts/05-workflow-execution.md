# Information Services — Workflow Execution

## Workflow: Get Current Location Weather

### Step 1: Get Location
```
1. Attempt GPS (--method gps --timeout 30)
2. If GPS fails, try System (--method system --timeout 20)
3. If System fails, use IP geolocation
4. Return coordinates with confidence score
```

### Step 2: Get Weather
```
1. Query wttr.in with coordinates
2. If timeout, retry with open-meteo
3. If all fail, return error WEATHER_FAILED
4. Return weather data with source and confidence
```

### Step 3: Combine & Report
```
1. Return { location, weather, confidence } object
2. If either service failed, use partial data with lower confidence
3. Report confidence score for transparency
```

## Workflow: Time Check with NTP Precision

### Step 1: System Clock
```
1. Read local system time (instant)
2. Record as baseline
3. Proceed to NTP if precision requested
```

### Step 2: NTP Query
```
1. Query NTP server (pool.ntp.org)
2. Calculate round-trip latency
3. Compute adjusted time
4. Compare with system time
```

### Step 3: Score & Return
```
1. If NTP successful: confidence = 0.98
2. If NTP fails: confidence = 0.85 (system only)
3. Return time object with all metadata
```

## Workflow: Handle No Sources Available

### Step 1: Log the failure
```
1. Record which sources were attempted
2. Note the failure reason (no hardware, no network, etc.)
```

### Step 2: Return error with context
```
1. Set confidence = 0
2. Include error code and message
3. Suggest manual input as recovery
4. Do NOT make up or estimate data
```