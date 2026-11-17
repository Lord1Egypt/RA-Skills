## Description:

Jiajiaoy Morning builds scheduled Chinese morning briefings and evening fortune prompts by orchestrating news, finance, weather, wellness, language, and fortune modules for a configured user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to configure daily Chinese morning briefings and optional evening fortune pushes delivered through scheduled OpenClaw tasks. It is intended for recurring personal briefing workflows that combine multiple installed ClawHub skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a concrete subscriber configuration with personal identifiers.

Mitigation: Remove the bundled subscriber file and keep only the blank template before installing or redistributing the skill.

Risk: The setup flow can generate scheduled-task commands from user-supplied channel and recipient fields.

Mitigation: Require explicit user confirmation and validate channel and recipient values before registering cron jobs.

Risk: The skill depends on multiple sibling skills, including a fortune module that may read bazi profile data.

Mitigation: Install only reviewed or pinned dependency skills and make users aware that evening fortune generation may use data from the yunshi skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/jiajiaoy-morning)
- [ClawHub publisher profile](https://clawhub.ai/user/cosmofang)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown prompts, JSON module lists, and shell commands for scheduled task setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer and 11 dependent ClawHub skills; several briefing modules may require web search or external skill execution.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
