# Gemini / Google Family Fingerprint

Stronger Gemini-like signals:
- model listing via `/v1beta/models` or `/v1/models`
- inference via `models/{model}:generateContent`
- response contains `candidates`, `content`, `parts`
- usage fields look like Gemini usage metadata
- API key query parameter style works as expected

Wrapper suspicion:
- claimed Gemini model only works via OpenAI-compatible endpoints
- no Gemini-native route behavior despite Gemini naming
