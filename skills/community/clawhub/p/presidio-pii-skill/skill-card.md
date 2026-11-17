## Description:

Provides local PII protection for OpenClaw agents by using Microsoft Presidio containers to scrub customer data before it reaches an AI model, with reversible pseudonymization and fail-closed behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to protect customer data from CRM, cloud storage, project management, and similar sources before an agent sends content to an AI model. It helps agents check local Presidio availability, scrub PII into tokens, reason over anonymized text, and restore user-facing responses locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw customer data can be sent to Presidio endpoints controlled through environment variables.

Mitigation: Use only trusted local Presidio analyzer and anonymizer endpoints, review endpoint environment variables before execution, and avoid forwarding sensitive input if the health check fails.

Risk: Reversible PII mapping files contain sensitive token-to-original-value associations.

Mitigation: Run the skill as an unprivileged user, store mappings in a restricted local directory, use trusted session identifiers, and restore/delete mappings promptly.

Risk: PII detection may miss unsupported formats or domain-specific identifiers.

Mitigation: Review anonymized output before sending it to a model and maintain custom recognizers for local data patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sebclawops/skills/presidio-pii-skill)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local reversible mapping files during scrub/restore workflows; restore deletes mappings unless explicitly kept.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact declares 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
