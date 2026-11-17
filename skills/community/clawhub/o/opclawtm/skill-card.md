## Description:

opclawtm CLI helps agents guide users through installing opclawtm, activating licenses, creating OpenClaw teams, configuring Feishu bots and groups, and creating private skills through the OpenClaw workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poderosom1](https://clawhub.ai/user/poderosom1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw administrators use this skill to guide opclawtm setup and operations, including npm installation, trial or key activation, team initialization, Feishu bot binding, group and user pairing, troubleshooting, and private skill creation through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad Feishu permissions and user-context scopes.

Mitigation: Review every requested Feishu scope before granting access and reduce permissions to the minimum required for the user's deployment.

Risk: The workflow asks users to copy App Secrets and inspect logs that may contain identifiers.

Mitigation: Keep App Secrets out of chat transcripts and shared logs, rotate exposed secrets, and share only the minimum identifiers needed for support.

Risk: The installation flow uses a global npm install for opclawtm.

Mitigation: Verify the npm package source and version before installation and avoid administrator privileges unless the environment requires them.

## Reference(s):

- [opclawtm ClawHub Skill Page](https://clawhub.ai/poderosom1/skills/opclawtm)
- [opclawtm Homepage](https://opclawtm.com)
- [Feishu Application Console](https://open.feishu.cn/app)
- [Feishu Bot Creation Tutorial](https://www.feishu.cn/content/article/7602519239445974205)
- [CLI Command Reference](references/cli-reference.md)
- [Installation and Activation Flow](references/installation-flow.md)
- [Team Creation Flow](references/team-creation-flow.md)
- [Feishu Configuration Flow](references/feishu-config-flow.md)
- [Private Skill Creation Flow](references/private-skill-flow.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, tables, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include Feishu permission scopes, App ID and App Secret handling steps, local OpenClaw paths, and opclawtm CLI commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
