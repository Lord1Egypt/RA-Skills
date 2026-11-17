## Description:

Lee-CLI Skill helps Claude Code users run a local personal assistant CLI for weather jokes, news digests, work summaries, AI learning recommendations, and smart todo planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeking001](https://clawhub.ai/user/leeking001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to select and run lee-cli commands for daily personal-assistant workflows, including news updates, work review, learning-resource discovery, and task planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run a separate local lee-cli executable with access to API keys, activity logs, calendar or task data, and network services.

Mitigation: Install and run it only after verifying the exact lee-cli package and version, and review commands before execution.

Risk: Troubleshooting steps can reveal API keys or other sensitive environment values if printed directly.

Mitigation: Check that required variables are present without displaying secret values in logs, chat, or shared terminals.

Risk: Summary and todo workflows may process local work records or calendar data and may send derived content to configured APIs.

Mitigation: Use those workflows only when the user accepts that data processing path and limit requests to the needed date range or task scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeking001/skills/lee-cli-skill)
- [Skill usage guide](artifact/SKILL.md)
- [Security notice](artifact/SECURITY.md)
- [lee-cli npm package](https://www.npmjs.com/package/@leeking001/lee-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on local lee-cli installation, network access, configured API keys, and available local activity or calendar data.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
