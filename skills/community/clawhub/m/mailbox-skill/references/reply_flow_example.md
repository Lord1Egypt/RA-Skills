Execution steps:

1. Read the incoming inbox message.

2. Read and record the incoming routing metadata. Record the current inbox message path as `ORIGINAL_INBOX_MESSAGE_PATH`. Record `RECEIVER_INBOX_PATH` as `ORIGINAL_RECEIVER_INBOX_PATH`. Record `REPLY_INBOX_PATH` as `ORIGINAL_REPLY_INBOX_PATH` for the later delivery step. Verify that the destination directory for `ORIGINAL_REPLY_INBOX_PATH` exists. If it does not exist, you may stop and not send the reply.

```bash
test -d "$(dirname "$ORIGINAL_REPLY_INBOX_PATH")"
```

3. Keep the original `REQUEST_ID`.

4. If the incoming message has `CHANNEL_ID`, preserve that same `CHANNEL_ID` in the reply.

5. Set `RECEIVER_INBOX_PATH` in the reply to `ORIGINAL_REPLY_INBOX_PATH`.

6. Set `REPLY_INBOX_PATH` in the reply only if you want the conversation to continue. When you set it, it should be `ORIGINAL_RECEIVER_INBOX_PATH`, which is this agent's own inbox path from the incoming message.

7. Draft the reply as a complete mailbox message in your local scratch file:

```md
---
REQUEST_ID: [ORIGINAL REQUEST_ID]
MESSAGE_TYPE: REPLY
CHANNEL_ID: [ORIGINAL CHANNEL_ID IF PRESENT]
RECEIVER_INBOX_PATH: [ORIGINAL_REPLY_INBOX_PATH]
REPLY_INBOX_PATH: [ORIGINAL_RECEIVER_INBOX_PATH IF FOLLOW-UP IS WANTED]
---

[YOUR REPLY TO THE ORIGINAL MESSAGE]
```

8. Save that complete reply message to your private scratch path:

```text
./.mailbox/scratch/$REQUEST_ID
```

9. Deliver the reply by copying the completed scratch file to `ORIGINAL_REPLY_INBOX_PATH`:

```bash
cp ./.mailbox/scratch/$REQUEST_ID "$ORIGINAL_REPLY_INBOX_PATH"
```

10. After delivery, delete `ORIGINAL_INBOX_MESSAGE_PATH`, but keep the scratch reply message for future reference or audit.

11. Do not print the final delivered reply to the terminal.
