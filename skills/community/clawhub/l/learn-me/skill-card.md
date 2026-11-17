## Description:

Learn me: Lets OpenClaw proactively learn more about you through natural conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yevhendiachenko0](https://clawhub.ai/user/yevhendiachenko0)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to let the agent ask occasional personal follow-up questions and maintain non-secret question directions with the user's permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled prompts may continue influencing the main OpenClaw session after installation.

Mitigation: Enable schedules only after user confirmation, confirm the exact cron entries created, and document how to list or delete all learn-me-* crons.

Risk: The memory/next-questions.md file can contain personal follow-up notes.

Mitigation: Avoid storing secrets, health details, precise location, credentials, or other highly sensitive personal information, and keep the file inspectable and deletable by the user.

Risk: Personal questions can be intrusive when the user is focused, stressed, or reluctant.

Mitigation: Ask at most one natural follow-up, skip during focused or difficult moments, and respect deflection cooldowns or permanent opt-outs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yevhendiachenko0/skills/learn-me)
- [Project homepage](https://github.com/YevhenDiachenko0/openclaw-learn-me-skill)
- [Example questions](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language guidance with Markdown notes and OpenClaw cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create OpenClaw cron entries and memory/next-questions.md after user confirmation.]

## Skill Version(s):

0.5.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
