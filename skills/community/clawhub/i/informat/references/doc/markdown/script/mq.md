# informat.mq Message Queue

## Overview

Use `informat.mq` to perform message queue operations

## basicGet

Pull a message from the queue

```javascript
informat.mq.basicGet(module, queue, autoAck)
```

| Parameter | Type      | Description                                                              |
|-----------|-----------|--------------------------------------------------------------------------|
| module    | `String`  | Message queue module identifier                                          |
| queue     | `String`  | Queue identifier                                                         |
| autoAck   | `Boolean` | Whether to auto-acknowledge. Generally set to false for manual acknowledgment |

**Return Value**

Type is [MqMessage](/guide/script/model.md#mqmessage)

::: tip
If you want to get a single message, use pull mode. However, do not use a loop-based pull mode to replace push mode, as this will severely impact performance.
:::

**Example**

::: code-group

```javascript [Call]
var message = informat.mq.basicGet("mq", "TaskQueue", true);
console.log('message', message)
```

```json [Return Value]
{
  "body": "{\r\n\t'taskId':'1',\r\n\t'taskStatus':'finished'\r\n}",
  "props": {
    "contentLength": 0,
    "deliveryTag": 1,
    "finalRetryForMessageWithNoId": false,
    "headers": {},
    "lastInBatch": false,
    "messageCount": 0,
    "projectionUsed": false,
    "publishSequenceNumber": 0,
    "receivedDeliveryMode": "NON_PERSISTENT",
    "receivedExchange": "",
    "receivedRoutingKey": "croe0zft168y3-skyduxiaoxiduilie-Test1",
    "redelivered": false
  }
}
```

:::

## publish

Send a message to the queue

```javascript
informat.mq.publish(moduleKey, routingKey, setting, message)
```

| Parameter  | Type                                                    | Description                    |
|------------|---------------------------------------------------------|--------------------------------|
| module     | `String`                                                | Message queue module identifier |
| routingKey | `String`                                                | Routing key                    |
| setting    | [PublishSetting](/guide/script/model.md#publishsetting) | Publish settings               |
| message    | `String`                                                | Message to send                |

::: info

- If setting.waitForConfirms is enabled, after the message is delivered, it will wait for the message queue to confirm successful delivery. If delivery fails, an exception will be thrown.
- Enabling setting.waitForConfirms will impact delivery performance, but it guarantees successful delivery.

:::

**Example**

```js
// Send a message to the queue after task completion
let body = {
    taskId: '1',
    taskStatus: 'finished'
}
informat.mq.publish('mq', 'TaskQueue', null, JSON.stringify(body));
```

## queuePurge

Purge a queue

```javascript
informat.mq.queuePurge(module, queue)
```

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| module    | `String` | Message queue module identifier |
| queue     | `String` | Queue identifier               |

**Example**

Purge the message queue after task completion

```js
informat.mq.queuePurge('mq', 'TaskQueue');
```

## basicAck

Manually acknowledge successful receipt of a message

```javascript
informat.mq.basicAck(message, multiple)
```

| Parameter | Type                                          | Description                    |
|-----------|-----------------------------------------------|--------------------------------|
| message   | [MqMessage](/guide/script/model.md#mqmessage) | Message object                 |
| multiple  | `Boolean`                                     | Whether to support batch acknowledgment |

**Example**

```javascript
// Acknowledge receipt of task completion message event
informat.mq.basicAck(message, true);
```

## basicNack

Nack-style rejection
Allows a consumer to reject a message, with the option to requeue or discard it

```javascript
informat.mq.basicNack(message, multiple, requeue)
```

| Parameter | Type                                          | Description                                                                                                           |
|-----------|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| message   | [MqMessage](/guide/script/model.md#mqmessage) | Message object                                                                                                        |
| multiple  | `Boolean`                                     | If false, only the message with this deliveryTag is rejected. If true, all messages before this deliveryTag are rejected. |
| requeue   | `Boolean`                                     | Whether to requeue the message                                                                                        |

**Example**
After receiving a task completion message event and business processing fails

```javascript
informat.mq.basicNack(message, true, true);
```

## basicReject

Reject a message
When a message is rejected and requeue is false, the message will be delivered to the dead letter queue

```javascript
informat.mq.basicReject(message, requeue)
```

| Parameter | Type                                          | Description                |
|-----------|-----------------------------------------------|----------------------------|
| message   | [MqMessage](/guide/script/model.md#mqmessage) | Message object             |
| requeue   | `Boolean`                                     | Whether to requeue the message |

**Example**

```javascript
informat.mq.basicReject(message, true);
```

## basicRecover

Resend unacknowledged messages

```javascript
informat.mq.basicRecover(message, requeue);
```

| Parameter | Type                                          | Description                                                                                                                                                                                        |
|-----------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| message   | [MqMessage](/guide/script/model.md#mqmessage) | Message object                                                                                                                                                                                     |
| requeue   | `Boolean`                                     | If requeue is true, unacknowledged messages will be re-added to the queue and may be assigned to a different consumer. If false, the same message will be assigned to the same consumer as before. |

**Example**

```javascript
informat.mq.basicRecover(message, true);
```

::: tip What to do if you accidentally deleted a queue from the message queue backend?

- You can find the corresponding message queue in the Informat message queue module configuration page, edit it and republish. The platform will automatically recreate the message queue.

:::
