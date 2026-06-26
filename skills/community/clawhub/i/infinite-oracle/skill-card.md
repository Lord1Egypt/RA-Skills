## Description: <br>
Manager-first orchestration for a dedicated PECO worker: proactive installation, durable desire injection into SOUL.md, and optional Feishu-backed human-in-the-loop operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KepanWang](https://clawhub.ai/user/KepanWang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and supervise a long-running OpenClaw PECO worker that pursues ongoing objectives, records progress, accepts local overrides, and optionally syncs human-blocked tasks through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to start and supervise a long-running autonomous background worker with persistent local control. <br>
Mitigation: Run it only in an intentional sandboxed workspace with low-privilege accounts, monitor logs and state files, and stop the background process when the objective is no longer active. <br>
Risk: Free-form overrides, logs, backlog entries, and Feishu fields can capture sensitive operational details if users paste secrets or identity data into them. <br>
Mitigation: Avoid entering OTPs, payment data, identity information, API secrets, or other sensitive values into override files, logs, backlog files, or Feishu fields. <br>
Risk: Optional Feishu synchronization adds external permissions and data sharing to the loop. <br>
Mitigation: Inspect Feishu permissions and configured app/table identifiers before enabling synchronization, and prefer local file mode when external tracking is unnecessary. <br>
Risk: A live Git one-shot install path appears in the artifact documentation, while server evidence recommends the reviewed ClawHub package. <br>
Mitigation: Prefer the reviewed ClawHub release and inspect SOUL.md, AGENTS.md, ~/.openclaw/peco_override.txt, logs, and Feishu configuration before starting the loop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KepanWang/infinite-oracle) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and structured JSON expectations for worker loop output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw files for worker state, logs, overrides, SOUL.md, AGENTS.md, and optional Feishu task synchronization.] <br>

## Skill Version(s): <br>
1.0.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
