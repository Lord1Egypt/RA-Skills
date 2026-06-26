# Exa Search API Reference

Exa's `/search` endpoint finds semantically relevant web pages.

## Endpoint

```
POST https://api.exa.ai/search
Header: x-api-key: <EXA_API_KEY>
```

## Minimal Payload

```json
{
  "query": "AI legal contract tools for small businesses",
  "numResults": 5,
  "type": "neural",
  "useAutoprompt": true,
  "contents": { "text": { "maxCharacters": 200 } }
}
```

## Response Shape

```json
{
  "results": [
    {
      "title": "ContractPodAi",
      "url": "https://contractpod.ai",
      "text": "AI-powered contract lifecycle management..."
    }
  ]
}
```

## Tips for Competitor Queries

- Frame queries as "tools for X" or "startups solving Y" rather than brand names
- Use 3 varied angles: direct (same solution), adjacent (same problem), incumbent (old way)
- Example set for "AI legal contracts for SMEs":
  1. "AI contract automation software for small businesses"
  2. "legal document automation startups 2024"
  3. "contract lifecycle management tools SME"
