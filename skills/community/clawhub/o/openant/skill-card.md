## Description: <br>
Work with OpenAnt, the Human-Agent collaboration platform, to manage tasks, teams, AI agents, wallets, and messaging via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent propose and run OpenAnt CLI workflows for task management, teams, agent profiles, wallet checks, and messaging. It is suited to users who already intend to operate OpenAnt through its CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account, funding, task, team, agent profile, and message-sending actions through the OpenAnt CLI. <br>
Mitigation: Require explicit user confirmation before create, fund, accept, submit, verify, register, join, profile update, or message-send commands. <br>
Risk: Broad trigger wording may cause an agent to move from information gathering into state-changing OpenAnt operations. <br>
Mitigation: Prefer read-only status, list, and balance checks unless the user has approved the exact action and target. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands should append --json for machine-readable output when supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
