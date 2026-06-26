## Description: <br>
Multi Agent Config Manager orchestrates OpenClaw multi-agent workflows for goal-driven research and project collaboration, including task decomposition, parallel execution, validation, review, rework, aggregation, and configuration checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjmrcft-hash](https://clawhub.ai/user/bjmrcft-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to coordinate multi-agent research or project workflows, validate outputs, manage retries and review loops, and set up the workspace directories and agent configuration needed for those workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw configuration from local files, and unsafe or untrusted changes to ~/.openclaw/openclaw.json could affect execution. <br>
Mitigation: Install and run it only in trusted OpenClaw workspaces where untrusted users or tools cannot modify OpenClaw configuration. <br>
Risk: The skill can create, archive, and clean files under the OpenClaw workspace, including shared output directories. <br>
Mitigation: Back up ~/.openclaw/workspace/shared before cleanup or archive operations and prefer dry-run cleanup where available. <br>
Risk: The release evidence shows inconsistent package identity across display name, slug, and internal skill naming. <br>
Mitigation: Confirm the intended ClawHub package, publisher handle, and installed skill name before deploying it to a production workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bjmrcft-hash/multi-agent-config-manager) <br>
- [Publisher profile](https://clawhub.ai/user/bjmrcft-hash) <br>
- [Module reference](artifact/references/modules.md) <br>
- [Runtime protocols](artifact/references/protocols.md) <br>
- [End-to-end test lessons](artifact/references/test-lessons.md) <br>
- [Release notes v7.2.0](artifact/RELEASE_v7.2.0.md) <br>
- [Pre-release audit v7.2.0](artifact/AUDIT_v7.2.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON plans, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw workspace directories, agent configuration, logs, reports, archives, and cleanup outputs during execution.] <br>

## Skill Version(s): <br>
7.2.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
