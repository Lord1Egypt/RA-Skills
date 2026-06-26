# Useless Facts

Did you know that honey never spoils? Or that a group of flamingos is called a "flamboyance"?

Get random bits of trivia that are completely useless but weirdly fascinating.

## Just two tools

- `random_fact` -- A random useless fact, different every time
- `today_fact` -- The useless fact of the day (same for everyone, changes daily)

Both return the fact text, source, source URL, and a permalink.

## Give it a spin

```bash
curl -X POST https://gateway.pipeworx.io/uselessfacts/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"random_fact","arguments":{}}}'
```

```json
{
  "mcpServers": {
    "uselessfacts": {
      "url": "https://gateway.pipeworx.io/uselessfacts/mcp"
    }
  }
}
```
