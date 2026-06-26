# Provider Probe Checklist

## Goal
Determine whether a claimed OpenAI-compatible model endpoint is:
1. likely a real/genuine upstream model route,
2. likely a wrapped or aliased route behind an aggregation pool,
3. or currently unusable.

## Step-by-step checklist

### 1. Establish declared facts
Collect:
- provider name
- baseURL
- claimed model id
- declared API type (`openai-completions`, `openai-responses`, etc.)
- where the config came from

### 2. Probe `/models`
Check:
- how many models are returned
- whether names span unrelated model families (GPT / Claude / Kimi / DeepSeek / Gemini / etc.)
- whether `owned_by` values are mixed
- whether the claimed model id appears exactly, as an alias, or not at all

Interpretation:
- a mixed catalog strongly suggests an aggregation pool
- a narrow catalog suggests a more focused upstream or curated proxy

### 3. Probe endpoint compatibility
Try both:
- `/responses`
- `/chat/completions`

Record:
- HTTP status
- latency
- whether the returned object shape is coherent
- whether the endpoint behavior matches the declared API type

### 4. Minimal capability tests
Use short prompts that reveal formatting reliability rather than raw intelligence:
- exact literal reply (`OK`)
- digits-only arithmetic
- exact JSON-only output
- exact multiline format output

### 5. Stability tests
Repeat the same small request 3–5 times.
Measure:
- success rate
- latency range
- output consistency
- parse consistency

### 6. Reasoning / structure hints
Look for:
- `reasoning_tokens`
- response object shape
- token accounting style
- fields that suggest a modern GPT-style endpoint or a thin compatibility wrapper

Do not overclaim. These are hints, not proof of official provenance.

### 7. Final judgment template
For each provider, assign:
- **High confidence**
- **Medium confidence**
- **Low confidence**

And explain in one paragraph:
- why it passed or failed
- whether it is suitable as primary, fallback, or avoid

## Important caveat
You usually cannot prove from public API behavior alone that a model is officially sourced from a specific upstream vendor. The right output is a confidence-based operational judgment, not a claim of certainty.
