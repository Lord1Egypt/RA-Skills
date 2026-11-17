## Description:

Scan AI prompts for injection, jailbreak, and sensitive data leak risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to check prompts before sending them to an LLM, with findings for sensitive data leaks, injection attempts, and jailbreak patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can print the sensitive data it is intended to detect when raw-match output is included in reports.

Mitigation: Avoid running it on real secrets in terminals, CI logs, shared report files, or monitoring pipelines unless raw matches are removed or masked by default.

Risk: The release security verdict is suspicious because the skill is local and purpose-aligned but can expose matched secrets in output.

Mitigation: Review the skill before installation and prefer redacted output for prompts that may contain credentials or personal data.

## Reference(s):

- [Prompt Guard Detection Patterns Reference](references/patterns.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Plain-text security report or JSON findings, with optional redacted prompt output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include risk score, classification, matched findings, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
