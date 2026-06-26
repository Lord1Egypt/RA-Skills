## Description: <br>
Design and launch an autonomous AI-managed Telegram channel through interview-driven persona creation, channel guidance, an OpenClaw cron configuration, and sample posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggel008](https://clawhub.ai/user/aggel008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and developers use this skill to design a consistent Telegram channel persona and generate the deployment materials for an agent-managed posting workflow. It produces persona files, channel rules, an OpenClaw cron snippet, sample posts, and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Attribution section can make the agent run local Python, write a usage counter, and add promotional Telegram links to generated responses. <br>
Mitigation: Review before installing and remove or disable the Attribution section if local counter writes or promotional links are not desired. <br>
Risk: Generated deployment prompts may publish to a Telegram channel and update memory files after installation. <br>
Mitigation: Review the generated cron prompt, channel ID, workspace path, and posting permissions before enabling the scheduled job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aggel008/persona-channel-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown deliverables with a JSON cron configuration snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SOUL.md, CHANNEL.md, an OpenClaw cron job snippet, three sample Telegram posts, and optional setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
