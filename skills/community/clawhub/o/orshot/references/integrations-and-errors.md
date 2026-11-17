## Integrations & Helps

### Integrations Service Support
Orshot connects with:
- **No-code:** Zapier, Make (Integromat), n8n, Pipedream, Airtable
- **Storage:** Amazon S3, Cloudflare R2, Google Drive, Dropbox
- **Notifications:** Slack, Webhooks
- **Design:** Figma Plugin, Canva Import, Polotno Import
- **CLI:** `npx orshot-cli` for terminal-based generation
- **MCP Server:** Use with Claude, Cursor, Windsurf via MCP protocol
- **Embed:** White-label design editor for your app (React SDK, Vue SDK, iframe)

### Common Error Codes

| Code | Error                          | Fix                                          |
| ---- | ------------------------------ | -------------------------------------------- |
| 400  | `templateId missing`           | Add `templateId` to request body             |
| 400  | `Invalid API Key`              | Generate new key from dashboard              |
| 403  | `Authorization header missing` | Add `Authorization: Bearer $ORSHOT_API_KEY` header     |
| 403  | `Subscription inactive`        | The workspace subscription is not active; check it in the dashboard |
| 403  | `Template not found`           | Verify template ID belongs to your workspace |
| 403  | `ai-video-not-on-plan`         | AI video is not included in the workspace's current plan; use stock footage or a Brand Library video instead |

### General Best Practices

1. **Use `url` response type** for production – avoids large base64 payloads
2. **Use `webp` format** for smaller file sizes with good quality
3. **Test in Playground** before coding – each template has an interactive playground
4. **Use style parameters** instead of creating multiple template variants
5. **Use consistent units** – stick to `px` for sizes
6. **Multi-page prefix** – always use `page1@paramId` format for carousel templates
7. **Cache renders** – use `?cache=false` query param to bypass cache when needed
8. **Handle errors** – check for 403/400 status codes and parse error messages

