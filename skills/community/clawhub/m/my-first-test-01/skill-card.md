## Description:

Captures learnings, errors, and corrections so agents can record failures, user corrections, missing capabilities, outdated knowledge, and recurring better practices for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muyangsx](https://clawhub.ai/user/muyangsx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture concise learning, error, and feature-request records during coding sessions, then promote durable patterns into project or agent memory after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent self-improvement logs and promoted memory files can preserve incorrect guidance or sensitive context across sessions.

Mitigation: Review entries before promotion, keep records concise, and redact secrets, tokens, environment variables, full command outputs, and raw transcripts.

Risk: Broad or global hook configuration can inject reminders in more sessions than intended and may inspect command output for error patterns.

Mitigation: Prefer project-local hooks, use the minimal activator-only setup by default, and enable command-output inspection only in trusted workspaces.

Risk: Cross-session sharing can expose transcripts or private working context if used casually.

Mitigation: Use cross-session tools only in trusted environments and share sanitized summaries plus relevant file paths instead of raw transcripts.

Risk: The skill extraction helper creates files from local inputs and should not be treated as an unattended automation path.

Mitigation: Run extraction manually, review generated skill content before use, and avoid running the helper in workspaces with untrusted symlinks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muyangsx/skills/my-first-test-01)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local .learnings files, configure opt-in hooks, or scaffold reusable skill files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
