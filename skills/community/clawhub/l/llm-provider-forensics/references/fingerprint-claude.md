# Claude / Anthropic Family Fingerprint

Stronger Claude-like signals:
- native `POST /v1/messages` works cleanly
- requires `x-api-key` and `anthropic-version`
- response contains `content` blocks with text segments
- shape feels Anthropic-native rather than OpenAI-normalized

Wrapper suspicion:
- endpoint claims Claude but only works through OpenAI-compatible paths
- no native messages path behavior
- catalog mixes many unrelated vendors and only the model id contains `claude`
