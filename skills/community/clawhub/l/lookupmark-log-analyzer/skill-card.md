## Description:

Securely analyzes whitelisted local OpenClaw and RAG logs, redacts common sensitive values, and reports errors, summaries, or search matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect recent local service logs for OpenClaw gateway and local RAG workflows, summarize likely failures, and search known log sources without granting arbitrary file access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sanitized log excerpts may still reveal operational details or residual sensitive content.

Mitigation: Use the skill only on intended local OpenClaw and RAG logs, avoid shared contexts with sensitive logs, and review output before sharing.

Risk: Broad requests such as "any errors" can cause wider log inspection across allowed sources than the user intended.

Mitigation: Prefer source-specific requests or confirm scope before asking for broad log analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lookupmark/skills/lookupmark-log-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON log summaries with redacted log excerpts and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads only configured local log sources and may include sanitized operational log snippets.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
