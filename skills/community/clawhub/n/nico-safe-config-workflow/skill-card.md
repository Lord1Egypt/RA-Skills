## Description: <br>
Guides agents through a confirmation-first workflow for safely changing OpenClaw configuration, running checks, applying fixes, and validating Gateway status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when modifying OpenClaw Gateway, channel, model, session, authentication, or other local OpenClaw configuration settings. It helps the agent confirm planned changes, run doctor checks, review backups and diffs, record lessons, and verify Gateway health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to local OpenClaw configuration files. <br>
Mitigation: Keep each change explicitly OpenClaw-scoped, confirm exact fields and expected impact before editing, and review backups and diffs after doctor --fix. <br>
Risk: Gateway checks or restart tests can temporarily disrupt active Gateway use. <br>
Mitigation: Avoid disruptive tests during important Gateway activity and verify Gateway status after changes. <br>
Risk: Lessons recorded to MEMORY.md could accidentally include sensitive values. <br>
Mitigation: Do not write secrets, tokens, or authentication material into MEMORY.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicoxia/nico-safe-config-workflow) <br>
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor) <br>
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md) <br>
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting) <br>
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with confirmation text, status summaries, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow expects user confirmation before edits and summarizes doctor, diff, log, and Gateway status results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
