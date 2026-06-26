# iNTERCEPT API Reference — Detailed Endpoints

## Authentication & Session

### POST /login
Auth required: No  |  CSRF: Yes
Body: `username=<str>&password=<str>&csrf_token=<str>`

### GET /logout
Clears session.

## Device & System

### GET /devices/status
Returns JSON array of detected SDR devices with capabilities (freq range, sample rates, gain steps, bias-t support).

### POST /devices/debug
Returns detailed device debug info including USB tree, permissions, and driver state.

### GET /health
Returns `{"status": "ok"}` if the server is running.

### GET /dependencies
JSON mapping of tool names to version strings. Shows which SDR tools are installed (rtl_fm, rtl_433, dump1090, etc.).

### GET /system/metrics
CPU, memory, and disk usage via psutil.

### GET /system/sdr_devices
Simplified device list.

## Settings

### POST /settings
Auth: Required  |  CSRF: Yes
Body (JSON):
```json
{"observer_lat": 33.3246, "observer_lon": -96.7844}
```

### GET /settings/observer-location
Returns current observer coordinates.

### GET /settings/<key>
Read a single setting by key.

## ADS-B

### GET /adsb/start
Starts dump1090 in the background. Returns status immediately.

### POST /adsb/status
Auth: Required | CSRF: Yes
Returns JSON with running state, process info, aircraft count.

### POST /adsb/stop
Auth: Required | CSRF: Yes
Sends SIGTERM to dump1090.

### GET /adsb/aircraft
Returns all tracked aircraft as JSON array. Each entry includes hex, flight, squawk, altitude, speed, lat, lon, track.

### GET /adsb/stream
SSE stream emitting `{"type":"aircraft","data":{...}}` events.

### POST /adsb/dashboard
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"sessions": [12345], "time_range": "24h", "filter": {}}
```

### POST /adsb/history
Auth: Required | CSRF: Yes
Body (JSON): `{"limit": 1000, "offset": 0, "filter": {}}`

### GET /adsb/tools
Returns installed ADS-B binary paths.

## ACARS

### GET /acars/start
Starts acarsdec.

### GET /acars/stop
Graceful stop.

### GET /acars/messages
JSON array of decoded ACARS messages. Each has time, freq, label, block_id, text, tail.

### GET /acars/stream
SSE: new ACARS messages as they arrive.

### POST /acars/frequencies
Auth: Required | CSRF: Yes
Body (JSON): `{"frequencies": [131.725, 131.550, 130.025]}`

## Weather Satellite

### POST /weather-sat/start
Auth: Required | CSRF: Yes
Body (JSON):
```json
{
    "frequency": 137.9125,
    "satellite": "NOAA 19",
    "gain": 49.6,
    "duration": 900
}
```

### POST /weather-sat/passes
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"hours": 48}
```
Returns upcoming satellite passes with AOS/LOS times, max elevation, direction.

### POST /weather-sat/images
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"satellite": "NOAA 19", "limit": 20}
```
Returns list of decoded images.

## APRS

### GET /aprs/start
Starts direwolf.
### GET /aprs/status
Returns state and station count.
### GET /aprs/stop
Stops direwolf.
### GET /aprs/data
All APRS position reports.

## Morse/CW Decoder

### GET /morse/start
Starts rtl_fm piped to multimon-ng MORSE_CW.

### POST /morse/calibrate
Auth: Required | CSRF: Yes
Auto-tunes tone threshold and bandwidth.

## TSCM Sweep

### GET /tscm/sweep/start
Starts frequency sweep across configured bands.

### POST /tscm/baseline/compare
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"baseline_id": 1, "sweep_id": 2}
```

## WiFi

### POST /wifi/monitor
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"interface": "wlan0"}
```
Enables monitor mode on the interface.

### POST /wifi/v2/scan/start
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"interface": "wlan0", "duration": 30, "channel_hop": true}
```

## Drone Detection

### POST /drone/start
Auth: Required | CSRF: Yes
Body (JSON):
```json
{"rtlsdr": true, "wifi": true, "ble": true}
```
