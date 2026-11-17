# informat.email Email Related Operations

## Overview

Use the `informat.email` object to send emails

## send

Send an email

```javascript
informat.email.send(server, message);
```

::: warning Note
An incorrect email address or server connection failure will cause the email to fail to send. An exception will be thrown on failure.
:::

| Parameter | Type                                              | Description      |
|-----------|----------------------------------------------------|------------------|
| server    | [EmailServer](/guide/script/model.md#emailserver)  | Email server     |
| message   | `EmailMessage`                                     | Email content    |

**Example**

```javascript
const server = {
    host: 'smtp.gmail.com',
    port: 465,
    ssl: true,
    auth: true,
    account: 'account@informat.cn',
    password: '<smtp-password>',
    protocol: 'smtp'
}
const textMessage = {
    recipients: [
        { address: 'to1@informat.cn', 'personal': 'sky', type: 'TO' },
        { address: 'cc1@informat.cn', 'personal': 'ginko', type: 'CC' },// CC
    ],
    subject: 'Email Subject',
    personal: 'Sender Nickname',
    text: 'Plain text email content',// Plain text content
}
const richMessage = {
    recipients: [
        { address: 'to1@informat.cn', 'personal': 'sky', type: 'TO' },
        { address: 'cc1@informat.cn', 'personal': 'ginko', type: 'CC' },// CC
    ],
    subject: 'Email Subject',
    personal: 'Sender Nickname',
    multiparts: [
        {
            type: 'text',
            content: 'Plain text content'
        },
        {
            type: 'content',
            contentType: "text/html;charset=utf-8",
            content: '<div style="color:red">Rich text content</div><img src="cid:image1"/>'
        },
        {
            type: 'attachment',
            contentId: '<image1>',
            disposition: 'inline',
            filename: 'image1.jpg',
            filepath: "logo.jpg"
        },// Image displayed in rich text
        {
            type: 'attachment',
            filename: 'excel.xlsx',
            filepath: "test.xlsx"
        },// Email attachment (local file)
        {
            type: 'attachment',
            filename: 'excel.xlsx',
            storageFilepath: "test.xlsx"
        }// Email attachment (shared storage file)
    ]
}
//
try {
    informat.email.send(server, textMessage);
    informat.email.send(server, richMessage);
} catch (e) {
    console.log('Send failed');
}
```

## sendWithSystemServer

Send an email using the system email server

```javascript
informat.email.sendWithSystemServer(message);
```

::: warning Note
An incorrect email address or server connection failure will cause the email to fail to send. An exception will be thrown on failure. System email configuration can be found [here](/guide/install/after_deploy.md#mail服务器配置).
:::

| Parameter | Type           | Description   |
|-----------|----------------|---------------|
| message   | `EmailMessage` | Email content |

**Example**

```js
const textMessage = {
    recipients: [
        { address: 'to1@informat.cn', 'personal': 'sky', type: 'TO' },
        { address: 'cc1@informat.cn', 'personal': 'ginko', type: 'CC' },// CC
    ],
    subject: 'Email Subject',
    personal: 'Sender Nickname',
    text: 'Plain text email content',// Plain text content
}
informat.email.sendWithSystemServer(textMessage);
```
