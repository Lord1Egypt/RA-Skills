# StackExchange

Search questions and retrieve answers from StackOverflow, ServerFault, SuperUser, Ask Ubuntu, Math, Physics, and any other StackExchange site.

## search_questions

Search for questions on any StackExchange site. Returns the question title, body (HTML), score, answer count, tags, link, and view count. Default site is `stackoverflow` but you can pass any site slug.

## get_answers

Get all answers for a question by its numeric ID. Returns the answer body, score, whether it's the accepted answer, author name, and author reputation.

```bash
curl -X POST https://gateway.pipeworx.io/stackexchange/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_questions","arguments":{"query":"async await best practices","site":"stackoverflow","limit":3}}}'
```

## Supported sites

Pass any site slug: `stackoverflow`, `serverfault`, `superuser`, `askubuntu`, `math`, `physics`, `gaming`, `dba`, `security`, `unix`, and hundreds more.

```json
{
  "mcpServers": {
    "stackexchange": {
      "url": "https://gateway.pipeworx.io/stackexchange/mcp"
    }
  }
}
```
