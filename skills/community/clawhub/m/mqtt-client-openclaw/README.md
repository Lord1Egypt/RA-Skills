# MQTT Client Skill for OpenClaw

> Production-ready, universal MQTT client with auto-reconnect, triggers, and health monitoring.

## Features

- 🔌 **Connection Management** - Auto-reconnect, Keep-Alive, LWT, Graceful disconnect
- 📬 **Subscription Management** - Wildcards (`+`, `#`), QoS levels (0/1/2), dynamic subscribe/unsubscribe
- 📤 **Message Handling** - Publish, retained messages, automatic JSON parsing
- ⚡ **Threshold Triggers** - React to value changes (e.g., battery < 10%, temperature > 30°C)
- 📊 **Health Monitoring** - Connection status, latency, message statistics
- 💾 **Message History** - Last N messages per topic
- 🔒 **Security** - TLS support, credentials from config

## Quick Start

```bash
npm install mqtt
```

```javascript
const { MqttClient } = require('./scripts/mqtt-client.js');

const client = new MqttClient({
  broker: process.env.MQTT_BROKER,
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD
});

client.on('message', (topic, payload) => console.log(`${topic}: ${payload}`));

await client.connect();
await client.subscribe('home/#');
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_BROKER` | localhost | Broker URL |
| `MQTT_BROKER_PORT` | 1883 | Broker port |
| `MQTT_USERNAME` | - | Username (optional) |
| `MQTT_PASSWORD` | - | Password (optional) |
| `MQTT_CLIENT_ID` | auto | Client ID |
| `MQTT_SUBSCRIBE_TOPIC` | # | Default topic |

Auto-configured in `~/.openclaw/openclaw.json` on first use.

## Threshold Triggers

React to value changes automatically:

```javascript
// Battery low warning
client.addTrigger('battery-low', {
  topic: 'home/+/battery',
  path: 'value',
  operator: '<',
  threshold: 10,
  valueType: 'number',
  cooldown: 60000,
  callback: (event) => console.log('Low battery:', event.value)
});
```

Supported operators: `>`, `<`, `>=`, `<=`, `==`, `!=`, `contains`, `startsWith`

## API

### Constructor Options

- `broker` - MQTT Broker URL
- `username` / `password` - Auth (optional)
- `clientId` - Custom client ID
- `reconnectPeriod` - Reconnect interval (ms)
- `keepalive` - Keep-alive interval (s)
- `messageHistorySize` - Max history entries
- `parseJson` - Auto JSON parse

### Methods

| Method | Description |
|--------|-------------|
| `connect()` | Establish connection |
| `disconnect()` | Graceful disconnect |
| `subscribe(topic, opts)` | Subscribe |
| `unsubscribe(topic)` | Unsubscribe |
| `publish(topic, payload, opts)` | Publish message |
| `getMessageHistory(topic)` | Get message history |
| `getHealth()` | Health status |
| `addTrigger(id, config)` | Add threshold trigger |

## Resources

- `scripts/mqtt-client.js` - Main library
- `references/mqtt-topics.md` - Topic naming conventions

## License

MIT-0 (No Attribution Required) - See [LICENSE](scripts/mqtt-client.js) for full text.

## Links

- [mqtt.js Documentation](https://github.com/mqttjs/MQTT.js)
- [MQTT 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)