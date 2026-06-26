---
name: imapflow
description: Modern Node.js IMAP client library (imapflow) for email integration.Covers authentication, mailbox locking, streaming fetches, async iterators, reconnection strategies, proxy support, and provider-specific configs (Gmail, Outlook, Yahoo, etc.).
---

# ImapFlow

## Overview

ImapFlow is a modern, promise-based IMAP client for Node.js. It auto-detects and handles IMAP extensions (CONDSTORE, QRESYNC, IDLE, COMPRESS, etc.) so the same code works across servers.

Key features: async/await API, async iterators for message streaming, built-in mailbox locking, TypeScript support, SOCKS/HTTP proxy support, Gmail X-GM-EXT-1 support.

## Trigger Scene

Use when building email features: connecting to IMAP servers, fetching/reading emails, searching mailboxes, managing folders, monitoring new messages via IDLE, working with Gmail labels and  Gmail-specific extensions, or any IMAP-based email automation. 

## Quick Start

```js
const { ImapFlow } = require('imapflow');

const client = new ImapFlow({
    host: 'imap.example.com',
    port: 993,
    secure: true,
    auth: { user: 'user@example.com', pass: 'password' }
});

await client.connect();

let lock = await client.getMailboxLock('INBOX');
try {
    // Fetch latest message
    let msg = await client.fetchOne(client.mailbox.exists, { source: true });
    console.log(msg.source.toString());

    // Stream all messages
    for await (let msg of client.fetch('1:*', { envelope: true })) {
        console.log(`${msg.uid}: ${msg.envelope.subject}`);
    }
} finally {
    lock.release();
}

await client.logout();
```

## Core Tasks

### 1. Connecting

```js
const client = new ImapFlow({
    host: 'imap.example.com',
    port: 993,
    secure: true,
    auth: { user: 'user@example.com', pass: 'password' }
});
await client.connect();
```

**Provider-specific configs** → See [references/connection.md](references/connection.md) for Gmail, Outlook, Yahoo, iCloud, and other common providers.

**OAuth2 / XOAUTH2:**
```js
auth: {
    user: 'user@gmail.com',
    accessToken: 'ya29.xxx...'
}
```

**Common options:**
- `logger`: Pass a logger object (`console`, pino, etc.) for debug output. Set `logger: false` to disable.
- `emitLogs`: Set `true` to emit 'log' events instead of using a logger.
- `clientInfo`: Custom client identification `{ name: 'myapp', version: '1.0.0' }`.
- `disableAutoIdle`: Disable automatic IDLE when mailbox is selected.

**Disconnect:** Call `client.logout()` for graceful disconnect. Handle `client.close()` for abrupt close.

### 2. Fetching Messages

**Always acquire a mailbox lock before fetching:**
```js
let lock = await client.getMailboxLock('INBOX');
try {
    // ... fetch operations ...
} finally {
    lock.release();
}
```

**Fetch one message:**
```js
let msg = await client.fetchOne('*', { source: true });
// or by sequence number: client.fetchOne(42, { source: true })
// or by UID (append `uid` flag):
let msg = await client.fetchOne('12345', { uid: true, source: true });
```

**Fetch query options** (what data to retrieve — choose only what you need):
- `source` — Full RFC822 message source (as Buffer)
- `envelope` — Parsed envelope (subject, from, to, date, message-id)
- `bodyStructure` — MIME structure tree
- `flags` — Array of flags (\\Seen, \\Answered, etc.)
- `internalDate` — Internal server date
- `size` — Message size in bytes
- `uid` — UID (always included)
- `threadId` — THREAD=ORDEREDSUBJECT reference (Gmail)
- `labels` — Gmail labels (X-GM-LABELS)
- `headers` — Raw headers as Buffer
- `bodyParts` — Array of MIME part paths to fetch, e.g. `['1.1', '1.2']`

**Stream/iterate messages:**
```js
// Range: sequence numbers
for await (let msg of client.fetch('1:100', { envelope: true, flags: true })) {
    console.log(`${msg.seq}: ${msg.envelope.subject}`);
}

// All messages: '1:*'
for await (let msg of client.fetch('1:*', { envelope: true })) { /* ... */ }

// By UID range
for await (let msg of client.fetch('1000:2000', { uid: true, envelope: true })) { /* ... */ }
```

**Fetch specific body parts:**
```js
let msg = await client.fetchOne('*', {
    bodyParts: ['1.1', '1.2'],  // MIME part paths
    source: true
});
// msg.bodyParts.get('1.1') → Buffer
// msg.text.toString() → decoded text content
```

**Download attachments:**
```js
let msg = await client.fetchOne('*', { source: true, bodyStructure: true });
for (let attachment of msg.attachments) {
    let buf = await client.download(msg.uid, attachment.part, { uid: true });
    // buf contains the attachment data
}
```

**Common envelope fields:** `msg.envelope.subject`, `msg.envelope.from[0].address`, `msg.envelope.to[0].address`, `msg.envelope.date`, `msg.envelope.messageId`, `msg.envelope.inReplyTo`.

### 3. Searching

```js
let lock = await client.getMailboxLock('INBOX');
try {
    // Simple search
    let list = await client.search({ unseen: true });

    // Complex query
    let list = await client.search({
        from: 'sender@example.com',
        subject: 'invoice',
        seen: false,
        since: new Date('2024-01-01'),
        before: new Date('2024-12-31'),
        larger: 1024 * 1024  // > 1MB
    });

    // Text search (body)
    let list = await client.search({ body: 'important keyword' });

    // Combine with OR
    let list = await client.search({
        or: [
            { from: 'alice@example.com' },
            { from: 'bob@example.com' }
        ]
    });

    // Combine AND + OR
    let list = await client.search({
        subject: 'report',
        or: [
            { from: 'alice@example.com' },
            { from: 'bob@example.com' }
        ]
    });

    // List is an array of sequence numbers. Use fetch() with those:
    for await (let msg of client.fetch(list, { envelope: true })) {
        console.log(msg.envelope.subject);
    }
} finally {
    lock.release();
}
```

**Search keys** → See [references/searching.md](references/searching.md) for the full IMAP search key reference.

**Gmail raw search (X-GM-RAW):**
```js
let list = await client.search({ 'x-gm-raw': 'has:attachment larger:10M' });
```

### 4. Mailbox Management

```js
// List all mailboxes
let mailboxes = await client.list();
for (let mb of mailboxes) {
    console.log(`${mb.name} (${mb.path})`);
}
// Filter by pattern: client.list({ path: 'INBOX/*' })

// Status (message count, unseen, etc.)
let status = await client.status('INBOX', { messages: true, unseen: true, uidNext: true });
console.log(`${status.messages} total, ${status.unseen} unseen`);

// Mailbox info (when a mailbox is selected)
console.log(client.mailbox.exists);    // total messages
console.log(client.mailbox.uidNext);   // next predicted UID (CONDSTORE)
console.log(client.mailbox.uidValidity);

// Create / Rename / Delete
await client.mailboxCreate('Projects/NewProject');
await client.mailboxRename('Projects/Old', 'Projects/New');
await client.mailboxDelete('Projects/Archive');

// Subscribe / Unsubscribe
await client.mailboxSubscribe('INBOX/Newsletters');
await client.mailboxUnsubscribe('INBOX/Newsletters');

// Move messages
await client.messageMove('1:5', 'Archive', { uid: false });
// Copy messages
await client.messageCopy('100:200', 'Important', { uid: true });

// Delete messages (set \Deleted flag + expunge)
await client.messageDelete('1:10');
// Or manually: flag + expunge
await client.messageFlagsAdd('1:10', ['\\Deleted']);
await client.messageExpunge('1:10');  // or expunge all: client.mailboxExpunge()
```

### 5. IDLE (Push Notifications)

ImapFlow automatically enters IDLE when there's an active mailbox lock and no pending commands. Use events to react to new messages:

```js
client.on('exists', async (data) => {
    console.log(`New messages! Count: ${data.count}`);
    // Fetch new messages
    let lock = await client.getMailboxLock('INBOX');
    try {
        for await (let msg of client.fetch(`${data.prevCount + 1}:${data.count}`, { envelope: true })) {
            console.log(`New: ${msg.envelope.subject}`);
        }
    } finally {
        lock.release();
    }
});

client.on('expunge', (data) => {
    console.log(`Message seq#${data.seq} was deleted`);
});

client.on('flags', (data) => {
    console.log(`Flags changed for seq#${data.seq}: ${data.flags}`);
});

// Connect and select mailbox — IDLE starts automatically
await client.connect();
let lock = await client.getMailboxLock('INBOX');
// Keep lock active — IDLE runs in background
```

**Manual IDLE control:**
```js
client.on('idle', () => console.log('Entered IDLE'));
// To disable auto-IDLE: new ImapFlow({ disableAutoIdle: true })
```

### 6. Gmail-Specific Operations

```js
// Gmail labels
let msg = await client.fetchOne('*', { labels: true });
console.log(msg.labels); // ['\\Inbox', 'Important', 'Starred']

// Set labels
await client.messageFlagsAdd('1', ['\\Starred', 'Important'], { uid: true });
await client.messageFlagsRemove('100', ['Important'], { uid: true });
await client.messageFlagsSet('42', ['\\Inbox', 'CustomLabel'], { uid: true });

// Gmail raw search
let results = await client.search({ 'x-gm-raw': 'from:alice has:attachment newer_than:7d' });

// Gmail thread ID
let msg = await client.fetchOne('*', { threadId: true });
console.log(msg.threadId); // Gmail thread identifier
```

Gmail connection config:
```js
new ImapFlow({
    host: 'imap.gmail.com',
    port: 993,
    secure: true,
    auth: {
        user: 'user@gmail.com',
        accessToken: 'oauth2-token'  // Use OAuth2
    }
})
```

> **Note:** Gmail requires OAuth2 or App Passwords. Regular passwords won't work unless "Less secure app access" is enabled (deprecated).

### 7. Error Handling & Reconnection

**Connection events:**
```js
client.on('error', (err) => {
    console.error('IMAP error:', err.message);
    // Connection is likely closed after a fatal error
});

client.on('close', () => {
    console.log('Connection closed');
    // Reconnect logic here
});

client.on('connectionError', (err) => {
    console.error('Connection failed:', err.message);
});
```

**Reconnection pattern:**
```js
async function connectWithRetry(config, maxRetries = 5) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const client = new ImapFlow(config);
            await client.connect();
            return client;
        } catch (err) {
            console.error(`Connection attempt ${i + 1} failed: ${err.message}`);
            if (i < maxRetries - 1) {
                await new Promise(r => setTimeout(r, Math.min(1000 * Math.pow(2, i), 30000)));
            }
        }
    }
    throw new Error('All connection attempts failed');
}
```

**Mailbox locking best practices:**
- Always use `try/finally` to release locks
- Keep lock durations short — release between operations when possible
- Never hold a lock across network calls or long async operations
- Use separate locks for read vs write operations when safe

```js
// BAD: lock held too long
let lock = await client.getMailboxLock('INBOX');
let results = await client.search({ unseen: true });
// ... process results (slow, lock held) ...
lock.release();

// GOOD: release lock between operations
let results;
{
    let lock = await client.getMailboxLock('INBOX');
    results = await client.search({ unseen: true });
    lock.release();
}
// Process results without holding lock
for (let seq of results) { /* ... */ }
```

**Timeouts and connection health:**
```js
// No operation timeout (blocks forever) — set one
const timeout = setTimeout(() => client.close(), 30000);
// ... your operation ...
clearTimeout(timeout);

// Check if connected: client.usable → true/false
```

## Reference Files

- **[connection.md](references/connection.md)** — Provider-specific connection configs: Gmail, Outlook/Hotmail, Yahoo, iCloud, Zoho, Fastmail, custom servers. Includes TLS, OAuth2, App Passwords, and proxy setup.
- **[searching.md](references/searching.md)** — Complete IMAP search key reference: flags, dates, sizes, headers, text searches, logical operators, sequence sets, Gmail raw search.
- **[api_reference.md](references/api_reference.md)** — Key API methods summary: client methods, events, MailboxLock, FetchQueryObject options, and ImapFlow constructor options.