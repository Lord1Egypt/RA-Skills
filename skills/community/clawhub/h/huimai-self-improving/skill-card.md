## Description:

Captures learnings, errors, corrections, and feature requests so agents can preserve useful project knowledge and improve recurring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, feature requests, and reusable lessons into structured Markdown records. It can also guide optional hook setup and promotion of reviewed learnings into agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived learnings into future agent instruction files.

Mitigation: Require a human-reviewed diff before writing or promoting content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Broad hook configuration can repeatedly inject reminders or inspect command output.

Mitigation: Keep .learnings project-local, avoid global hooks and empty matchers, and enable error-output hooks only when command output inspection is acceptable.

Risk: Learning logs may accidentally capture sensitive operational context.

Mitigation: Store concise, sanitized summaries and redact secrets, tokens, environment variables, private keys, and full transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-self-improving)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-local learning logs and optional setup guidance; hook output is intended to be lightweight reminders.]

## Skill Version(s):

3.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
