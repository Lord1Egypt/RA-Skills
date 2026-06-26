## Description: <br>
OpenClaw Agency Agents helps an agent list, search, and activate professional AI agent personas from agency-agents-zh across engineering, design, marketing, sales, and product domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roymax](https://clawhub.ai/user/roymax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to browse a catalog of AI agent personas, activate one for the workspace, restore previous configuration, and update the local persona repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently replace core OpenClaw instruction files with content pulled from an unpinned third-party repository. <br>
Mitigation: Install only when the publisher and upstream repository are trusted, review selected agent markdown before activation, keep the generated backups, and review updates before activating changed personas. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roymax/openclaw-agency-agents) <br>
- [agency-agents-zh repository referenced by the skill](https://github.com/jnMetaCode/agency-agents-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated OpenClaw configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Activation may write SOUL.md, IDENTITY.md, and AGENTS.md in the workspace and create backups for restore.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
