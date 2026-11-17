## Description:

Captures learnings, errors, and corrections so coding agents can record failures, user corrections, feature requests, outdated knowledge, and reusable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jageri](https://clawhub.ai/user/jageri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to record command failures, corrections, feature requests, and reusable lessons in learning files, then promote high-value items into agent memory or instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files or promoted memory can preserve incorrect guidance, sensitive context, or outdated assumptions.

Mitigation: Keep learning files project-local, use short redacted summaries, and review every promoted addition before writing to agent instruction files.

Risk: Optional hooks can inject reminders broadly or inspect command output when configured with broad matchers.

Mitigation: Enable hooks only in trusted workspaces, avoid empty matchers where possible, and start with the activator-only setup before enabling command-output error detection.

Risk: Agent memory files such as AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or copilot-instructions.md can affect future agent behavior.

Mitigation: Require human review for proposed memory changes and avoid adding raw transcripts, credentials, environment variables, private data, or full command output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jageri/skills/jageri-self-improvement)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets, hook configuration examples, and file-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local learning files and may provide optional hook reminders when configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
