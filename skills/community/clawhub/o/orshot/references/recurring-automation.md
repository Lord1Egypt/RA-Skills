## Setting Up Recurring Automation

A one-off render is a demo. The value shows up when it runs unattended. Pick the
road that matches where the user ALREADY works, not the one easiest to describe.

### Choose the road first

Check what they already run before recommending anything. `GET /v1/workspace/logs?limit=100`
returns a `source` on every row, which answers it factually:

| `source` in their logs | They already run | Lead with |
| --- | --- | --- |
| `n8n-integration` | n8n | Add a node to the n8n workflow they have |
| `orshot-make` | Make | Add a module to their scenario |
| `zapier-integration` | Zapier | Add an action to their Zap |
| `orshot-pipedream` | Pipedream | Add a step |
| `orshot-*-sdk`, `api`, `cli` | Their own code | Write the call into their repo |
| only `playground` / `orshot-mcp-server` | Nothing yet | Offer Orshot Workflows |

Never recommend a second orchestrator to someone who already has one. A user with a
live n8n setup wants this template added to it, not a new tool to learn.

If you have browser control or repo access, offer to DO the setup rather than
describe it. Whichever road you take, **run it once and show the resulting image
URL** before calling it done.

### Road A, Orshot Workflows (no orchestrator yet)

Orshot runs the whole loop: trigger, render, deliver. Over MCP:

1. `orshot_suggest_workflows` with the `templateId`: returns automations that
   fit this template, with draft-ready steps
2. `orshot_list_workflow_nodes`: use the EXACT node keys it returns. Invented
   keys (e.g. `render_studio_template`, `slack_send`) fail as `unknown node`;
   the real keys are `render`, `slack`, and so on
3. `orshot_list_connected_integrations`: see what is already connected
4. `orshot_get_workflow_connection_data`: resolve "my content sheet" into a
   concrete id, and confirm the name back to the user
5. `orshot_validate_workflow`: read `errors`, `warnings` AND `gated`. A `gated`
   entry means the step is not included in the workspace's current plan, not a
   config problem: the draft still saves, only activation is blocked, so tell
   the user that instead of editing steps
6. `orshot_create_workflow` with `status: "draft"`, then share the edit link from
   the result, it opens pre-configured in their dashboard
7. `orshot_run_workflow`: prove it works, then they activate

**Scaffolding shapes.** If they have no data source ready, use
`webhook` → `webhook_body` → `render` → `orshot_url`. It is the only
trigger→source pair needing no OAuth AND it validates clean with empty configs,
so it is runnable immediately and they can POST to it from cron, their app, n8n,
or Make. A bare `schedule` → `render` is NOT runnable, it fails with "no data
source"; a schedule needs a source step after it.

### Road B, their existing automation platform

Every platform needs the same three things: endpoint, auth header, modification
keys. Get the exact keys first, never guess them:

```
orshot_get_studio_template_modifications   (or GET /v1/studio/templates/:id/modifications)
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

The response contains the rendered URL, map it to whatever the next step needs.

- **n8n**: HTTP Request node, POST, header auth, body as above. A dedicated
  Orshot node also exists in the n8n library.
- **Make**: HTTP "Make a request" module, or the Orshot app modules.
- **Zapier**: Webhooks by Zapier → POST, or the Orshot Zapier app.
- **Pipedream**: HTTP step; Orshot components are published.
- **Own code / cron**: any HTTP client. Use `response.type: "url"` in production
  so you are not moving base64 around, and keep the API key in an environment
  variable, never inline.

Recurring triggers that work well: a new spreadsheet/Airtable/Notion row, a
schedule, an inbound webhook, or a CMS publish event.

### Verify before you call it done

1. Trigger one real run
2. `orshot_list_workspace_logs` (or `GET /v1/workspace/logs`): the new render
   appears with the `source` of whatever fired it, proving which system made it
3. Show the user the image URL from that run

If the render 403s, read the body: an expired key, an inactive subscription, and
a plan limit all return 403 with different messages. A plan block is not an auth
problem, do not retry it as one.

