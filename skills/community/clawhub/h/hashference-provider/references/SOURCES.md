# Sources and freshness

Retrieved 2026-11-17 UTC:

- https://hashference.com/skill.md — existing general-purpose skill, MIT/MIT-0.
- https://hashference.com/.well-known/skills/hashference/LICENSE — upstream license.
- https://hashference.com/llms.txt — current API, privacy, credits and routes.
- https://hashference.com/docs/connect.md — client settings; its example local ID quai is arbitrary. Literal key examples are replaced here with SecretRefs.
- https://hashference.com/docs/models.md — catalog fields/limits.
- https://hashference.com/v1/catalog — bundled public snapshot.
- https://hashference.com/v1/capabilities — live feature discovery.
- https://docs.openclaw.ai/concepts/model-providers/custom-providers — runtime registrations, aliases and route metadata; also checked in installed docs.
- https://docs.openclaw.ai/gateway/configuration — validation/merge; check installed version schema.

Reconciled differences: do not repeat upstream blanket Claude zero-retention wording; live direct Anthropic records say provider-policy. Historical configuration had 61 canonical models; this retrieval has 62. Neither previous assistant claims nor public metadata constitute current paid inference/tool-loop proof.

Package excludes private account data, keys, transcripts, personal configuration and host paths. No authenticated inference was performed for skill authoring.
