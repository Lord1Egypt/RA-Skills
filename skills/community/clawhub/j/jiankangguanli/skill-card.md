## Description:

健康管理 collects structured personal health information, sends it to a configured medical model API, and returns the resulting disease-risk assessment and optional report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantian888](https://clawhub.ai/user/lantian888)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to structure personal health details, submit them to a configured health assessment model API, and receive the returned risk assessment text or an optional HTML report. It is positioned as a health management aid and not as a substitute for clinician diagnosis or emergency care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects identifiable medical details and sends full conversation context to an external service.

Mitigation: Require explicit consent and privacy disclosure, minimize or de-identify medical data before transmission, and document the external data processor before use.

Risk: Server evidence reports an exposed API key and runtime token retrieval behavior.

Mitigation: Remove exposed credentials, rotate affected keys, and use a managed secret mechanism with scoped access before installation.

Risk: Generated local HTML reports can include unsanitized assessment or user-provided content.

Mitigation: Escape or sanitize all substituted HTML fields and disable script-capable content before saving or opening reports.

Risk: The skill may show health screening promotions and hotline details in generated reports.

Mitigation: Gate promotional screening content behind clear user intent, consent, and relevance checks, especially for cancer-related content.

## Reference(s):

- [API documentation reference](artifact/references/api_docs.md)
- [ClawHub skill page](https://clawhub.ai/lantian888/skills/jiankangguanli)
- [Publisher profile](https://clawhub.ai/user/lantian888)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown responses and optional local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams model responses, preserves returned assessment content, and may save a rendered HTML report on request.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
