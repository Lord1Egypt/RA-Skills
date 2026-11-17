# Model compatibility assessment

## Contents

1. Evidence policy
2. Capability profile
3. Assessment procedure
4. Cross-model matrix
5. Prohibited claims

## 1. Evidence policy

Model capabilities, limits, and APIs change. Prefer, in order:

1. exact model/version and documentation supplied by the user;
2. current official vendor documentation available through approved sources;
3. an explicitly dated local model profile;
4. capability requirements marked `Unknown`.

Do not rely on remembered context limits, prices, feature names, or vendor-specific prompting folklore when the claim affects the score.

## 2. Capability profile

Capture only relevant fields:

```yaml
vendor: unknown
model_id: unknown
profile_checked_at: unknown
evidence_source: unknown
message_roles:
  system: unknown
  developer: unknown
structured_output:
  json_mode: unknown
  json_schema: unknown
tools:
  native_tool_use: unknown
modalities:
  input: [text]
  output: [text]
limits:
  context_tokens: unknown
  max_output_tokens: unknown
environment:
  web: unknown
  code_execution: unknown
  file_access: unknown
```

Unknown fields are not failures. They reduce claim scope and confidence.

## 3. Assessment procedure

1. Extract the prompt's capability requirements.
2. Separate platform features from model features. Web access, file access, memory, and code execution often belong to the host environment.
3. Map each requirement to verified, unsupported, or unknown.
4. Identify vendor-specific syntax, message roles, schema formats, and tool protocols.
5. Recommend a portable core prompt and thin model-specific adapters where appropriate.
6. Label the result `Static compatibility prediction — not runtime tested`.

Avoid general claims such as “Model X prefers XML.” Instead state the observable dependency: “The prompt requires correctly nested XML delimiters; malformed tags create ambiguity on any model.”

## 4. Cross-model matrix

Use this shape:

| Requirement | Model A | Model B | Model C | Prompt implication |
|---|---|---|---|---|
| Exact model/version known | Yes/No | Yes/No | Yes/No | Confidence impact |
| Required message roles | Supported/Unsupported/Unknown | ... | ... | Migration needed |
| Strict schema output | Supported/Unsupported/Unknown | ... | ... | Adapter or validator |
| Native tools | Supported/Unsupported/Unknown | ... | ... | Protocol rewrite |
| Required modality | Supported/Unsupported/Unknown | ... | ... | Feasibility |
| Context/output fit | Fits/Does not fit/Unknown | ... | ... | Compression needed |
| Portability risk | Low/Medium/High/Unknown | ... | ... | Key reason |

If no verified capability data is available, still compare prompt dependencies and list what must be verified. Do not invent per-model numeric scores merely to fill the table.

## 5. Prohibited claims

Without runtime evidence, do not report:

- actual answer quality;
- actual instruction-following rate;
- actual hallucination rate;
- actual format compliance rate;
- latency, token usage, or cost;
- statistical superiority of one model;
- a model-specific score based only on reputation.

Static scores may describe compatibility with verified interface requirements, not observed response performance.
