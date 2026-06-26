---
name: pipeworx-dictionary
description: Word definitions, phonetics, usage examples, synonyms, and antonyms from the Free Dictionary API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📝"
    homepage: https://pipeworx.io/packs/dictionary
---

# Dictionary

Look up any English word and get definitions organized by part of speech, phonetic transcription, audio pronunciation URLs, usage examples, synonyms, and antonyms. Powered by the Free Dictionary API.

## Tools

- **`define_word`** — Full definitions with phonetics, parts of speech, and example sentences
- **`get_synonyms`** — Synonyms and antonyms extracted from dictionary entries

## Reach for this when

- A user asks "what does 'ephemeral' mean?"
- Building a vocabulary quiz or flashcard application
- Need synonyms for writing assistance or paraphrasing
- Want phonetic pronunciation data for a language learning tool

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/dictionary/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"define_word","arguments":{"word":"serendipity"}}}'
```

Returns definitions grouped by part of speech, with example usage and audio URLs.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-dictionary": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dictionary/mcp"]
    }
  }
}
```
