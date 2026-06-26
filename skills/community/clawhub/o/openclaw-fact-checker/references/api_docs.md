# External API Reference

## Google Fact Check Tools API (Optional)

Free API that searches 100+ global fact-checking organizations (Snopes, PolitiFact, AFP, etc.).

**Endpoint:** `https://factchecktools.googleapis.com/v1alpha1/claims:search`

**Parameters:**
| Param | Description |
|-------|-------------|
| `query` | Search text (use first 200 chars of input) |
| `languageCode` | ISO 639-1 code (e.g., `en`, `zh`, `es`, `fr`, `ar`) |
| `pageSize` | Max results (default: 10) |
| `key` | API key |

**Example curl:**
```bash
curl -s "https://factchecktools.googleapis.com/v1alpha1/claims:search?query=COVID+vaccines+contain+microchips&languageCode=en&pageSize=10&key=$GOOGLE_FACTCHECK_API_KEY"
```

**Response structure:**
```json
{
  "claims": [
    {
      "text": "The claim text",
      "claimReview": [
        {
          "textualRating": "False",
          "publisher": { "name": "Snopes" },
          "url": "https://snopes.com/...",
          "reviewDate": "2024-01-15"
        }
      ]
    }
  ]
}
```

**Get API key:** https://developers.google.com/fact-check/tools/api/reference/rest (free, requires Google Cloud project)

