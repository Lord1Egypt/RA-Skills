# Auth Playbook - Instacart

## Surface Matrix

| Surface | Primary auth | Base / entrypoint | Use it for |
|--------|--------------|-------------------|------------|
| Developer Platform REST | `Authorization: Bearer $INSTACART_API_KEY` | `https://connect.dev.instacart.tools` or `https://connect.instacart.com` | recipe pages, shopping list pages, nearby retailers |
| Developer Platform MCP | Developer Platform API key through MCP client config | `https://mcp.dev.instacart.tools/mcp` or `https://mcp.instacart.com/mcp` | agent-native recipe and shopping-list creation |
| Catalog / Connect | separate auth model, often OAuth client credentials | product family specific | retailer, catalog, fulfillment, post-checkout |

## Key Rules

- Keep development and production keys separate.
- Confirm the key permission level before assuming write access.
- Treat a newly created production key as unusable until approval completes.
- Do not paste keys into chat, markdown, screenshots, or repo files.

## REST Smoke Test

Use a low-risk nearby-retailers probe before page creation:

```bash
curl -s \
  "https://connect.dev.instacart.tools/idp/v1/retailers?postal_code=94103&country_code=US" \
  -H "Authorization: Bearer $INSTACART_API_KEY" \
  -H "Accept: application/json" | jq
```

## MCP Smoke Test

- Connect MCP Inspector to `https://mcp.dev.instacart.tools/mcp`
- Use Streamable HTTP
- Verify the tool list includes `create-recipe` and `create-shopping-list`

If those tools do not appear, stop and fix auth or environment before continuing.

## Production Readiness

- Development test coverage should be complete first.
- Creating a production key triggers Instacart review.
- Pending approval means the production key does not function yet.
- Approval also gates production launch messaging and partner workflows.
