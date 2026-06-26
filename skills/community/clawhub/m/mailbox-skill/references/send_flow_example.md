Execution steps:

1. Generate a new `REQUEST_ID`, for example:

```bash
uuidgen | tr 'A-Z' 'a-z' | tr -d '-'
```

2. Find the destination inbox folder for the target agent and record it as `TARGET_AGENT_INBOX_FOLDER`. Then set `TARGET_AGENT_INBOX_PATH` to the final message path inside that folder.

   Guidance:
   - If the target agent inbox folder was given explicitly, use that folder.
   - If the workspace documents another agent's mailbox path in Markdown, use that documented inbox folder.
   - If you only know the other agent workspace, derive the inbox folder as `<target agent workspace>/.mailbox/inbox/`.
   - Then set `TARGET_AGENT_INBOX_PATH` to `TARGET_AGENT_INBOX_FOLDER/<request_id>`.
   - If you cannot determine a valid target inbox folder, stop and do not send the message.

3. Verify that `TARGET_AGENT_INBOX_FOLDER` exists. If it does not exist, you may stop and not send the message.

```bash
test -d "$TARGET_AGENT_INBOX_FOLDER"
```

4. If the new message belongs to an existing channel or thread, decide the `CHANNEL_ID`. Otherwise you may omit it.

5. Set `RECEIVER_INBOX_PATH` in the new message to `TARGET_AGENT_INBOX_FOLDER/$REQUEST_ID`.

6. Set `REPLY_INBOX_PATH` in the new message to this agent's own absolute inbox path with the same `REQUEST_ID` if you want a reply.
   Example: `$(pwd)/.mailbox/inbox/$REQUEST_ID`

7. Draft the new message as a complete mailbox message in your local scratch file:

```md
---
REQUEST_ID: [NEW REQUEST_ID]
MESSAGE_TYPE: NEW
CHANNEL_ID: [OPTIONAL CHANNEL_ID]
RECEIVER_INBOX_PATH: [TARGET_AGENT_INBOX_PATH]
REPLY_INBOX_PATH: [THIS_AGENT_ABSOLUTE_INBOX_PATH_WITH_REQUEST_ID]
---

[YOUR NEW MESSAGE TO THE TARGET AGENT]
```

8. Save that complete new message to your private scratch path:

```text
./.mailbox/scratch/$REQUEST_ID
```

9. Deliver the message by copying the completed scratch file to `TARGET_AGENT_INBOX_PATH`:

```bash
cp ./.mailbox/scratch/[NEW REQUEST_ID] "$TARGET_AGENT_INBOX_PATH"
```

10. Keep the scratch message for future reference or audit.

11. Do not print the final delivered message to the terminal.
