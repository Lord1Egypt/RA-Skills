# Translate

Machine translation between dozens of languages, plus language detection.

## Three tools

`translate` -- Translate text from one language to another. Requires source and target language codes.

`detect_language` -- Identify the language of any text. Returns detected languages ranked by confidence.

`list_languages` -- Get all supported language codes and names.

## Example: English to Spanish

```bash
curl -X POST https://gateway.pipeworx.io/translate/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"translate","arguments":{"text":"The weather is beautiful today","source":"en","target":"es"}}}'
```

## Common language codes

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| pt | Portuguese |
| zh | Chinese |
| ja | Japanese |
| ar | Arabic |
| ru | Russian |
| ko | Korean |

Use `list_languages` for the full set.

## Add to your client

```json
{
  "mcpServers": {
    "translate": {
      "url": "https://gateway.pipeworx.io/translate/mcp"
    }
  }
}
```

Powered by LibreTranslate.
