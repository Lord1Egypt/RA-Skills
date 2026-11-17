## Description:

Coordinates multi-agent project work by routing early discussions, creating Discord project threads, assigning initial agent tasks, and reporting project status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project leads use this skill to coordinate multi-agent work in Discord, from brainstorming and project initiation through thread-based task assignment and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord bot credentials may be exposed by helper commands or logs.

Mitigation: Avoid running the config output command unless token fields are redacted, keep bot tokens out of transcripts, and rotate any token that may have been printed.

Risk: Project ideas, assignments, and status queries can be sent to the configured Discord workspace.

Mitigation: Use the skill only with approved Discord workspaces and avoid submitting confidential project details unless that workspace is authorized for them.

Risk: Broad natural-language triggers can send messages, create threads, or update project records unexpectedly.

Mitigation: Prefer explicit /project:init, /project:discuss, and /project:status invocations, confirm agent selections before thread creation, and review archive actions before updating records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexxxiong/skills/inspirai-project)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Discord API calls, project summaries, local project-record updates, and status tables.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
