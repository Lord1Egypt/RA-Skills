# nbnhhsh - Pinyin Initialism Translator

Use this skill when:
- User asks what an abbreviation means (e.g., "what does xswl mean", "what is yyds")
- User provides a pinyin initialism for lookup
- User says something like "don't understand", "what's this"
- User inputs a confusing string of letters that might be a pinyin initialism

## Function
- Translate pinyin initialisms to Chinese (e.g., xswl → 笑死我了)
- Support batch queries, multiple abbreviations separated by commas
- Return multiple possible interpretations

## Usage

Run curl:

```bash
curl -s -X POST "https://lab.magiconch.com/api/nbnhhsh/guess" \
  -H "Content-Type: application/json" \
  -d '{"text":"abbreviation to query"}'
```

## Example

Input: `xswl`
Output: 笑死了, 吓死了, 想死了... (multiple possible results)

## Notes
- API may have rate limits, please do not abuse
- Same abbreviation may have multiple interpretations, returned in trans array
- If trans is null but inputting has values, it means awaiting review