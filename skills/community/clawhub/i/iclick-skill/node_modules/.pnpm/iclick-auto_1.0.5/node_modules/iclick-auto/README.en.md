# iclick-auto

![npm version](https://img.shields.io/npm/v/iclick-auto.svg)
![npm license](https://img.shields.io/npm/l/iclick-auto.svg)

English | [中文](README.md)

Node.js SDK for iOS automation without jailbreak. In addition to API calls, it implements automatic reconnection, event listening mechanisms, and binary meta data packet parsing.

Official Website: https://iosclick.com/

## Installation

```bash
npm install iclick-auto
```

## Quick Start

```javascript
const iclick = require('iclick-auto')

// Create client instance
const client = new iclick()

// Listen to device events
client.on('device:online', (_data) => {
    console.log('Device online:', _data)
})

client.on('device:offline', (_data) => {
    console.log('Device offline:', _data)
})

// Connect to server
await client.connect()

// Invoke API
const result = await client.invoke('getDevices', { deviceId: 'P60904DC8D3F' })

console.log('Result:', result)
```

## API Documentation

### `new iclick(options)`

Create a client instance.

**Parameters:**

| Parameter | Type | Optional | Description | Default |
|-----------|------|----------|-------------|---------|
| `options.host` | string | Yes | WebSocket server address | `127.0.0.1` |
| `options.port` | number | Yes | WebSocket server port | `23188` |
| `options.autoReconnect` | boolean | Yes | Enable automatic reconnection | `true` |
| `options.reconnectDelay` | number | Yes | Reconnection delay (seconds) | `3` |

### `client.connect()`

Connect to the WebSocket server.

**Returns:** `Promise<void>`

**Example:**

```javascript
try {
    await client.connect()
    console.log('Connected successfully')
} catch (error) {
    console.error('Connection failed:', error)
}
```

### `client.invoke(type, params, timeout)`

Invoke an API method.

**Parameters:**

- `type` (string): API type
- `params` (object, optional): Request parameters, default `{}`
- `timeout` (number, optional): Timeout in seconds, default `18`

**Returns:** `Promise<any>`

**Example:**

```javascript
// Send key
const result = await client.invoke('sendKey', {
    deviceId: 'P60904DC8D3F',
    key: 'h',
    fnkey: 'COMMAND'
})

// Custom timeout
const result = await client.invoke('someType', { param: 'value' }, 30)
```

### `client.on(eventName, callback)`

Register an event listener.

**Parameters:**

- `eventName` (string): Event name
- `callback` (function): Callback function that receives event data as parameter

**Example:**

```javascript
client.on('device:online', (_data) => {
    console.log('Device online:', _data)
})

client.on('device:offline', (_data) => {
    console.log('Device offline:', _data)
})
```

### `client.off(eventName, callback)`

Remove an event listener.

**Parameters:**

- `eventName` (string): Event name
- `callback` (function, optional): Callback function to remove. If not provided, all listeners for the event will be removed

**Example:**

```javascript
const handler = (_data) => {
    console.log('Event received:', _data)
}

// Register listener
client.on('someEvent', handler)

// Remove specific listener
client.off('someEvent', handler)

// Remove all listeners for the event
client.off('someEvent')
```

### `client.destroy()`

Destroy the client, disconnect and clean up all resources.

**Example:**

```javascript
client.destroy()
console.log('Client destroyed')
```

## License

ISC

## Related Links

- API Reference: https://iosclick.com/en/api/index.html
- Event Notifications: https://iosclick.com/en/api/notify.html

## Issues

If you encounter any issues, please report them in [Issues](https://github.com/Undefined-Token/iclick-nodejs/issues).

