## Description:

Builds an OpenClaw multi-agent HQ system with a mother-bot and sub-bots, including organization design, role files, dispatcher guidance, task state machine, blackboard protocol, and onboarding docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyandlg123321-maker](https://clawhub.ai/user/happyandlg123321-maker)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to turn a multi-agent OpenClaw concept into a structured, installable, teachable HQ skeleton. It is especially suited for creating 001-05 bot organization docs, dispatcher/runbook files, task cards, blackboard protocol, review mechanisms, and newcomer acceptance checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to propose or write many workspace files for an OpenClaw HQ skeleton.

Mitigation: Review the generated file list and acceptance checklist before allowing workspace writes.

Risk: The bundled onboarding material is primarily Chinese-language and may not fit users who expect English-only output.

Mitigation: Ask the agent for English output or narrower trigger conditions when Chinese-only onboarding material is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/happyandlg123321-maker/skills/openclaw-multi-agent-hq-builder)
- [Install Guide](references/install-guide.md)
- [Acceptance Checklist](references/acceptance-checklist.md)
- [Minimal Examples](references/minimal-examples.md)
- [Test Prompts](references/test-prompts.md)
- [Publish Checklist](references/publish-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with file lists, checklists, templates, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose multiple workspace files for an OpenClaw HQ skeleton; review generated file lists before writing.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact RELEASE.md lists v1.0 released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
