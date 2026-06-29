# Capability Taxonomy

Use these dimensions to classify model/provider support. Always bind a status to a provider surface, model/version, API version, region when relevant, and citation.

## Status Values

- `supported`: Official docs for the exact provider surface confirm the capability.
- `not_supported`: Official docs for the exact provider surface explicitly deny, omit from an exclusive support matrix, or document an incompatible API shape.
- `partial`: Official docs confirm support with material limits such as selected models, regions, API versions, modalities, quotas, preview status, or missing subfeatures.
- `provider_specific`: The capability exists but semantics, parameters, auth, quotas, model IDs, safety controls, logging, or lifecycle differ from the first-party provider.
- `unknown_needs_live_check`: Current official docs for the exact provider surface were not checked, could not be accessed, conflict, or do not mention the capability clearly.

## Capability Dimensions

- Model availability: model family, exact model ID, version/date suffix, lifecycle stage, deprecation status.
- Region and tenancy: supported regions, data residency, provisioned throughput, private networking, enterprise controls.
- API surface: endpoint family, API version, SDK, streaming behavior, batch/asynchronous support.
- Input modalities: text, image, audio, video, document/PDF, embeddings, files, context caching.
- Output modalities: text, structured JSON, image/audio/video generation, citations, logprobs.
- Tooling: function/tool calling, computer use, code execution, web/search grounding, retrieval, agents/assistants abstractions.
- Reasoning controls: thinking/reasoning modes, budgets, summaries, trace visibility, deterministic controls.
- Context and limits: context window, output tokens, file size, rate limits, quota classes.
- Safety and policy: safety filters, content moderation, configurable guardrails, prompt shielding, data-use policy.
- Operations: authentication, IAM/RBAC, billing unit, monitoring, audit logs, SLA, support channel.
- Compatibility: OpenAI-compatible endpoints, Anthropic-compatible messages, migration gaps, parameter aliases.

## Evidence Requirements

- Prefer hosting-provider docs for hosted support claims.
- Use first-party model docs for first-party API claims or as comparison context only.
- Cite exact official URL and mention if docs require live verification.
- If support depends on model version, API version, or region, include that condition in the status.
