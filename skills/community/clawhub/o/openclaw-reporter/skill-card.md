## Description:

OpenClaw Reporter helps agents opt in to the OpenClaw activity heatmap by registering a user-chosen claw name and sending consent-gated heartbeat, task, and optional token usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardwei195](https://clawhub.ai/user/richardwei195)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to participate in the OpenClaw global activity heatmap while keeping reporting opt-in and limited to non-code activity signals. It is intended for agents that can ask for consent, run the claw-market CLI, and manage the local OpenClaw configuration file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned global third-party CLI that was not included in the artifact for review.

Mitigation: Review or pin the @ricardweii/claw-market package before installation, and install it only from a trusted source.

Risk: Participation sends platform, model, task-completion signals, optional token counts, and the user's IP address to https://kymr.top/.

Mitigation: Use the skill only after explicit consent, avoid identifying task summaries, and clear ~/.openclaw/config.json to opt out.

Risk: Registration stores an API key locally in ~/.openclaw/config.json.

Mitigation: Keep the file permission restricted to the user and avoid sharing the local OpenClaw configuration file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardwei195/skills/openclaw-reporter)
- [OpenClaw service endpoint](https://kymr.top/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and consent prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or clear ~/.openclaw/config.json after user consent and uses the external claw-market CLI for reporting.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
