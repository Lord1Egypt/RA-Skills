# IoT & Smart Home

## Available Tools
- **openhue** — Philips Hue lights and scenes
- **eightctl** — Eight Sleep pod control
- **sonoscli** — Sonos speakers
- **blucli** — BluOS multi-room audio
- **camsnap** — RTSP/ONVIF security cameras

## Smart Home Patterns

### Lighting
- Scene control (movie mode, reading, sleep)
- Schedule-based automation
- Color temperature for circadian rhythm
- Motion-triggered lighting

### Climate
- Eight Sleep: temperature zones, heating/cooling schedules
- Thermostat integration via APIs
- Sleep optimization tracking

### Audio
- Multi-room sync (Sonos, BluOS)
- Alarm/wake-up routines
- Podcast/music scheduling

### Security
- Camera monitoring (RTSP/ONVIF)
- Motion detection alerts
- Door/window sensor integration
- Recording schedules

## Automation Routines

### Morning Routine
1. Gradual light increase (30min before wake)
2. Temperature adjustment
3. News briefing (TTS)
4. Calendar review
5. Coffee maker trigger

### Evening Routine
1. Lights dim to warm
2. Temperature cool for sleep
3. Doors lock check
4. Security cameras activate
5. Sleep mode engage

### Away Mode
1. Random light patterns
2. Camera monitoring active
3. Motion alerts enabled
4. Temperature setback

## Integration Points
- Cron schedules for time-based triggers
- Heartbeat checks for status monitoring
- Message notifications for alerts
- Voice control via TTS/STT

## Protocol Support
- HTTP REST APIs
- mDNS/SSDP discovery
- MQTT for real-time events
- Local-first (no cloud dependency when possible)
