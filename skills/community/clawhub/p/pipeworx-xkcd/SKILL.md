# xkcd

Fetch xkcd comics programmatically. Because sometimes you need to cite "Standards" (927) in a technical argument, or share "Compiling" (303) while waiting for CI.

Three tools:

- `get_latest` -- Whatever Randall published most recently
- `get_comic` -- A specific comic by number
- `random_comic` -- Surprise me (skips #404, which is intentionally missing -- it's an xkcd joke)

Each comic comes with the title, alt text (the hover text!), image URL, date, transcript, and a permalink.

## Example: fetch the classic "Python" comic (#353)

```bash
curl -X POST https://gateway.pipeworx.io/xkcd/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_comic","arguments":{"number":353}}}'
```

## Greatest hits

| # | Title |
|---|-------|
| 149 | Sandwich |
| 303 | Compiling |
| 327 | Exploits of a Mom (Bobby Tables) |
| 353 | Python |
| 386 | Duty Calls |
| 927 | Standards |
| 1053 | Ten Thousand |
| 2347 | Dependency |

```json
{
  "mcpServers": {
    "xkcd": {
      "url": "https://gateway.pipeworx.io/xkcd/mcp"
    }
  }
}
```
