---
name: mqtt-client
description: Universal MQTT Client for OpenClaw with Node.js/mqtt.js. Enables Connection Management, Subscription Management, Message Handling and OpenClaw Integration for arbitrary MQTT-based automation.
---

# 📡 MQTT OpenClaw Skill

> Production-ready MQTT client for OpenClaw automation. Universal - not bound to specific systems.

Universal MQTT Client for OpenClaw with Node.js/mqtt.js. Connect to any MQTT broker to subscribe to topics, publish messages, and react to state changes. The client automatically handles reconnection, supports wildcards for flexible topic patterns, and can trigger alerts when values cross thresholds (e.g., battery below 10% or temperature above 30°C). Use this skill to integrate OpenClaw with smart home systems such as ioBroker, Home Assistant, Zigbee2MQTT, Shelly devices, other OpenClaw instances (to communicate between them), or any other MQTT-based system.

---

## 🚀 Quick Start

### Prerequisites

```bash
npm install mqtt
```

### Minimal Example

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

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_BROKER` | `localhost` | Broker URL (with or without protocol) |
| `MQTT_BROKER_PORT` | `1883` | Broker port |
| `MQTT_USERNAME` | - | Username (optional) |
| `MQTT_PASSWORD` | - | Password (optional) |
| `MQTT_CLIENT_ID` | auto-generated | Client ID (max 23 chars) |
| `MQTT_SUBSCRIBE_TOPIC` | `#` | Default topic to subscribe |
| `MQTT_KEEPALIVE` | `60` | Keep-alive interval (seconds) |
| `MQTT_RECONNECT_PERIOD` | `5000` | Reconnect interval (ms) |

### Auto-Setup

When first used, the skill automatically creates config in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "mqtt-client": {
        "enabled": true,
        "env": {
          "MQTT_BROKER": "localhost",
          "MQTT_BROKER_PORT": "1883"
        }
      }
    }
  }
}
```

> ⚠️ Existing values are NOT overwritten.

---

## 🔌 Connection Management

### Auto-Reconnect

```javascript
const client = new MqttClient({
  broker: 'mqtt://localhost:1883',
  reconnectPeriod: 5000,
  connectTimeout: 30000,
  maxReconnectAttempts: 10
});
```

### Keep-Alive

```javascript
const client = new MqttClient({
  broker: 'mqtt://localhost:1883',
  keepalive: 60  // seconds
});
```

### LWT (Last Will & Testament)

```javascript
const client = new MqttClient({
  will: {
    topic: 'openclaw/status',
    payload: JSON.stringify({ status: 'offline' }),
    qos: 1,
    retain: true
  }
});
```

### Graceful Disconnect

```javascript
await client.disconnect();  // with timeout
await client.disconnect(5000);
```

---

## 📬 Subscription Management

### Basic Subscribe

```javascript
// Single topic
await client.subscribe('home/bridge/info');

// Multiple topics
await client.subscribe(['home/bridge/info', 'home/bridge/state']);
```

### Wildcards

| Wildcard | Description | Example |
|----------|-------------|---------|
| `+` | Single level | `home/+/temperature` |
| `#` | Multi level | `home/sensors/#` |

### QoS Levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | At most once | Fire and forget |
| 1 | At least once | Acknowledged delivery |
| 2 | Exactly once | Handshake protocol |

```javascript
await client.subscribe('topic', { qos: 2 });
```

### Dynamic Subscribe/Unsubscribe

```javascript
await client.subscribe('new/topic');
await client.unsubscribe('old/topic');
await client.unsubscribeAll();
```

---

## 📤 Message Handling

### Publish

```javascript
// Simple
await client.publish('home/lights/set', 'ON');

// With options
await client.publish('home/lights/set', 'ON', { qos: 1, retain: true });

// As JSON (auto-stringified)
await client.publish('home/lights/set', { state: 'ON', brightness: 255 });
```

### Retained Messages

```javascript
// Set retained
await client.publish('home/announcement', 'Hello', { retain: true });

// Delete retained (empty payload)
await client.publish('home/announcement', '', { retain: true });
```

### JSON Parsing

Automatic parsing - `payload` is already an object for JSON messages:

```javascript
client.on('message', (topic, payload) => {
  if (typeof payload === 'object') {
    console.log('JSON:', payload.key);
  }
});
```

---

## 🔔 Threshold Triggers

React to value changes with triggers:

```javascript
// Battery low trigger
client.addTrigger('battery-low', {
  topic: 'home/+/battery',
  path: 'value',
  operator: '<',
  threshold: 10,
  valueType: 'number',
  cooldown: 60000,
  callback: (event) => console.log('⚠️ Low battery:', event.value)
});

// Temperature high trigger
client.addTrigger('temp-high', {
  topic: 'home/sensors/+/temperature',
  path: 'value',
  operator: '>',
  threshold: 30,
  valueType: 'number',
  callback: (event) => console.log('🔥 Hot:', event.value)
});
```

### Trigger Operators

| Operator | Description |
|----------|-------------|
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |
| `==` | Equal |
| `!=` | Not equal |
| `contains` | String contains |
| `startsWith` | String starts with |

---

## 📊 Health & State

### Get Health Status

```javascript
const health = client.getHealth();
// { connected, reconnecting, lastConnected, messagesReceived, latency }
```

### Get Current State

```javascript
const state = client.getState();
// { status, broker, subscriptions }
```

### Message History

```javascript
// Last messages for topic
const history = client.getMessageHistory('home/+/temperature');

// Last message
const last = client.getLastMessage('home/sensors/#');

// Clear history
client.clearHistory();
```

---

## 📋 API Reference

### Constructor Options

| Option               | Type    | Default | Description             |
|----------------------|---------|---------|-------------------------|
| `broker`             | string  | env     | MQTT Broker URL         |
| `username`           | string  | env     | Username                |
| `password`           | string  | env     | Password                |
| `clientId`           | string  | auto    | Client ID               |
| `reconnectPeriod`    | number  | 5000    | Reconnect interval (ms) |
| `connectTimeout`     | number  | 30000   | Connection timeout (ms) |
| `keepalive`          | number  | 60      | Keep-alive (s)          |
| `messageHistorySize` | number  | 50      | Max history entries     |
| `parseJson`          | boolean | true    | Auto JSON parse         |
| `logLevel`           | string  | info    | debug/info/warn/error   |

### Methods

| Method                          | Description           |
|---------------------------------|-----------------------|
| `connect()`                     | Establish connection  |
| `disconnect([ms])`              | Graceful disconnect   |
| `subscribe(topic, opts)`        | Subscribe to topic(s) |
| `unsubscribe(topic)`            | Unsubscribe           |
| `publish(topic, payload, opts)` | Publish message       |
| `getMessageHistory([topic])`    | Get message history   |
| `getHealth()`                   | Health status         |
| `getState()`                    | Current state         |
| `isConnected()`                 | Connection check      |
| `addTrigger(id, config)`        | Add threshold trigger |
| `removeTrigger(id)`             | Remove trigger        |
| `getTriggers()`                 | List triggers         |

### Events

| Event           | Description                               |
|-----------------|-------------------------------------------|
| `connect`       | Successfully connected                    |
| `disconnect`    | Disconnected                              |
| `message`       | Message received (topic, payload, packet) |
| `error`         | Error occurred                            |
| `offline`       | Client offline                            |
| `reconnecting`  | Attempting reconnect                      |
| `reconnect`     | Successfully reconnected                  |

---

## 📁 Resources

### scripts/

- `mqtt-client.js` - Main library

### references/

- `mqtt-topics.md` - Topic naming conventions

---

## 🔗 External Links

- [mqtt.js GitHub](https://github.com/mqttjs/MQTT.js)
- [MQTT 5.0 Spec](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)