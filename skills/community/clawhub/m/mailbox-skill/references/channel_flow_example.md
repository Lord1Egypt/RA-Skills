Execution steps:

1. Read the pending inbox messages and group them by `CHANNEL_ID` when present.

2. For one `CHANNEL_ID`, sort or inspect the pending messages in arrival order and identify:
   - the latest pending message in that channel
   - any older pending messages in that same channel that were superseded by the latest one

3. You may use all messages in that `CHANNEL_ID` to understand the full context.

4. Create a full reply only for the latest pending message in that `CHANNEL_ID`.

5. For each older superseded pending message in that same `CHANNEL_ID`, still create a valid `REPLY` mailbox message, but use the minimal empty reply body:

```md
---
REQUEST_ID: [OLDER REQUEST_ID]
MESSAGE_TYPE: REPLY
CHANNEL_ID: [SHARED CHANNEL_ID]
RECEIVER_INBOX_PATH: [OLDER ORIGINAL_REPLY_INBOX_PATH]
REPLY_INBOX_PATH: [OLDER ORIGINAL_RECEIVER_INBOX_PATH IF FOLLOW-UP IS WANTED]
---
""
```

6. Draft each reply message in a separate scratch file first.

7. Deliver each reply by copying its completed scratch file to that message's destination reply inbox path.

8. Do not ignore older superseded pending messages in the same `CHANNEL_ID`. They still require delivery of a valid `REPLY` mailbox message, even when the body is `""`.

9. After delivery, delete each processed inbox message and keep the scratch messages for future reference or audit.

10. Do not print the final delivered replies to the terminal.