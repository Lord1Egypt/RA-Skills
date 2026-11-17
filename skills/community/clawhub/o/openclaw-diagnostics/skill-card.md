## Description:

Diagnoses and troubleshoots OpenClaw configuration, channel, group message, cron job, and authentication issues using logs and a built-in knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperun](https://clawhub.ai/user/cooperun)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to gather OpenClaw configuration, status, and log details, check common setup problems, and produce troubleshooting guidance for messaging, automation, and authentication failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output can expose raw OpenClaw configuration and recent logs, including secrets or private message data.

Mitigation: Review and redact diagnostic output before sharing it, especially tokens, API keys, webhook URLs, phone numbers, user IDs, and message content.

Risk: The knowledge-base update workflow uses network access and an unpinned tsx execution path.

Mitigation: Avoid update commands unless tsx is pinned or installed from a trusted lockfile, and treat any updated documentation snapshot as untrusted reference text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cooperun/skills/openclaw-diagnostics)
- [OpenClaw Common Issues Diagnostic Rules](references/common-issues.md)
- [OpenClaw Knowledge Base Index](references/knowledge-base-index.md)
- [Built-in OpenClaw Documentation Snapshot](assets/default-snapshot.json)
- [OpenClaw Documentation Sitemap](https://docs.openclaw.ai/sitemap.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include excerpts from local OpenClaw configuration, status, and recent logs when the diagnostic scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
