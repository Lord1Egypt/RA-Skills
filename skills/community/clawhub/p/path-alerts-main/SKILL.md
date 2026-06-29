---
name: path-alerts
description: Get real-time NJ PATH train service alerts, delays, status updates, and live arrival times. Monitors official Port Authority alerts feed and GTFS-Realtime data.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: gtfs-realtime-bindings
    emoji: "🚊"
    homepage: https://github.com/LiamSx45/openclaw-path-alerts
---

# NJ PATH Alerts Skill

Get real-time service alerts, delays, and live arrival times for NJ PATH trains.

## Capabilities

- **Service Alerts**: Real-time disruptions from Port Authority
- **Live Arrivals**: Next train times via GTFS-Realtime
- **Line Status**: Check all 4 PATH lines
- **Station Info**: Arrivals for all 13 stations

## Usage

The skill activates when you ask about PATH trains, delays, or service status.

**Examples:**
- "Are there PATH delays?"
- "When's the next train at Hoboken?"
- "Is the HOB-33 running?"
- "PATH status"

### Programmatic Usage

**Check current alerts:**
```javascript
import { getAlertsMessage } from 'nj-path-alerts';
const message = await getAlertsMessage();
```

**Get live arrivals:**
```javascript
import { getStationArrivals } from 'nj-path-alerts';
const arrivals = await getStationArrivals('hoboken');
```

**Check specific line:**
```javascript
const hobokenAlerts = await getAlertsMessage('HOB-33');
```

## Data Sources

- **Alerts**: Port Authority Everbridge API (official)
- **Arrivals**: path.transitdata.nyc GTFS-RT feed
- **Update frequency**: Alerts every 2-5 min, arrivals every 5 sec

## Lines & Stations

**Lines:** HOB-33, JSQ-33, NWK-WTC, HOB-WTC

**Stations:** Newark, Harrison, Journal Square, Grove Street, Exchange Place, Newport, Hoboken, Christopher St, 9th St, 14th St, 23rd St, 33rd St, World Trade Center

## Requirements

- Node.js 18+
- Internet access for API calls
- No API keys required

## Installation

```bash
openclaw skills install path-alerts
```

Or install from GitHub:
```bash
openclaw plugins install github:LiamSx45/openclaw-path-alerts
```
