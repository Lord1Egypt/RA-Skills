## Description:

Detects and redacts personally identifiable information and secret-like values in application logs, then helps select masking, tokenization, hashing, dropping, scanner, pipeline, and compliance-mapping outputs for common observability stacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, privacy engineers, and platform teams use this skill to audit log streams for PII, design redaction strategy, generate pipeline configuration, add pre-production scanning, and map controls to privacy and compliance requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner and pipeline examples may miss important secrets or nested PII in real logs.

Mitigation: Require recursive structured-log traversal, multiline secret detection, and representative tests against the target log schema before production use.

Risk: Incomplete redaction can create false confidence before logs are retained in observability or storage sinks.

Mitigation: Use field allowlists, fail-closed handling, and review gates before sending logs to retained systems such as Datadog, Splunk, ELK, Loki, or S3.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/charlie-morrison/skills/log-pii-redactor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include regex packs, scanner scripts, per-field strategy tables, pipeline recipes, compliance mappings, placement guidance, and rollout plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
