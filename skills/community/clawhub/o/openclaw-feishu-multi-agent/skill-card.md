## Description: <br>
Build and troubleshoot OpenClaw multi-agent workflows on Feishu by combining visible `<at>` mentions with `sessions_send` for reliable delegation, handoffs, and multi-hop group discussions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CCharlesMeng](https://clawhub.ai/user/CCharlesMeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and teams use this skill to build or repair OpenClaw multi-agent collaboration in Feishu groups. It helps define coordinator and specialist roles, generate OpenClaw configuration artifacts, audit existing setups, and repair Feishu group session metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Role files and generated OpenClaw configs may contain Feishu bot secrets or account identifiers. <br>
Mitigation: Use placeholders in shared examples, keep real appSecret values out of repositories and chat logs, and restrict access to generated configuration files. <br>
Risk: Write or fix modes can modify OpenClaw configuration, protocol files, identity files, or Feishu group session metadata. <br>
Mitigation: Run dry-run or audit mode first, review planned changes, and use backups before enabling --write or --fix. <br>
Risk: Incorrect role, binding, or session metadata can disrupt agent-to-agent handoffs in Feishu groups. <br>
Mitigation: Validate the roles file, audit openclaw.json against the intended roster, and test a minimal coordinator-to-specialist handoff before broader rollout. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/CCharlesMeng/openclaw-feishu-multi-agent) <br>
- [README](artifact/README.md) <br>
- [Reference guide](artifact/reference.md) <br>
- [Templates](artifact/templates.md) <br>
- [Role example](artifact/roles.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration, generated markdown files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The utility scripts default to dry-run behavior unless explicit write or fix flags are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
