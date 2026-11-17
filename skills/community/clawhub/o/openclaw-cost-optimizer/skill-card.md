## Description:

Adds lower-cost OpenRouter model aliases to an OpenClaw setup and advises when to switch models based on task complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw users use this skill to add task-specific model aliases, estimate model costs, and receive guidance on when to switch between cheaper or more capable OpenRouter models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run local OpenClaw commands and can make changes to model aliases.

Mitigation: Review each proposed command before approval and only approve expected OpenClaw model or gateway commands.

Risk: The cost tracker may write task descriptions to ~/.openclaw/cost-tracker.md and could expose sensitive task, customer, or project details.

Mitigation: Avoid using tracker features with sensitive work, or disable/reset the tracker when sensitive context may be recorded.

Risk: The security summary flags tracker append/reset behavior as unsafe because shell interpolation could execute unintended commands from task text.

Mitigation: Treat tracker-writing behavior as high risk until it is changed to write safely without shell interpolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeffjhunter/skills/openclaw-cost-optimizer)
- [Publisher Profile](https://clawhub.ai/user/jeffjhunter)
- [OpenRouter](https://openrouter.ai)
- [Model Reference](artifact/MODEL-REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and chat commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local cost tracker at ~/.openclaw/cost-tracker.md.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
