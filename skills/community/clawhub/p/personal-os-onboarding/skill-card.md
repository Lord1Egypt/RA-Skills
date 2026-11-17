## Description:

Set up a Personal OS through a conversational onboarding flow that creates SOUL.md, USER.md, IDENTITY.md, AGENTS.md, and MEMORY.md as foundation files for future agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borodich](https://clawhub.ai/user/borodich)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when setting up a new agent workspace for the first time. The skill interviews the user about identity, tools, communication preferences, and goals, then creates persistent Markdown files that future sessions can read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal details, workspace preferences, goals, and agent operating rules in persistent files that future sessions may read.

Mitigation: Use the skill only when persistent onboarding is intended, and review SOUL.md, USER.md, IDENTITY.md, AGENTS.md, and MEMORY.md before relying on them in later sessions.

Risk: Generated AGENTS.md rules may change future agent behavior in the workspace.

Mitigation: Inspect and edit or delete generated AGENTS.md rules that do not match the user's desired operating boundaries.

Risk: The security evidence flags broad activation and limited upfront consent around persistent memory creation.

Mitigation: Confirm consent before collecting sensitive personal information and avoid recording details the user does not want reused.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/borodich/skills/personal-os-onboarding)
- [Publisher profile](https://clawhub.ai/user/borodich)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown plus generated Markdown workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates SOUL.md, USER.md, IDENTITY.md, AGENTS.md, and MEMORY.md after collecting onboarding details.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
