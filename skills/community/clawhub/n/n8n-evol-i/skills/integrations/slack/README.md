---
name: integration-slack
description: Slack nodes — bot/user OAuth, posting messages, threads, error-notification Block Kit pattern.
user-invocable: false
---

# Slack

## Node type

`n8n-nodes-base.slack`.

## Credential type

`slackApi` (bot token) or `slackOAuth2Api` (full OAuth flow).

For setup, see [`skills/manage-credentials.md`](../../manage-credentials.md). Bot tokens (`slackApi`) are simpler — paste `xoxb-...` into `.env.<env>` and run Path A.

## Common operations

- **Post message:** `resource: message`, `operation: post`. Set `channel` to a channel ID (preferred) or `#name` (sometimes resolves slowly).
- **Reply in thread:** include `thread_ts` from a previous message.
- **Update message:** `operation: update` with `ts` of the original message.

## Channel ID gotcha

Slack's UI shows `#channel-name` but the API takes channel IDs (e.g. `C0123456789`). Find the ID by right-clicking the channel → Copy Link → the URL contains the ID. Store the ID in your env YAML, not the name:

```yaml
slack:
  alertsChannel: "C0123456789"
```

```json
{
  "type": "n8n-nodes-base.slack",
  "parameters": {
    "channel": "{{@env:slack.alertsChannel}}"
  }
}
```

## Error-notification worked example

Used inside an n8n error handler, fed by the `Build Context` Code node from [`patterns/error-handling.md`](../../patterns/error-handling.md). Posts a Block Kit message to the alerts channel + captures the response so a downstream node can thread updates onto it.

```json
{
  "type": "n8n-nodes-base.slack",
  "typeVersion": 2.3,
  "parameters": {
    "resource": "message",
    "operation": "post",
    "select": "channel",
    "channelId": {
      "__rl": true,
      "value": "{{@env:slack.alertsChannel}}",
      "mode": "id"
    },
    "messageType": "block",
    "blocksUi": "={{ JSON.stringify({ blocks: [\n  { type: 'header', text: { type: 'plain_text', text: ':rotating_light: Workflow failed: ' + $json.workflow_name } },\n  { type: 'section', fields: [\n    { type: 'mrkdwn', text: '*Workflow:*\\n' + $json.workflow_name },\n    { type: 'mrkdwn', text: '*Last node:*\\n`' + ($json.last_node || 'unknown') + '`' },\n    { type: 'mrkdwn', text: '*Env:*\\n' + ($env.N8N_ENV || 'unknown') },\n    { type: 'mrkdwn', text: '*When:*\\n' + $json.timestamp }\n  ]},\n  { type: 'section', text: { type: 'mrkdwn', text: '*Error message:*\\n```\\n' + $json.message + '\\n```' } },\n  { type: 'actions', elements: [\n    { type: 'button', text: { type: 'plain_text', text: 'Open in n8n' }, url: $json.execution_url || 'https://n8n.example.com', style: 'primary' }\n  ]}\n]}) }}",
    "otherOptions": {}
  },
  "credentials": {
    "slackApi": {
      "id": "{{@env:credentials.slack.id}}",
      "name": "{{@env:credentials.slack.name}}"
    }
  }
}
```

The `messageType: block` mode tells the Slack node to send Block Kit JSON in the `blocksUi` field. The Block Kit structure shipped above is:

- A `header` block with the rotating-light emoji + workflow name (large, can't-miss-it).
- A `section` with `fields` showing workflow / last-node / env / timestamp in a 2-column grid.
- A second `section` with the error message in a fenced code block.
- An `actions` row with a primary button linking to the n8n execution URL.

Slack's response includes `ts` (the message timestamp) — capture it via `$json.ts` for thread updates:

```javascript
// In a downstream node referencing the Slack post output:
const threadTs = $('Slack Post').first().json.ts;
```

## Threading updates onto the original alert

When the cleanup step finishes (lock released, DB invalidated, etc.), reply in-thread on the original alert so on-call sees the resolution without a second top-level message:

```json
{
  "type": "n8n-nodes-base.slack",
  "typeVersion": 2.3,
  "parameters": {
    "resource": "message",
    "operation": "post",
    "select": "channel",
    "channelId": {
      "__rl": true,
      "value": "{{@env:slack.alertsChannel}}",
      "mode": "id"
    },
    "text": "={{ ':white_check_mark: Cleanup complete: ' + $json.cleanup_summary }}",
    "otherOptions": {
      "thread_ts": "={{ $('Slack Post').first().json.ts }}"
    }
  }
}
```

This keeps the alerts channel readable: one top-level :rotating_light: per incident, replies-in-thread for status updates.

## See also

- [`patterns/error-handling.md`](../../patterns/error-handling.md) — three-step paradigm; this Slack post is the "log to humans" step.
- [`manage-credentials.md`](../../manage-credentials.md) — registering the slackApi credential.
