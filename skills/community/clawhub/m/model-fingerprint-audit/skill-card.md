## Description:

Audit OpenAI-compatible or Anthropic-compatible model endpoints using repeated behavioral probes, stability metrics, and trusted reference fingerprints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess the stability of authorized model endpoints and compare proxy behavior against a trusted fingerprint of a claimed model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials or private content could be exposed in reports or saved fingerprints.

Mitigation: Use authorized local key sources and synthetic prompts; exclude keys and raw private responses from reports and cached artifacts.

Risk: Repeated probes can consume endpoint quota and incur costs.

Mitigation: Confirm authorization and quota impact, run a low-cost pilot first, and bound concurrency during full audits.

Risk: Missing or stale reference fingerprints can lead to misleading identity claims.

Mitigation: Record baseline provider, model version, collection date, and probe set; report an inconclusive result if the reference is missing or stale.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jes614753-sketch/skills/model-fingerprint-audit)
- [Trusted reference sources](references/baseline-sources.md)
- [llm-fingerprint probe engine](https://github.com/dreamor/llm-fingerprint)
- [CompatBench compatibility checks](https://github.com/RuizhangZhou/CompatBench)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown audit report and sanitized local fingerprint artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports request success, stability, comparison limits, and baseline provenance; supports cached reference fingerprints.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
