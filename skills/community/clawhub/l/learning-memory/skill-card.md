## Description: <br>
Enables OpenClaw agents to update long-term MEMORY.md notes and package reusable workflow scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanminhhole](https://clawhub.ai/user/tuanminhhole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add durable memory and reusable helper-script creation behavior to agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can persistently modify AGENTS.md across configured OpenClaw workspaces. <br>
Mitigation: Review install.js before use, run it only when workspace-wide instruction changes are intended, and use node install.js --restore to remove the patch. <br>
Risk: The skill encourages agents to save long-term memory and create reusable scripts automatically. <br>
Mitigation: Keep secrets and sensitive infrastructure details out of MEMORY.md, and inspect generated scripts before running them. <br>
Risk: The package declares a postinstall script that runs install.js. <br>
Mitigation: Avoid npm-style installation flows that trigger postinstall unless automatic workspace patching is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanminhhole/skills/learning-memory) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead agents to update MEMORY.md and TOOLS.md, create reusable scripts, and patch AGENTS.md during installation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
