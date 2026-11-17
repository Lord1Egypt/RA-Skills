## Description:

Weekly memory governance audit for OpenClaw. Use when user asks to audit/optimize memory quality, reduce token overhead, verify MEMORY/TOOLS/AGENTS role boundaries, validate QMD routing quality, or run a periodic memory health check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markisadesigner1992-eng](https://clawhub.ai/user/markisadesigner1992-eng)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to audit memory and governance files, identify role-boundary or token-budget issues, and produce a weekly action plan for keeping memory concise and useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may place profile details, durable memories, persona notes, tool rules, or governance policy into the active model context.

Mitigation: Ask for redacted findings or file-size and section checks first when memory or governance files may contain secrets or highly private content.

Risk: Suggested memory edits could remove useful context or shift governance boundaries if applied without review.

Mitigation: Review the report's proposed fixes before changing files, and require explicit approval before overwriting or editing user memory files.

## Reference(s):

- [Memory Audit Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with findings, risk notes, action plan, and report path suggestion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an A/B/C score, concise executive summary, weekly fixes, and add/remove keyword suggestions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
