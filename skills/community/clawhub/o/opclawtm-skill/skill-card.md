## Description: <br>
Guides an agent in helping users install, activate, configure, and troubleshoot the opclawtm CLI for OpenClaw team workflows, while directing users to perform business-data changes in the TUI themselves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poderosom1](https://clawhub.ai/user/poderosom1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to guide opclawtm installation, license activation, team setup, Feishu bot configuration, private skill creation, and troubleshooting. The skill separates commands the agent may run from TUI workflows that require direct user control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu setup asks for broad workspace permissions. <br>
Mitigation: Use a test workspace first, reduce Feishu scopes where possible, and grant production access only after review. <br>
Risk: The troubleshooting flow can involve reading local gateway logs that may contain identifiers or sensitive operational data. <br>
Mitigation: Do not allow the agent to print raw gateway logs; extract only the specific identifier needed and redact unrelated log content. <br>
Risk: The skill depends on installing and trusting the third-party opclawtm npm package. <br>
Mitigation: Install only after reviewing the package source and publisher, and revoke or rotate Feishu credentials after testing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/poderosom1/opclawtm-skill) <br>
- [opclawtm homepage](https://opclawtm.com) <br>
- [CLI command reference](references/cli-reference.md) <br>
- [Installation and activation flow](references/installation-flow.md) <br>
- [Team creation flow](references/team-creation-flow.md) <br>
- [Feishu configuration flow](references/feishu-config-flow.md) <br>
- [Private skill creation flow](references/private-skill-flow.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Feishu bot tutorial](https://www.feishu.cn/content/article/7602519239445974205) <br>
- [Feishu open platform app console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands, checklists, and TUI navigation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to run environment-preparation and query commands, but to guide the user through TUI operations for business-data creation or modification.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
