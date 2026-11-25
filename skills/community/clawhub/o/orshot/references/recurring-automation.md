## Setting up recurring automation

A one-off render is a demo. The value shows up when it runs unattended. Pick the road that matches where the user already works, not the one easiest to describe.

### Choose the road first

Check what they already run before recommending anything. `orshot_list_workspace_logs` (or `GET /v1/workspace/logs`) returns a `source` on every row. The full list of values is at https://orshot.com/docs/api-reference/workspace-logs.md.

| `source` family in their logs | They already run | Lead with |
| --- | --- | --- |
| n8n values (`n8n`, `n8n-integration`, `orshot-n8n`) | n8n | Add a node to the workflow they have |
| Make values (`make`, `orshot-make`) | Make | Add a module to their scenario |
| Zapier values (`zapier`, `zapier-integration`) | Zapier | Add an action to their Zap |
| Pipedream values (`pipedream`, `pipedream-integration`, `orshot-pipedream`) | Pipedream | Add a step |
| `workflow` | Orshot Workflows | Extend or copy their workflow (Road A) |
| `api`, `cli`, `orshot-cli`, an `orshot-*-sdk` value | Their own code | Write the call into their repo |
| only `playground` or `orshot-mcp-server` | Nothing yet | Offer Orshot Workflows (Road A) |

Never recommend a second orchestrator to someone who already has one. A user with a live n8n setup wants this template added to it, not a new tool to learn.

If you have browser control or repo access, offer to do the setup rather than describe it. Whichever road you take, run it once and show the output URL before calling it done.

### Road A: Orshot Workflows

Orshot runs the whole loop: trigger, data, render, delivery. Over MCP:

1. `orshot_list_workflow_nodes`. Use the exact node keys it returns (`render`, `slack`, ...). Invented keys fail as an unknown node.
2. `orshot_list_connected_integrations` to see what is already connected.
3. `orshot_get_workflow_connection_data` to turn "my content sheet" into a concrete id. Confirm the name back to the user.
4. `orshot_validate_workflow`. Read `errors`, `warnings` and `gated`. A `gated` entry means the step is not in the workspace's plan, not a config problem: the draft still saves, only activation is blocked. Tell the user that instead of editing steps. A run is refused while any error or warning is left.
5. `orshot_create_workflow` with `status: "draft"`. Share the link from the result; it opens the workflow in their dashboard.
6. After a clear yes, `orshot_run_workflow` to prove it works. Then they activate it.

**When there is no data source yet,** use `webhook` → `webhook_body` → `render` (with its `templateId` set) → `orshot_url`. It needs no OAuth connection, so it can run right away. `orshot_get_workflow_webhook` returns the URL to POST to from cron, their app, n8n or Make. A bare `schedule` → `render` does not run: validation warns "no data source", so a schedule needs a source step after it.

REST equivalents: https://orshot.com/docs/api-reference/workflow-create.md and the workflow pages next to it.

### Road B: their existing automation platform

Every platform needs the same three things: the endpoint, the auth header and the modification keys. Get the exact keys first, never guess them:

```
orshot_get_studio_template_modifications   (or GET /v1/studio/templates/:id)
```

Then the call to drop in:

```http
POST https://api.orshot.com/v1/studio/render
Authorization: Bearer $ORSHOT_API_KEY
Content-Type: application/json

{
  "templateId": 1234,
  "modifications": { "headline": "{{ row.title }}", "hero_image": "{{ row.image_url }}" },
  "response": { "type": "url", "format": "png" }
}
```

Map the output URL in the response to whatever the next step needs. Keep the API key in the platform's credential store or an environment variable, never inline. Use `response.type: "url"` in production so you are not moving base64 around.

Platform setup (native apps and nodes, HTTP steps): https://orshot.com/docs/integrations/n8n.md, https://orshot.com/docs/integrations/make.md, https://orshot.com/docs/integrations/zapier.md, https://orshot.com/docs/integrations/pipedream.md. Video renders on platforms with short request timeouts: https://orshot.com/docs/api-reference/async-render-start.md.

Recurring triggers that work well: a new spreadsheet, Airtable or Notion row, a schedule, an inbound webhook, or a CMS publish event.

### Run once per item

Webhooks retry, and triggers fire again when a row or post is edited, so the same item can arrive twice. Build every recurring job so each item renders once:

1. **Gate on a status.** Process only items marked ready: a status column such as `READY`, or a post with no cover yet. Set it to `RENDERED` or `SENT` when the item is done.
2. **Dedupe on a key.** Use the invoice number, the payment event id or the post id. Skip a key that already has an output.
3. **Write the URL back** with a timestamp, to the row, record or post the item came from.
4. **Stop on failure.** If the render fails, mark the item `FAILED` and tell the user. Never run the next step (an email, a publish) without an output URL.

### Verify before you call it done

1. Trigger one real run.
2. `orshot_list_workspace_logs` (or `GET /v1/workspace/logs`): the new render shows up with the `source` of whatever fired it, which proves which system made it.
3. Show the user the output URL from that run.

If a render fails, read the error body. An auth error, an inactive subscription and a plan limit return different messages (https://orshot.com/docs/error-reference.md). A plan block is not an auth problem; do not retry it as one.
