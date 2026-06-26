# ImapFlow API Reference

## ImapFlow Constructor

```js
const { ImapFlow } = require('imapflow');
const client = new ImapFlow(options);
```

### Constructor Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `host` | string | (required) | IMAP server hostname |
| `port` | number | 993 | IMAP server port |
| `secure` | boolean | true | Use TLS (true=993, false=143) |
| `auth` | object | (required) | `{ user, pass }` or `{ user, accessToken }` |
| `logger` | object/false | — | Logger instance (pino, console, etc.); `false` to disable |
| `emitLogs` | boolean | false | Emit 'log' events instead of using logger |
| `clientInfo` | object | — | `{ name, version }` sent in ID command |
| `disableAutoIdle` | boolean | false | Disable automatic IDLE when mailbox selected |
| `tls` | object | — | `{ rejectUnauthorized, ca, servername, ... }` |
| `proxy` | object | — | `{ host, port, protocol, auth }` for SOCKS/HTTP proxy |

### Debug / Logging Events

```js
// Option 1: logger object
new ImapFlow({ host: '...', auth: {...}, logger: console });

// Option 2: emit events
new ImapFlow({ host: '...', auth: {...}, emitLogs: true });
client.on('log', (entry) => {
    console.log(`${entry.level}: ${entry.msg}`);
    // entry: { level, msg, cid, tid, t }
});
```

## Client Methods

### Connection

| Method | Returns | Description |
|--------|---------|-------------|
| `connect()` | Promise | Connect to server, authenticate, and negotiate capabilities |
| `logout()` | Promise | Gracefully close connection |
| `close()` | void | Force close connection immediately |

### Mailbox Selection & Locking

| Method | Returns | Description |
|--------|---------|-------------|
| `getMailboxLock(path, [options])` | Promise\<MailboxLock\> | Select mailbox and acquire exclusive lock |
| `mailboxOpen(path, [options])` | Promise\<Mailbox\> | Select mailbox without locking (use with caution) |
| `mailboxClose()` | Promise | Unselect current mailbox |

```js
let lock = await client.getMailboxLock('INBOX');
try {
    // ... operations ...
} finally {
    lock.release();
}
```

### Mailbox Info (on `client.mailbox`)

| Property | Description |
|----------|-------------|
| `mailbox.path` | Mailbox path |
| `mailbox.exists` | Number of messages |
| `mailbox.uidNext` | Next predicted UID |
| `mailbox.uidValidity` | UID validity value |
| `mailbox.highestModseq` | Highest MODSEQ (CONDSTORE) |

### Fetching

| Method | Returns | Description |
|--------|---------|-------------|
| `fetch(range, query, [options])` | AsyncIterable\<FetchMessageObject\> | Fetch multiple messages |
| `fetchOne(seq, query, [options])` | Promise\<FetchMessageObject\> | Fetch single message |
| `download(uid, part, [options])` | Promise\<Buffer\> | Download message/attachment by UID |

**Range formats:** `'1:100'` (sequence numbers), `'1000:2000'` (with `uid: true`), `[1, 3, 5]` (array from search).

**FetchQueryObject fields:** `source`, `envelope`, `bodyStructure`, `flags`, `internalDate`, `size`, `uid`, `threadId`, `labels`, `headers`, `bodyParts`.

**Download options:** `{ uid: true, maxBytes: 1048576, chunkSize: 65536 }`.

### Searching

| Method | Returns | Description |
|--------|---------|-------------|
| `search(query, [options])` | Promise\<number[]\> | Search and return sequence numbers |

**Options:** `{ uid: true }` to return UIDs instead of sequence numbers.

### Message Manipulation

| Method | Description |
|--------|-------------|
| `messageFlagsAdd(range, flags, [options])` | Add flags (e.g., `['\\Seen']`) |
| `messageFlagsRemove(range, flags, [options])` | Remove flags |
| `messageFlagsSet(range, flags, [options])` | Replace all flags |
| `messageMove(range, mailbox, [options])` | Move messages to another mailbox |
| `messageCopy(range, mailbox, [options])` | Copy messages to another mailbox |
| `messageDelete(range, [options])` | Delete messages (\\Deleted + expunge) |
| `messageExpunge(range, [options])` | Expunge specific messages |

**Range formats:** sequence numbers, UIDs (with `uid: true`), or `'1:*'`.
**Common flags:** `\\Seen`, `\\Answered`, `\\Flagged`, `\\Deleted`, `\\Draft`, plus custom keywords.

### Mailbox Management

| Method | Description |
|--------|-------------|
| `list([query])` | List mailboxes |
| `status(path, query)` | Get mailbox status (messages, unseen, uidNext, etc.) |
| `mailboxCreate(path)` | Create mailbox |
| `mailboxRename(from, to)` | Rename mailbox |
| `mailboxDelete(path)` | Delete mailbox |
| `mailboxSubscribe(path)` | Subscribe to mailbox |
| `mailboxUnsubscribe(path)` | Unsubscribe from mailbox |
| `mailboxExpunge()` | Expunge all deleted messages in current mailbox |

### Utility

| Method | Returns | Description |
|--------|---------|-------------|
| `getQuota(path)` | Promise\<Quota\> | Get mailbox quota information |
| `append(path, content, flags, [date])` | Promise\<AppendResult\> | Append a message to a mailbox |
| `idle()` | Promise | Enter IDLE mode manually |

```js
// Append a message
await client.append('INBOX', rawMessageBuffer, ['\\Seen'], new Date());

// Get quota
let quota = await client.getQuota('INBOX');
// quota.storage: { used, limit } (in KB)
```

### Properties

| Property | Description |
|----------|-------------|
| `client.usable` | `true` if connection is authenticated and usable |
| `client.authenticated` | `true` if authenticated |
| `client.mailbox` | Current selected mailbox info (null if none) |
| `client.capabilities` | Map of server capabilities (Map\<string, boolean\|string\>) |
| `client.enabled` | Set of enabled capabilities |

## Events

| Event | Data | Description |
|-------|------|-------------|
| `exists` | `{ count, prevCount }` | New messages arrived |
| `expunge` | `{ seq }` | Message deleted |
| `flags` | `{ seq, flags, uid }` | Message flags changed |
| `mailbox` | `{ path }` | Mailbox opened/closed |
| `close` | — | Connection closed |
| `error` | `Error` | Protocol-level error |
| `connectionError` | `Error` | TCP/TLS connection error |
| `idle` | — | Entered IDLE mode |
| `log` | `{ level, msg, cid, tid, t }` | Log event (when `emitLogs` is true) |
| `update` | `{ path, exists, uidNext, ... }` | STATUS update for a watched mailbox |

## MailboxLock

Returned by `client.getMailboxLock()`. Provides exclusive access to a mailbox.

```js
let lock = await client.getMailboxLock('INBOX');
try {
    // Operations on INBOX
} finally {
    lock.release();
}
```

**Methods:** `lock.release()` — release the lock and unselect the mailbox.

**Important:** The lock ensures exclusive access. Only one active lock per mailbox at a time. Release immediately when done.

## FetchMessageObject

Returned by `fetch()` and `fetchOne()`.

| Property | Type | Description |
|----------|------|-------------|
| `seq` | number | Sequence number |
| `uid` | number | UID |
| `source` | Buffer | Full message source (when `source: true`) |
| `envelope` | object | Parsed envelope (when `envelope: true`) |
| `bodyStructure` | object | MIME structure (when `bodyStructure: true`) |
| `flags` | Set\<string\> | Message flags |
| `internalDate` | Date | Internal date |
| `size` | number | Message size in bytes |
| `threadId` | string | Gmail thread ID |
| `labels` | Set\<string\> | Gmail labels |
| `headers` | Buffer | Raw headers |
| `bodyParts` | Map\<string, Buffer\> | Requested body parts |
| `text` | object | Decoded text parts (when available) |
| `attachments` | object[] | Attachment metadata (when bodyStructure fetched) |

**Envelope fields:** `date`, `subject`, `from`, `sender`, `replyTo`, `to`, `cc`, `bcc`, `inReplyTo`, `messageId`.

Each address field is an array of `{ name, address }` objects.

## List / Status Results

```js
// client.list() → MailboxListItem[]
// { path, name, delimiter, flags, listed, subscribed, specialUse, ... }

// client.status() → StatusObject
// { path, messages, recent, unseen, uidNext, uidValidity, ... }
```

## Stream Fetch Pattern

```js
// Recommended: stream process to limit memory usage
let lock = await client.getMailboxLock('INBOX');
try {
    for await (let msg of client.fetch('1:*', { envelope: true, uid: true })) {
        // Process one message at a time
        console.log(`${msg.uid}: ${msg.envelope.subject}`);
    }
} finally {
    lock.release();
}
```