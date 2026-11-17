# informat.wework WeCom Operations

## Overview

Use the `informat.wework` object to call WeCom (WeChat Work) APIs, covering commonly used interfaces such as customer contact, customer groups, mass messaging, welcome messages, etc. All methods automatically use the current team's WeCom configuration (WeCom integration must be completed in the team admin panel first), and internally handle `access_token` retrieval and refresh automatically.

Return values are all `Map<String, Object>` (JSON objects), and field meanings are consistent with the official WeCom documentation.

## getAccessToken

Get the WeCom `access_token`.

```javascript
informat.wework.getAccessToken();
```

**Returns** `String`

**Example**

```javascript
const token = informat.wework.getAccessToken();
console.log(token);
```

## getUserIdList

Get the member ID list. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/96269).

```javascript
informat.wework.getUserIdList(limit, cursor);
```

| Parameter | Type      | Description                                                  |
|-----------|-----------|--------------------------------------------------------------|
| limit     | `Integer` | Number of records per pull, default 10000, max 10000         |
| cursor    | `String`  | Pagination cursor, pass `null` or empty string for the first query |

**Example**

```javascript
let cursor = null;
do {
    const result = informat.wework.getUserIdList(10000, cursor);
    result.dept_user.forEach(u => console.log(u.userid, u.department));
    cursor = result.next_cursor;
} while (cursor);
```

## getGroupChatList

Get the customer group list. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92120).

```javascript
informat.wework.getGroupChatList(statusFilter, userIdList, partyIdList, limit, cursor);
```

| Parameter    | Type       | Description                                                        |
|--------------|------------|--------------------------------------------------------------------|
| statusFilter | `Integer`  | Group status filter: 0-all, 1-pending transfer from departed member, 2-transfer in progress, 3-transfer completed. Can be `null` |
| userIdList   | `String[]` | Group owner userid list, can be `null`                             |
| partyIdList  | `String[]` | Group owner department id list, can be `null`                      |
| limit        | `Integer`  | Number of groups per pull, default 100, max 1000                   |
| cursor       | `String`   | Pagination cursor, pass `null` or empty string for the first query |

**Example**

```javascript
const result = informat.wework.getGroupChatList(0, null, null, 100, null);
result.group_chat_list.forEach(g => console.log(g.chat_id, g.status));
```

## getGroupChat

Get customer group details. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92122).

```javascript
informat.wework.getGroupChat(chatId, needName);
```

| Parameter | Type      | Description                                    |
|-----------|-----------|------------------------------------------------|
| chatId    | `String`  | Customer group ID                              |
| needName  | `Integer` | Whether to return group member names: 0-no, 1-yes |

**Example**

```javascript
const chat = informat.wework.getGroupChat('wrqVPjDAAAAb8SqvAfi3OuABDqviLKzg', 1);
console.log(chat.name, chat.owner, chat.member_list);
```

## addMsgTemplate

Create a mass message. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92135).

```javascript
informat.wework.addMsgTemplate(msgTemplate);
```

| Parameter   | Type     | Description                                |
|-------------|----------|--------------------------------------------|
| msgTemplate | `Object` | Mass message template, refer to official docs for structure |

**Example**

```javascript
const template = {
    chat_type: 'single',//single-send to customer  group-send to customer group
    external_userid: ['external_userid_xxx'],
    sender: 'DuZhanYang',
    text: { content: 'Hello, thank you for your attention!' },
    attachments: [
        {
            msgtype: 'link',
            link: {
                title: 'Welcome Link',
                picurl: 'https://example.com/pic.jpg',
                desc: 'Click to view',
                url: 'https://example.com'
            }
        }
    ]
};
const result = informat.wework.addMsgTemplate(template);
console.log(result.msgid, result.fail_list);
```

## unionidToExternalUserid

Query the WeCom customer `external_userid` by a WeChat customer `unionid`. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/95900).

```javascript
informat.wework.unionidToExternalUserid(unionid);
```

| Parameter | Type     | Description             |
|-----------|----------|-------------------------|
| unionid   | `String` | WeChat customer unionid |

**Example**

```javascript
const result = informat.wework.unionidToExternalUserid('unionid_xxx');
console.log(result.external_userid);
```

## getUnassignedList

Get the customer list of departed members. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92124).

```javascript
informat.wework.getUnassignedList(pageId, pageSize, cursor);
```

| Parameter | Type      | Description                              |
|-----------|-----------|------------------------------------------|
| pageId    | `Integer` | Page id, pass 0 for the first page       |
| pageSize  | `Integer` | Number per page, default 100, max 1000   |
| cursor    | `String`  | Pagination cursor, pass `null` for the first query |

**Example**

```javascript
const result = informat.wework.getUnassignedList(0, 100, null);
result.info.forEach(item => console.log(item.handover_userid, item.external_userid));
```

## getUserBehaviorData

Get "Contact Customer Statistics" data. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92132).

```javascript
informat.wework.getUserBehaviorData(userIdList, partyIdList, startTime, endTime);
```

| Parameter   | Type       | Description                          |
|-------------|------------|--------------------------------------|
| userIdList  | `String[]` | Member userid list, can be `null`    |
| partyIdList | `String[]` | Department id list, can be `null`    |
| startTime   | `long`     | Start timestamp (seconds)            |
| endTime     | `long`     | End timestamp (seconds)              |

::: warning Note
At least one of `userIdList` and `partyIdList` must be provided; the time range cannot exceed 30 days.
:::

**Example**

```javascript
const end = Math.floor(Date.now() / 1000);
const start = end - 7 * 86400;
const result = informat.wework.getUserBehaviorData(['DuZhanYang'], null, start, end);
console.log(result.behavior_data);
```

## getGroupMsgResult

Get mass message execution results for members. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/93338).

```javascript
informat.wework.getGroupMsgResult(msgid, userid, limit, cursor);
```

| Parameter | Type      | Description                                  |
|-----------|-----------|----------------------------------------------|
| msgid     | `String`  | Mass message id                              |
| userid    | `String`  | Sender's userid                              |
| limit     | `Integer` | Number per pull, default 500                 |
| cursor    | `String`  | Pagination cursor, pass `null` for the first query |

**Example**

```javascript
const result = informat.wework.getGroupMsgResult('msg_xxx', 'DuZhanYang', 500, null);
console.log(result.detail_list);
```

## getGroupMsgListV2

Get all mass message records for the enterprise. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/93338).

```javascript
informat.wework.getGroupMsgListV2(chatType, startTime, endTime, creator, filterType, limit, cursor);
```

| Parameter  | Type      | Description                                                |
|------------|-----------|------------------------------------------------------------|
| chatType   | `String`  | Chat type: `single` or `group`                             |
| startTime  | `long`    | Start timestamp (seconds)                                  |
| endTime    | `long`    | End timestamp (seconds)                                    |
| creator    | `String`  | Creator userid, can be `null`                              |
| filterType | `Integer` | Send method filter: 0-all (default), 1-enterprise sent, 2-member sent |
| limit      | `Integer` | Number per pull, default 50, max 100                       |
| cursor     | `String`  | Pagination cursor, pass `null` for the first query         |

**Example**

```javascript
const end = Math.floor(Date.now() / 1000);
const start = end - 7 * 86400;
const result = informat.wework.getGroupMsgListV2('single', start, end, null, 0, 50, null);
result.groupmsg_list.forEach(m => console.log(m.msgid, m.creator, m.create_time));
```

## sendWelcomeMsg

Send a new customer welcome message. Refer to the [official documentation](https://developer.work.weixin.qq.com/document/path/92137).

```javascript
informat.wework.sendWelcomeMsg(welcomeCode, text, attachments);
```

::: warning Note
The `welcomeCode` comes from the event callback of the "add external contact event" or "group join event", and each `welcomeCode` can only be used once with a validity period of 20 seconds. `text` and `attachments` cannot both be empty.
:::

| Parameter   | Type     | Description                                          |
|-------------|----------|------------------------------------------------------|
| welcomeCode | `String` | Welcome message code from event push                 |
| text        | `Object` | Text message object `{ content: '...' }`, can be `null` |
| attachments | `Array`  | Attachment list, supports image/link/miniprogram/video/file |

**Example**

```javascript
const text = { content: 'Welcome, thank you for your attention!' };
const attachments = [
    {
        msgtype: 'link',
        link: {
            title: 'Welcome Link',
            picurl: 'https://example.com/pic.jpg',
            desc: 'Click to view',
            url: 'https://example.com'
        }
    }
];
informat.wework.sendWelcomeMsg('welcome_code_xxx', text, attachments);
```
