# NJ PATH Alerts Plugin

Real-time service alerts, status, and arrival times for NJ PATH trains.

## Features

- ✅ Real-time service alerts from official Port Authority API
- ✅ **Live train arrivals** via GTFS-Realtime feed
- ✅ Line-specific filtering (HOB-33, JSQ-33, NWK-WTC, HOB-WTC)
- ✅ Station-specific arrival times
- ✅ Service status summary for all lines
- ✅ No API keys required
- ✅ Automatic duplicate detection
- ✅ Formatted messages for chat

## Installation

```bash
cd /path/to/plugin
npm install
openclaw plugins install .
```

## Usage

### Check service alerts
```javascript
import { getAlertsMessage } from 'nj-path-alerts';

// All lines
const alerts = await getAlertsMessage();

// Specific line
const hobokenAlerts = await getAlertsMessage('HOB-33');
```

### Get live arrivals
```javascript
import { getStationArrivals } from 'nj-path-alerts';

// Get next trains at Hoboken
const arrivals = await getStationArrivals('hoboken');
console.log(arrivals);
// 🚊 **Hoboken** - Next trains:
// **859**: 2 min, 6 min
// **1024**: 8 min
```

### Check service status
```javascript
import { getStatusMessage } from 'nj-path-alerts';

const status = await getStatusMessage();
// 🚊 **PATH Service Status**
// ✅ Good Service **HOB-33** - Hoboken - 33rd St
// ✅ Good Service **JSQ-33** - Journal Square - 33rd St
// ...
```

## API Reference

### Alerts
- `getPathAlerts()` - All active alerts
- `getAlertsForLine(lineCode)` - Filter by line
- `getAlertsMessage(lineCode?)` - Formatted message
- `checkForNewAlerts()` - Poll for new alerts
- `getStatusMessage()` - Service status summary

### Real-time Arrivals
- `getStationArrivals(stationName)` - Next trains at station
- `getTrainsAtStation(stationId)` - Raw train data
- `getArrivalsMessage(stationId, name)` - Formatted arrivals

### Stations
`newark`, `harrison`, `journal_square`, `grove_street`, `exchange_place`, `newport`, `hoboken`, `christopher_street`, `ninth_street`, `fourteenth_street`, `twenty_third_street`, `thirty_third_street`, `world_trade_center`

### Lines
- `HOB-33`: Hoboken ↔ 33rd St
- `JSQ-33`: Journal Square ↔ 33rd St  
- `NWK-WTC`: Newark ↔ World Trade Center
- `HOB-WTC`: Hoboken ↔ World Trade Center

## Data Sources

1. **Port Authority Alerts API**
   - URL: `panynj.gov/.../everbridge/incidents`
   - Service disruptions, delays
   - Updates: 2-5 min
   - No auth required

2. **GTFS-Realtime Feed**
   - URL: `path.transitdata.nyc/gtfsrt`
   - Real-time vehicle positions & arrivals
   - Updates: Every 5 seconds
   - Community-maintained

## Example: Monitor PATH Alerts

```javascript
import { checkForNewAlerts, formatAlert } from 'nj-path-alerts';

// Poll every 5 minutes
setInterval(async () => {
  const newAlerts = await checkForNewAlerts();
  for (const alert of newAlerts) {
    await sendTelegram(formatAlert(alert));
  }
}, 300000);
```

## License

MIT
