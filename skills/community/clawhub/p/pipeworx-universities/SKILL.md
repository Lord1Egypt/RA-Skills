# Universities

Search universities worldwide by name or country. Returns institution names, countries, domains, and web pages.

This pack has a single tool: **search_universities**. Provide a name, a country, or both to filter results.

## Examples

Find universities named "Stanford":

```bash
curl -X POST https://gateway.pipeworx.io/universities/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_universities","arguments":{"name":"Stanford"}}}'
```

List universities in Japan:

```bash
curl -X POST https://gateway.pipeworx.io/universities/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_universities","arguments":{"country":"Japan"}}}'
```

Each result includes the university name, country, ISO country code, state/province (where available), domain names, and web page URLs.

```json
{
  "mcpServers": {
    "universities": {
      "url": "https://gateway.pipeworx.io/universities/mcp"
    }
  }
}
```
