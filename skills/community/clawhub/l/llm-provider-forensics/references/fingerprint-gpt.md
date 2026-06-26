# GPT / OpenAI Family Fingerprint

Stronger GPT-like signals:
- OpenAI-compatible `/responses` and/or `/chat/completions` behave coherently
- response objects look like `response` or `chat.completion`
- token accounting includes `completion_tokens_details` or `output_tokens_details`
- reasoning-related fields may exist
- tool/function schema behavior feels OpenAI-compatible

Weaker evidence:
- a route merely accepts OpenAI-compatible requests
- claimed model id contains `gpt`

Suspicion of wrapper:
- giant mixed model catalog
- zero reasoning signal across all tests despite claimed cutting-edge GPT route
- schema looks normalized and generic across many unrelated claimed models
