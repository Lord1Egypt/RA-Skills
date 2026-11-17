## Description:

Manager-first orchestration for a dedicated PECO worker: proactive installation, durable desire injection into SOUL.md, and optional Feishu-backed human-in-the-loop operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kepanwang](https://clawhub.ai/user/kepanwang)

### License/Terms of Use:


## Use Case:

Developers and operators use Infinite Oracle to create and supervise a dedicated OpenClaw PECO worker for long-running objectives, with local-file controls and optional Feishu-backed human-in-the-loop task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous background execution can continue spending API budget or taking actions longer than intended.

Mitigation: Install only in a sandboxed OpenClaw environment with a low-privilege worker, clear API spending limits, loop logs, and a visible way to stop the nohup process.

Risk: Persistent SOUL.md changes and override channels can materially alter the worker's long-running behavior.

Mitigation: Review SOUL.md and override-file changes before they are written, preserve existing content, and keep human review around durable desire updates.

Risk: Optional Feishu sync handles credentials, network requests, and table-edited task resolution data.

Mitigation: Use Feishu sync only with trusted table editors, keep FEISHU_BASE_URL fixed to the official Feishu origin, and avoid arbitrary webhook destinations for sensitive objectives.

Risk: The authoritative scan verdict is suspicious because persistent agent changes, high-priority overrides, and credential/network handling require review.

Mitigation: Review the skill and its runtime configuration before deployment, monitor human-task backlogs and manager notifications, and disable integrations that are not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kepanwang/skills/infinite-oracle)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python/runtime configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw workspace files and start a long-running background PECO loop when installation is approved.]

## Skill Version(s):

1.0.11 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
