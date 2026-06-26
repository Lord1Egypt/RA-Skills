# IMAP Search Key Reference

ImapFlow's `client.search()` accepts a search object with the following keys. Multiple keys are combined with AND by default. Use `or` for OR logic.

## Flag Searches

| Key | Description |
|-----|-------------|
| `answered` | Messages with \\Answered flag |
| `deleted` | Messages with \\Deleted flag |
| `draft` | Messages with \\Draft flag |
| `flagged` | Messages with \\Flagged flag |
| `seen` | Messages with \\Seen flag |
| `unseen` | Messages without \\Seen flag |
| `unanswered` | Messages without \\Answered flag |
| `undeleted` | Messages without \\Deleted flag |
| `undraft` | Messages without \\Draft flag |
| `unflagged` | Messages without \\Flagged flag |
| `new` | Messages with \\Recent and not \\Seen |
| `old` | Messages without \\Recent |
| `recent` | Messages with \\Recent flag |
| `keyword` | Messages with a custom flag keyword |
| `unkeyword` | Messages without a custom flag keyword |

```js
await client.search({ unseen: true });              // Unread messages
await client.search({ seen: false });                // Same: unread
await client.search({ flagged: true });             // Starred/flagged
await client.search({ seen: true, flagged: true });  // Read AND flagged (AND)
await client.search({ keyword: '$Forwarded' });      // Custom keyword
```

## Date Searches

| Key | Description |
|-----|-------------|
| `before` | Internal date before this date |
| `on` | Internal date on this exact date |
| `since` | Internal date on or after this date |
| `sentBefore` | Date header before this date |
| `sentOn` | Date header on this exact date |
| `sentSince` | Date header on or after this date |

```js
await client.search({ since: new Date('2024-06-01') });
await client.search({ before: new Date('2024-06-30') });
await client.search({ since: new Date('2024-01-01'), before: new Date('2024-12-31') });
await client.search({ sentSince: new Date('2024-06-01') });  // Sent date, not received
```

## Size Searches

| Key | Description |
|-----|-------------|
| `larger` | Messages larger than N bytes |
| `smaller` | Messages smaller than N bytes |

```js
await client.search({ larger: 1024 * 1024 });   // > 1MB
await client.search({ smaller: 50 * 1024 });     // < 50KB
```

## Header / Address Searches

| Key | Description |
|-----|-------------|
| `bcc` | BCC header contains string |
| `cc` | CC header contains string |
| `from` | From header contains string |
| `to` | To header contains string |
| `subject` | Subject header contains string |
| `header` | Custom header search: `{ key: 'List-Unsubscribe', value: 'yes' }` |

```js
await client.search({ from: 'alice@example.com' });
await client.search({ subject: 'invoice' });
await client.search({ to: 'support@example.com' });
await client.search({ cc: 'manager@example.com' });
await client.search({ header: ['List-Unsubscribe', 'yes'] });
```

## Body / Text Searches

| Key | Description |
|-----|-------------|
| `body` | Message body contains text (full text search) |
| `text` | Message body OR subject contains text |

```js
await client.search({ body: 'urgent meeting' });
await client.search({ text: 'invoice payment' });
```

> **Note:** Body/text search is server-dependent. Not all servers index message bodies efficiently. Gmail is fast; other servers may be slow on large mailboxes.

## Sequence / UID Searches

| Key | Description |
|-----|-------------|
| `seq` | By sequence number(s) |
| `uid` | By UID(s) |

```js
await client.search({ seq: '1:100' });       // Messages by sequence number
await client.search({ uid: '1000:2000' });    // Messages by UID
```

## Modseq (CONDSTORE)

| Key | Description |
|-----|-------------|
| `modseq` | Messages modified since a given MODSEQ value |

```js
await client.search({ modseq: 12345n });  // Use BigInt for large MODSEQ values
```

## Gmail Extensions (X-GM-EXT-1)

| Key | Description |
|-----|-------------|
| `'x-gm-msgid'` | Gmail message ID |
| `'x-gm-thrid'` | Gmail thread ID |
| `'x-gm-raw'` | Gmail raw search query (same syntax as Gmail search box) |
| `'x-gm-labels'` | Has specific Gmail label(s) |

```js
// Gmail raw search (uses Gmail's native search syntax)
await client.search({ 'x-gm-raw': 'has:attachment larger:10M' });
await client.search({ 'x-gm-raw': 'from:alice subject:report newer_than:7d' });
await client.search({ 'x-gm-raw': 'in:inbox is:unread category:primary' });

// By Gmail thread ID
await client.search({ 'x-gm-thrid': '1234567890123456789' });

// By Gmail label
await client.search({ 'x-gm-labels': 'Important' });
```

## Logical Operators

### OR Operator

```js
// Messages from alice OR bob
await client.search({
    or: [
        { from: 'alice@example.com' },
        { from: 'bob@example.com' }
    ]
});
```

### NOT Operator

Use negative keys (e.g., `seen: false`) instead of explicit NOT:
```js
await client.search({ seen: false });           // NOT seen
await client.search({ keyword: false });         // No custom keyword
```

### Combining AND + OR

```js
await client.search({
    subject: 'report',          // AND
    seen: false,                // AND
    or: [                       // AND (OR)
        { from: 'alice@example.com' },
        { from: 'bob@example.com' }
    ],
    since: new Date('2024-01-01')  // AND
});
```

## Sequence Sets

When fetching by results, use the returned sequence numbers:

```js
let seqs = await client.search({ unseen: true, since: new Date('2024-01-01') });
// seqs is an array: [1, 3, 5, 7]

// Fetch those messages
for await (let msg of client.fetch(seqs, { envelope: true })) {
    console.log(msg.envelope.subject);
}
```

For UID-based operations, pass `{ uid: true }`:
```js
let uids = await client.search({ unseen: true }, { uid: true });
await client.messageFlagsAdd(uids, ['\\Seen'], { uid: true });
```

## Performance Tips

1. **Prefer flag/header searches over body searches** — they're faster and server-indexed.
2. **Limit date ranges** — searching a year of email is slower than searching a week.
3. **Use Gmail raw search on Gmail** — `x-gm-raw` uses Gmail's optimized search engine.
4. **Combine criteria** — the more specific the search, the fewer results to process.
5. **UID-based operations are preferred** when available — UIDs are stable while sequence numbers change.