## Description: <br>
Automates weekly memory compression per agent in OpenClaw, consolidating daily notes into domain-specific long-term files without manual setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensk2001](https://clawhub.ai/user/bensk2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install recurring per-agent memory consolidation tasks that read older daily notes, extract durable facts, and append them to long-term memory files. It is intended for multi-agent OpenClaw deployments that need automated state tracking, deduplication, and domain-aware extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring jobs automatically read older daily notes and persist extracted personal profile information into long-term memory files. <br>
Mitigation: Back up agent workspaces before installing, review generated USER.md, IDENTITY.md, SOUL.md, and MEMORY.md entries, and remove or correct sensitive or inaccurate extracted content. <br>
Risk: The installer discovers all OpenClaw agents with workspaces and creates scheduled tasks for each one. <br>
Mitigation: Edit the installer or delete unwanted cron tasks after installation so only intended agents run memory compression. <br>
Risk: Delivery summaries can be sent to the wrong external recipient if channel or recipient settings are incorrect. <br>
Mitigation: Verify the delivery channel, recipient, and account values before installation and confirm notification behavior after the first run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bensk2001/per-agent-compression-universal) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [Installer-driven cron configuration with Markdown and text updates to agent memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates OpenClaw cron tasks, state files, processed-note folders, and delivery summaries.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
