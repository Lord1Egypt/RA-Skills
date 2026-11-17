# informat.notification System Notifications

## Overview

Use `informat.notification` to perform system notification operations.

## queryNotificationListCount

Query the total count of system notifications

```javascript
informat.notification.queryNotificationListCount(filter)
```

| Parameter | Type                                      | Description |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Filter conditions |

Fields available in the filter

| Field            | Type      | Description |
|----------------|---------|---------|
| id             | String  | System notification ID |
| accountId      | String  | Account ID |
| name           | String  | Name |
| type           | String  | Type |
| content        | String  | Content |
| isRead         | Boolean | Whether read |
| isWebSend      | String  | Whether sent via web |
| isDingTalkSend | String  | Whether sent via DingTalk |
| isFeishuSend   | String  | Whether sent via Feishu |
| createTime     | String  | Creation time |

**Return Value**

Type is `Integer`
Returns the total count of system notifications

**Example**

```javascript
const count = informat.notification.queryNotificationListCount({
    conditionList: [
        {
            fieldId: 'accountId',
            opt: 'eq',
            value: 'x38s0fa436v69'
        }
    ]
})
// Get the matching list count
console.log('count:', count);
```

## queryNotificationList

Query system notification list

```javascript
informat.notification.queryNotificationList(query)
```

| Parameter | Type                                    | Description |
|-------|---------------------------------------|------|
| query | [Query](/guide/script/model.md#query) | Query conditions |

Fields available in the filter

| Field            | Type      | Description |
|----------------|---------|---------|
| id             | String  | System notification ID |
| accountId      | String  | Account ID |
| name           | String  | Name |
| type           | String  | Type |
| content        | String  | Content |
| isRead         | Boolean | Whether read |
| isWebSend      | String  | Whether sent via web |
| isDingTalkSend | String  | Whether sent via DingTalk |
| isFeishuSend   | String  | Whether sent via Feishu |
| createTime     | String  | Creation time |

**Return Value**

Type is Array<[Notification](/guide/script/model.md#notification)>
Returns system notification list

**Example**

```javascript
const notificationList = informat.notification.queryNotificationList({
    pageIndex: 1,
    pageSize: 20,
    filter: {
        conditionList: [
            {
                fieldId: 'accountId',
                opt: 'eq',
                value: 'x38s0fa436v69'
            }
        ]
    }
})
// Get system notification list
console.log('notificationList:', notificationList);
```

## updateNotification

Update a system notification

```javascript
informat.notification.updateNotification(notification)
```

| Parameter      | Type                                                  | Description |
|--------------|-----------------------------------------------------|------|
| notification | [Notification](/guide/script/model.md#notification) | System notification |

Fields that can be updated

| Field            | Type      | Description |
|----------------|---------|----------------|
| isWebSend      | Boolean | Whether sent via Websocket |
| isWeworkSend   | Boolean | Whether sent via WeCom |
| isDingTalkSend | Boolean | Whether sent via DingTalk |
| isFeishuSend   | Boolean | Whether sent via Feishu |
| isCustomSend   | Boolean | Whether custom notification sent |

**Return Value**

Type is `Integer`
Number of records updated

**Example**

```javascript
informat.notification.updateNotification({
    'id': 'e15ab1jmdjyl8',
    'isWebSend': true,
    'isWeworkSend': true,
    'isDingTalkSend': true,
    'isFeishuSend': true,
    'isCustomSend': true
});
```

## deleteNotification

Delete a system notification

```javascript
informat.notification.deleteNotification(id)
```

| Parameter | Type       | Description |
|----|----------|--------|
| id | `String` | System notification ID |

**Return Value**

Type is `Integer`
Number of records deleted

**Example**

```javascript
informat.notification.deleteNotification('b8ynqdu6z31ry');
```

## queryCustomNotificationListCount

Query the total count of unsent custom notifications

```javascript
informat.notification.queryCustomNotificationListCount(filter)
```

| Parameter | Type                                      | Description |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Filter conditions |

Fields available in the filter

| Field            | Type     | Description |
|----------------|--------|---------|
| id             | String | System notification ID |
| accountId      | String | Account ID |
| name           | String | Name |
| type           | String | Type |
| content        | String | Content |
| isWebSend      | String | Whether sent via web |
| isDingTalkSend | String | Whether sent via DingTalk |
| isFeishuSend   | String | Whether sent via Feishu |
| createTime     | String | Creation time |

**Return Value**

Type is `Integer`
Returns the total count of system notifications

**Example**

```javascript
const count = informat.notification.queryCustomNotificationListCount({
    conditionList: [
        {
            fieldId: 'accountId',
            opt: 'eq',
            value: 'x38s0fa436v69'
        }
    ]
})
// Get the matching list count
console.log('count:', count);
```

## queryCustomNotificationList

Query unsent custom notification list

```javascript
informat.notification.queryCustomNotificationList(query)
```

| Parameter | Type      | Description |
|-------|---------|------|
| query | [Query](/guide/script/model.md#query) | Query conditions |

Fields available in the filter

| Field            | Type     | Description |
|----------------|--------|---------|
| id             | String | System notification ID |
| accountId      | String | Account ID |
| name           | String | Name |
| type           | String | Type |
| content        | String | Content |
| isWebSend      | String | Whether sent via web |
| isDingTalkSend | String | Whether sent via DingTalk |
| isFeishuSend   | String | Whether sent via Feishu |
| createTime     | String | Creation time |

**Return Value**

Type is Array<[Notification](/guide/script/model.md#notification)>
Returns system notification list

**Example**

```javascript
const notificationList = informat.notification.queryCustomNotificationList({
    pageIndex: 1,
    pageSize: 20,
    filter: {
        conditionList: [
            {
                fieldId: 'accountId',
                opt: 'eq',
                value: 'x38s0fa436v69'
            }
        ]
    }
})
// Get the matching list
console.log('notificationList:', notificationList);
```

## sendNotification

Send a system notification

```javascript
informat.notification.sendNotification(notification)
```

| Parameter      | Type                         | Description |
|--------------|----------------------------|--------|
| notification | [NotificationForm](/guide/script/model.md#notificationform) | System notification form |

**Return Value**

Type is `String`
Returns the system notification ID

**Example**

```javascript
const notificationId = informat.notification.sendNotification({
    title: 'Notification Title',
    content: 'Notification Content',
    accountId: informat.app.userId(),
    type: "openurl", // openurl||openrecord|openbpmntask
    urlSetting: {
        url: "https://next.informat.cn/",
        "isAppURL": false
    },
    recordSetting: {
        recordId: null,
        moduleId: null,
    },
    bpmnTaskSetting: {
        taskId: null,
        moduleId: null
    }
})
// Get notification ID
console.log('notificationId:', notificationId);
```

## setCustomNotificationSent

Mark a custom notification as sent

::: tip
After successful setting, `notificationSent.isCustomSend` will be changed to true (sent)
:::

```javascript
informat.notification.setCustomNotificationSent(notificationId)
```

| Parameter        | Type       | Description |
|----------------|----------|------|
| notificationId | `String` | Notification ID |

**Example**

```javascript
const notificationList = informat.notification.queryCustomNotificationList({
    pageIndex: 1,
    pageSize: 20,
    filter: {
        conditionList: [
            {
                fieldId: 'accountId',
                opt: 'eq',
                value: 'x38s0fa436v69'
            }
        ]
    }
})
notificationList.forEach(notification => {
    console.log('notification:', notification);
    // do smth
    // Mark as sent
    informat.notification.setCustomNotificationSent(notification.id)
});
```

## setThreadLocalEnableNotify

Set the thread-local variable for whether notifications are enabled in the current application

```javascript
informat.notification.setThreadLocalEnableNotify(enable)
```

| Parameter | Type        | Description |
|--------|-----------|--------|
| enable | `Boolean` | Whether to enable notifications |

**Example**

```javascript
informat.notification.setThreadLocalEnableNotify(true);
```

## isThreadLocalEnableNotify

Get the thread-local variable for whether notifications are enabled in the current application

```javascript
informat.notification.isThreadLocalEnableNotify()
```

**Return Value**

Type is `Boolean`
Returns whether notifications are enabled

**Example**

```javascript
informat.notification.isThreadLocalEnableNotify();
```
