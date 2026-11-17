## Description:

Captures learnings, errors, and corrections to enable continuous improvement for AI coding-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyjin](https://clawhub.ai/user/luckyjin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding-agent users use this skill to capture corrections, command failures, knowledge gaps, and reusable lessons in learning logs. Teams can review those logs and promote stable, non-sensitive guidance into project or agent context after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted guidance can influence future agent behavior across sessions.

Mitigation: Review entries before promotion and do not allow automatic promotion into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Learning logs can accidentally capture secrets, personal data, proprietary context, or transcripts.

Mitigation: Redact sensitive information before writing any learning and keep logs project-local.

Risk: Broad or global hook configuration can increase unintended prompt injection or reminder scope.

Mitigation: Use project-local hook configuration, keep hook matchers narrow, and prefer an audited pinned release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luckyjin/skills/my-test)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Self-Improvement Hook](hooks/openclaw/HOOK.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and learning-log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning-log entries and optional skill scaffold content for agent workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
