---
name: intercept-sdr
description: Control and query the iNTERCEPT SDR signal intelligence platform via its REST API. Use when the user wants to check SDR device status, start/stop signal decoders (ADS-B, ACARS, POCSAG pager, rtl_433, weather satellites, APRS, AIS, SSTV, VDL2, DSC, Morse code, sub-GHz, TSCM sweeps, drone detection, WiFi/BT scanning, GPS, Meshtastic, space weather), retrieve decoded messages, check system health, manage recordings, view satellite passes, or perform any SDR/SIGINT operation through iNTERCEPT. Also use for starting/stopping/listening to audio streams, managing the frequency scanner, controlling remote agents, and checking dependencies.
version: 1.0.0
---

# iNTERCEPT — Signal Intelligence API

Control a running iNTERCEPT SDR platform instance through its REST API. The platform is a web-based SDR signal intelligence suite supporting RTL-SDR and HackRF.

## Connection

The iNTERCEPT server runs locally by default. Read the base URL from the `INTERCEPT_BASE_URL` environment variable, or default to `http://localhost:5050`.

Authentication is session-based. To make API calls:
1. `POST /login` with `username=admin&password=admin` and a CSRF token
2. Grab the CSRF token from the login page HTML: `grep -oP 'name="csrf_token"[^>]*value="\K[^"]+'`
3. Use the session cookie for subsequent requests

For quick/diagnostic calls that don't need auth, use `/devices/status`, `/health`, `/dependencies`, `/system/sdr_devices`.

## Quick Start

### Check SDR hardware
```
GET /devices/status   → JSON list of detected SDRs
GET /health           → System health
GET /dependencies     → Installed tool versions
```

### Start a decoder (pattern)
```
GET /<module>/start   → Starts the decoder, returns status
GET /<module>/status  → Current decoder state
GET /<module>/stop    → Stops gracefully
GET /<module>/stream  → SSE stream of decoded data
```

## Core Capabilities

### 1. Device & System Management

Check what SDR hardware is connected:
```
GET /devices/status     → SDR device list with capabilities
GET /devices/debug      → Detailed device debug info
GET /system/sdr_devices → SDR device listing
GET /system/metrics     → CPU/memory/disk metrics
GET /health             → Quick health check
GET /dependencies       → All installed tool versions
```

Set observer location:
```
POST /settings  JSON: {"observer_lat": 33.3246, "observer_lon": -96.7844}
GET  /settings/observer-location
```

Kill all running processes:
```
POST /killall
```

### 2. ADS-B (Aircraft Tracking)

```
GET  /adsb/start                         → Start dump1090
POST /adsb/status                        → Current state
POST /adsb/stop                          → Stop decoder
GET  /adsb/stream                        → SSE: aircraft positions
GET  /adsb/aircraft                      → All tracked aircraft
POST /adsb/dashboard      JSON: filters  → Dashboard data
POST /adsb/history        JSON: filters  → Historical data
GET  /adsb/tools                         → Installed ADS-B tools
```

### 3. ACARS (Aircraft Datalink)

```
GET  /acars/start                        → Start acarsdec
GET  /acars/status                       → Current state
GET  /acars/stop                         → Stop decoder
GET  /acars/messages                     → All decoded messages
GET  /acars/stream                       → SSE: new messages
POST /acars/frequencies   JSON: freqs[]  → Set frequencies
GET  /acars/clear                        → Clear message buffer
```

### 4. POCSAG/FLEX (Pager Decoding)

```
POST /start               JSON: {"mode": "pocsag"}
GET  /status                            → Decoder state
POST /stop                             → Stop decoder
POST /stream                            → SSE: decoded pages
```

### 5. rtl_433 (433MHz Sensors)

```
GET  /start_sensor                      → Start rtl_433
GET  /status                            → Decoder state
POST /stop_sensor                       → Stop decoder
GET  /stream_sensor                     → SSE: sensor data
GET  /sensor/rssi_history               → RSSI records
POST /sensor/status                     → Status check
```

### 6. Weather Satellites (NOAA/Meteor)

```
POST /weather-sat/start    JSON: freq, gain, etc.  → Start capture
GET  /weather-sat/status                             → State/queue
POST /weather-sat/stop                               → Stop
POST /weather-sat/stream                             → SSE progress
POST /weather-sat/passes                             → Upcoming passes
POST /weather-sat/images                             → List received images
GET  /weather-sat/schedule/status                    → Scheduler status
GET  /weather-sat/schedule/enable                    → Enable scheduler
GET  /weather-sat/schedule/disable                   → Disable scheduler
GET  /weather-sat/satellites                         → Tracked satellites
```

### 7. APRS (Amateur Packet Radio)

```
GET  /aprs/start                        → Start direwolf
GET  /aprs/status                       → State
GET  /aprs/stop                         → Stop
GET  /aprs/data                         → Position reports
GET  /aprs/stations                     → All stations
GET  /aprs/stream                       → SSE
GET  /aprs/frequencies                  → Frequencies used
```

### 8. AIS (Vessel Tracking)

```
POST /ais/start                         → Start decoder
POST /ais/status                        → State
POST /ais/stop                          → Stop
POST /ais/vessels                       → Tracked vessels
POST /ais/dashboard                     → Dashboard summary
POST /ais/stream                        → SSE
```

### 9. SSTV (Slow-Scan TV)

```
PUT  /sstv-general/start                → Start decoder
POST /sstv-general/status               → State
POST /sstv-general/stop                 → Stop
GET  /sstv-general/images               → Decoded images
POST /sstv-general/stream               → SSE
GET  /sstv/images                       → ISS SSTV images
POST /sstv/decode-file                  → Decode uploaded file
```

### 10. Morse/CW Decoder

```
GET  /morse/start                       → Start CW decode
GET  /morse/status                      → State
GET  /morse/stop                        → Stop
POST /morse/stream                      → SSE
POST /morse/calibrate                   → Auto-calibrate
POST /morse/decode-file                 → Decode audio file
```

### 11. VDL2 (VHF Data Link Mode 2)

```
POST /vdl2/start                        → Start dumpvdl2
GET  /vdl2/status                       → State
PATCH /vdl2/stop                        → Stop
GET  /vdl2/messages                     → Decoded messages
GET  /vdl2/stream                       → SSE
GET  /vdl2/clear                        → Clear buffer
```

### 12. DSC (VHF Distress)

```
GET  /dsc/start                         → Start decoder
GET  /dsc/status                        → State
GET  /dsc/stop                          → Stop
GET  /dsc/messages                      → All messages
GET  /dsc/stream                        → SSE
GET  /dsc/alerts                        → Distress alerts
```

### 13. Sub-GHz Analyzer

```
GET  /subghz/receive/start              → Start capture
GET  /subghz/receive/stop               → Stop
POST /subghz/status                     → State
GET  /subghz/captures                   → Saved captures
GET  /subghz/sweep/start                → Frequency sweep
GET  /subghz/sweep/stop                 → Stop sweep
POST /subghz/stream                     → SSE
PUT  /subghz/decode/start               → Decode capture
```

### 14. TSCM (Counter-Surveillance)

```
GET  /tscm/sweep/start                  → Start RF sweep
GET  /tscm/sweep/status                 → Sweep state
GET  /tscm/sweep/stop                   → Stop sweep
GET  /tscm/capabilities                 → Available features
POST /tscm/baselines                    → List baselines
GET  /tscm/baseline/record              → Record baseline
GET  /tscm/baseline/status              → Recording state
POST /tscm/baseline/compare             → Compare sweeps
GET  /tscm/devices                      → Detected devices
GET  /tscm/threats                      → Detected threats
POST /tscm/findings                    → Search findings
```

### 15. WiFi Scanning & Recon

```
GET  /wifi/interfaces                   → Available interfaces
POST /wifi/monitor     JSON: iface      → Enable monitor mode
GET  /wifi/scan/start                   → Start scan
GET  /wifi/scan/stop                    → Stop scan
POST /wifi/networks                    → Visible networks
POST /wifi/v2/scan/start               → Advanced scan
POST /wifi/v2/scan/status              → Scan state
GET  /wifi/v2/networks/<bssid>         → Network details
GET  /wifi/v2/clients                  → Connected clients
GET  /wifi/stream                       → SSE results
```

### 16. Bluetooth Scanning

```
GET  /bt/interfaces                     → Available adapters
GET  /bt/scan/start                     → Start discovery
GET  /bt/scan/stop                      → Stop
POST /bt/stream                        → SSE results
POST /bt/devices                       → Discovered devices
GET  /api/bluetooth/devices            → Device details
GET  /api/bluetooth/scan/start         → API-based scan
```

### 17. Drone Detection

```
POST /drone/start                       → Start detection
POST /drone/status                      → State
GET  /drone/stop                        → Stop
GET  /drone/stream                      → SSE contacts
GET  /drone/contacts                    → Detected drones
```

### 18. Satellite Tracking

```
GET  /satellite/predict                 → Pass predictions
GET  /satellite/position                → Current positions
GET  /satellite/tracked                 → Tracked satellites
POST /satellite/tracked/<norad_id>     → Add/remove satellite
GET  /satellite/update-tle              → Refresh TLE data
GET  /satellite/celestrak/<category>   → Fetch TLEs
POST /satellite/dashboard              → Dashboard data
```

### 19. Meshtastic (LoRa Mesh)

```
POST /meshtastic/start                  → Connect to device
GET  /meshtastic/status                 → Connection state
GET  /meshtastic/stop                   → Disconnect
GET  /meshtastic/nodes                  → Mesh nodes
GET  /meshtastic/messages               → Received messages
POST /meshtastic/send                   → Send message
POST /meshtastic/stream                 → SSE
GET  /meshtastic/channels               → Channel config
```

### 20. Space Weather

```
POST /space-weather/data                → Solar/geomagnetic data
GET  /space-weather/image/<key>         → SDO/NASA imagery
GET  /space-weather/prefetch-images     → Cache images
```

### 21. Spy Stations & Signal ID

```
POST /spy-stations/stations            → Query number stations
GET  /spy-stations/filters             → Available filters
POST /signalid/sigidwiki               → Identify signal
```

### 22. GPS

```
GET  /gps/status                        → GPS receiver state
GET  /gps/devices                       → Available devices
GET  /gps/position                      → Current position
GET  /gps/satellites                    → Satellites in view
GET  /gps/auto-connect                  → Auto-detect GPS
POST /gps/stream                        → SSE position updates
```

### 23. Audio / Receiver / Scanner

```
GET  /receiver/audio/start              → Start audio
GET  /receiver/audio/stop               → Stop
POST /receiver/audio/status             → State
GET  /receiver/audio/probe              → Probe audio devices
POST /receiver/scanner/start            → Frequency scanner
GET  /receiver/scanner/status           → Scanner state
GET  /receiver/scanner/pause            → Pause scanning
POST /receiver/scanner/skip             → Skip frequency
GET  /receiver/waterfall/start          → Start waterfall
PUT  /receiver/waterfall/stop           → Stop waterfall
GET  /receiver/presets                  → Frequency presets
```

### 24. Recordings

```
GET  /recordings                        → List all recordings
GET  /recordings/<session_id>          → Session details
GET  /recordings/<session_id>/download → Download IQ file
GET  /recordings/<session_id>/events   → Session events
GET  /recordings/start                  → Start recording
GET  /recordings/stop                   → Stop recording
```

### 25. Remote Agents

```
GET  /controller/agents                 → List remote agents
GET  /controller/agents/health          → Agent health
GET  /controller/monitor                → Agent monitor dashboard
POST /controller/agents/<id>/<mode>/data    → Agent data
GET  /controller/agents/<id>/<mode>/start   → Start agent module
GET  /controller/agents/<id>/<mode>/status  → Agent module status
GET  /controller/agents/<id>/<mode>/stop    → Stop agent module
```

### 26. Utility Meters (rtlamr)

```
GET  /start_rtlamr                      → Start meter reading
POST /stop_rtlamr                       → Stop
GET  /stream_rtlamr                     → SSE: meter data
```

### 27. Radiosonde (Weather Balloons)

```
POST /radiosonde/start                  → Start decoder
GET  /radiosonde/status                 → State
POST /radiosonde/stop                   → Stop
POST /radiosonde/balloons              → Active balloons
POST /radiosonde/stream                 → SSE
```

### 28. WebSDR (KiwiSDR Remote)

```
GET  /websdr/receivers                  → List remote KiwiSDRs
GET  /websdr/receivers/nearest          → Nearest receiver
GET  /ws/kiwi-audio                     → WebSocket audio stream (WebSocket, not HTTP)
```

## Stream Handling

Several endpoints return SSE (Server-Sent Events) streams. The stream path is typically `/<module>/stream`.

Use `curl -N http://localhost:5050/<module>/stream` for long-lived SSE connections.

WebSocket streams use `<ws://localhost:5050/ws/...>` for waterfall and satellite data.

## Common Patterns

### Start, check, stop workflow
```bash
# 1. Start decoder
curl "http://localhost:5050/<module>/start"

# 2. Wait and verify
curl "http://localhost:5050/<module>/status"

# 3. Read data
curl "http://localhost:5050/<module>/data"

# 4. Stop when done
curl "http://localhost:5050/<module>/stop"
```

### Watch stream with timeout
```bash
curl -N --max-time 30 "http://localhost:5050/<module>/stream"
```

## Auth Note

For POST endpoints that require CSRF + session auth (login), the skill should:
1. Fetch login page to get CSRF token
2. POST login with credentials
3. Use cookie jar for all subsequent requests
