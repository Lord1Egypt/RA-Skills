# Translation

Use `POST /translation/` for Chinese, Traditional Mongolian, and Cyrillic Mongolian translation or conversion.

## Request

```json
{"from":"zh","to":"mw","content":"你好朋友"}
```

`from` and `to` accept:

- `zh`: Chinese
- `mw`: Traditional Mongolian
- `mn`: Cyrillic Mongolian

The source and target must differ. Use one request for `mw` ↔ `mn`; the service handles its internal pivot.

For source languages outside this set, first translate the non-Mongolian source to Chinese with an appropriate general translation capability. Then send only the Chinese intermediate through this endpoint for the Mongolian leg. Do not claim that `/translation/` accepts Japanese, English, or automatic arbitrary-language input.

## Direction defaults

- U+1800–U+18AF source → `mw`
- Cyrillic source → `mn`
- otherwise → `zh`
- Chinese source with no explicit target → `mw`
- Mongolian source with no explicit target in a translation request → `zh`

## Length and segmentation

The bundled script accepts at most 4,000 Unicode code points per call. For longer material:

1. obtain cost confirmation;
2. split on paragraphs or sentence boundaries without changing text;
3. call each segment once in order;
4. concatenate results using the original separators;
5. stop on the first failed segment and report which segment failed without automatically replaying successful segments.

Serialize JSON with Python or another real JSON encoder. Never interpolate raw multiline text into a hand-built JSON string.

## Response

Return `data.tgtText`. Do not return `data.srcText`, the intermediate pivot language, or the response envelope.
