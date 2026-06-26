## Description: <br>
opclawtm CLI helps users set up an OpenClaw-based AI Agent team collaboration network with team creation, Feishu group integration, task workflow orchestration, and built-in preset resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poderosom1](https://clawhub.ai/user/poderosom1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide users through installing and activating opclawtm, creating OpenClaw agent teams, configuring Feishu bots and groups, creating private skills through the assistant workflow, and troubleshooting common setup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to propose broad local installs, activation commands, or gateway startup steps. <br>
Mitigation: Have the user review and approve npm install, activation, gateway, and TUI commands before execution, and run them only in a trusted local environment. <br>
Risk: The skill guides handling of App Secrets, license keys, and other setup credentials. <br>
Mitigation: Do not paste real App Secrets or license keys into shared chat; enter secrets directly into the intended local tool or Feishu console when possible. <br>
Risk: Troubleshooting can involve inspecting local gateway logs that may expose user or organization identifiers. <br>
Mitigation: Inspect only the minimum log lines needed for diagnosis and avoid sharing log excerpts unless the user understands what identifiers may be revealed. <br>


## Reference(s): <br>
- [opclawtm Skill Guide](SKILL.md) <br>
- [CLI Command Reference](references/cli-reference.md) <br>
- [Installation and Activation Flow](references/installation-flow.md) <br>
- [Team Creation Flow](references/team-creation-flow.md) <br>
- [Feishu Configuration Flow](references/feishu-config-flow.md) <br>
- [Private Skill Creation Flow](references/private-skill-flow.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/poderosom1/opclawtm) <br>
- [opclawtm Homepage](https://opclawtm.com) <br>
- [Feishu Bot Tutorial](https://www.feishu.cn/content/article/7602519239445974205) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [npm Package: opclawtm](https://www.npmjs.com/package/opclawtm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include npm installation commands, opclawtm CLI commands, Feishu setup steps, and cautions around secrets and local logs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
