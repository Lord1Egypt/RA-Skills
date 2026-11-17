## Description:

Multi-Agent Orchestrator v8.2.1 provides goal-driven research and project collaboration with task decomposition, parallel execution, validation review, aggregation, and model adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjmrcft-hash](https://clawhub.ai/user/bjmrcft-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan and run multi-agent research or project workflows that decompose goals, spawn specialist agents, validate outputs, and aggregate final reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local configuration parsing can execute code from OpenClaw configuration files.

Mitigation: Remove the eval fallback in lib/modelSelector.js and use a strict JSON or reviewed JSON5 parser before running the skill.

Risk: Path handling and workflow identifiers may allow writes outside the intended workspace.

Mitigation: Validate agent and workflow identifiers, constrain all resolved paths to the expected workspace root, and review file operations before deployment.

Risk: archive_and_clean can delete shared workspace files as part of cleanup.

Mitigation: Treat archive_and_clean as destructive, run cleanup in dry-run mode first where available, and confirm archives or backups before deleting shared files.

Risk: The skill persists profiles, model settings, capability data, logs, archives, and reports under ~/.openclaw/workspace.

Mitigation: Avoid storing secrets in workflow inputs or outputs, review local files for sensitive data, and apply normal retention controls for generated artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bjmrcft-hash/skills/multi-agent-engine-v8)
- [Modules Reference](artifact/references/modules.md)
- [Runtime Protocols](artifact/references/protocols.md)
- [End-to-End Test Lessons](artifact/references/test-lessons.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON workflow plans, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reference persistent local workspace files, logs, archives, model settings, capability data, and reports under ~/.openclaw/workspace.]

## Skill Version(s):

8.2.1 (source: ClawHub release metadata, artifact skill.json, and SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
