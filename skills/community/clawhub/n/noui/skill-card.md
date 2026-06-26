## Description: <br>
Use this skill when the user wants to install NoUI skills, get started with NoUI, see which NoUI skills are available, or add NoUI to their agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabriel-adopt](https://clawhub.ai/user/gabriel-adopt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use NoUI to discover, install, and set up browser automation skills that record workflows and export them as FastMCP servers or Claude Code Skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downstream NoUI components may operate with live browser cookies and session context. <br>
Mitigation: Use a disposable browser profile or sandbox for authenticated workflows. <br>
Risk: Installing all referenced NoUI sub-skills may add more browser automation capability than a user needs. <br>
Mitigation: Install only the NoUI sub-skills intended for the workflow and review the referenced GitHub repository before running npx commands. <br>


## Reference(s): <br>
- [NoUI ClawHub Release](https://clawhub.ai/gabriel-adopt/noui) <br>
- [NoUI GitHub Repository](https://github.com/adoptai/noui) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides installation commands and setup guidance; it does not install components on its own.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
