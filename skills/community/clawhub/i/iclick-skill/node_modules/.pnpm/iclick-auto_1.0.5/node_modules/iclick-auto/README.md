# iclick-auto

![npm version](https://img.shields.io/npm/v/iclick-auto.svg)
![npm license](https://img.shields.io/npm/l/iclick-auto.svg)

[English](README.en.md) | 中文

用于iOS免越狱自动化的 Node.js SDK。除了 API 调用功能外，实现了断线重连和事件监听机制以及二进制meta数据包解析。

官方网站: https://iosclick.com/

## 安装

```bash
npm install iclick-auto
```

## 快速开始

```javascript
const iclick = require('iclick-auto')

// 创建客户端实例
const client = new iclick()

// 监听设备事件
client.on('device:online', (_data) => {
    console.log('设备上线:', _data)
})

client.on('device:offline', (_data) => {
    console.log('设备下线:', _data)
})

// 连接服务器
await client.connect()

// 调用 API
const result = await client.invoke('getDevices', { deviceId: 'P60904DC8D3F' })

console.log('结果:', result)
```

## API 文档

### `new iclick(options)`

创建客户端实例。

**参数：**

| 参数 | 类型 | 可选 | 说明 | 默认值 |
|------|------|------|------|--------|
| `options.host` | string | 是 | WebSocket 服务器地址 | `127.0.0.1` |
| `options.port` | number | 是 | WebSocket 服务器端口 | `23188` |
| `options.autoReconnect` | boolean | 是 | 是否启用自动重连 | `true` |
| `options.reconnectDelay` | number | 是 | 重连延迟（秒） | `3` |


### `client.connect()`

连接到 WebSocket 服务器。

**返回：** `Promise<void>`

**示例：**

```javascript
try {
    await client.connect()
    console.log('连接成功')
} catch (error) {
    console.error('连接失败:', error)
}
```

### `client.invoke(type, params, timeout)`

调用 API 方法。

**参数：**

- `type` (string): API 类型
- `params` (object, 可选): 请求参数，默认 `{}`
- `timeout` (number, 可选): 超时时间（秒），默认 `18`

**返回：** `Promise<any>`

**示例：**

```javascript
// 发送按键
const result = await client.invoke('sendKey', {
    deviceId: 'P60904DC8D3F',
    key: 'h',
    fnkey: 'COMMAND'
})

// 自定义超时时间
const result = await client.invoke('someType', { param: 'value' }, 30)
```

### `client.on(eventName, callback)`

注册事件监听器。

**参数：**

- `eventName` (string): 事件名称
- `callback` (function): 回调函数，接收事件数据作为参数

**示例：**

```javascript
client.on('device:online', (_data) => {
    console.log('设备上线:', _data)
})

client.on('device:offline', (_data) => {
    console.log('设备下线:', _data)
})
```

### `client.off(eventName, callback)`

移除事件监听器。

**参数：**

- `eventName` (string): 事件名称
- `callback` (function, 可选): 要移除的回调函数。如果不提供，将移除该事件的所有监听器

**示例：**

```javascript
const handler = (_data) => {
    console.log('收到事件:', _data)
}

// 注册监听器
client.on('someEvent', handler)

// 移除特定监听器
client.off('someEvent', handler)

// 移除事件的所有监听器
client.off('someEvent')
```

### `client.destroy()`

销毁客户端，断开连接并清理所有资源。

**示例：**

```javascript
client.destroy()
console.log('客户端已销毁')
```

## License

ISC

## 相关链接

- API参考: https://iosclick.com/zh/api/index.html
- 事件通知: https://iosclick.com/zh/api/notify.html

## 问题反馈

如有问题，请在 [Issues](https://github.com/Undefined-Token/iclick-nodejs/issues) 中反馈。
