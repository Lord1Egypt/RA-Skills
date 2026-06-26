## Description: <br>
Use the linear-cli agent-native runtime to read and mutate Linear from Claude Code, Codex, or other agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyaukyuai](https://clawhub.ai/user/kyaukyuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect and update Linear workspaces through the linear CLI. It supports issue, project, cycle, document, notification, webhook, label, user, workflow-state, schema, and raw GraphQL API workflows with JSON-oriented command output and dry-run previews where supported. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live access to mutate, delete, upload to, and make raw API calls against Linear. <br>
Mitigation: Install only when the agent is intended to operate with Linear credentials, use the least-privileged workspace credentials available, and require explicit approval for raw API, curl, delete, archive, and bulk operations. <br>
Risk: Linear credentials or authentication tokens may be exposed if token-printing or curl workflows are used carelessly. <br>
Mitigation: Avoid exposing `linear auth token`, review command output before sharing logs, and verify the external `linear` CLI source and version before use. <br>
Risk: File and context upload workflows can send sensitive local content to Linear. <br>
Mitigation: Review file inputs and source-context envelopes before upload, and prefer dry-run previews where supported. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyaukyuai/kyaukyuai-linear-cli) <br>
- [Linear CLI installation instructions](https://github.com/kyaukyuai/linear-cli?tab=readme-ov-file#install) <br>
- [Agent-facing capabilities](references/capabilities.md) <br>
- [Command reference](references/commands.md) <br>
- [Authentication](references/auth.md) <br>
- [Issues](references/issue.md) <br>
- [Projects](references/project.md) <br>
- [Raw GraphQL API](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash examples and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Linear workspace credentials and may perform live mutations, deletes, uploads, and raw API calls when the agent executes the generated commands.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
