# Words

A writer's toolkit: synonyms, rhymes, related words, autocomplete, and advanced word search. Powered by the Datamuse API.

## find_synonyms

Find synonyms ranked by similarity. `find_synonyms("happy")` returns words like joyful, cheerful, content, glad.

## find_rhymes

Perfect rhymes ranked by score. Great for poetry and songwriting.

## find_related

Find words connected by different relationships:
- `syn` -- synonyms
- `ant` -- antonyms
- `rhy` -- rhymes
- `trg` -- associated/trigger words
- `jja` -- adjectives that describe a noun
- `jjb` -- nouns that an adjective describes

## autocomplete

Word completions from a prefix. `"hel"` returns hello, help, helicopter, etc.

## find_words

The power tool. Combine constraints:
- `meaning_like` -- words with similar meaning to a phrase
- `sounds_like` -- approximate pronunciation match
- `spelled_like` -- pattern with wildcards (`b*ttle` finds bottle, battle, brittle)

## Example: find rhymes for "code"

```bash
curl -X POST https://gateway.pipeworx.io/words/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"find_rhymes","arguments":{"word":"code","limit":10}}}'
```

## Example: words meaning "ocean" that start with "s"

```bash
curl -X POST https://gateway.pipeworx.io/words/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"find_words","arguments":{"meaning_like":"ocean","spelled_like":"s*"}}}'
```

```json
{
  "mcpServers": {
    "words": {
      "url": "https://gateway.pipeworx.io/words/mcp"
    }
  }
}
```
