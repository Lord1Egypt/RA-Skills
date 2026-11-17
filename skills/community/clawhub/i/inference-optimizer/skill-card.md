## Description:

Audit OpenClaw runtime health first, then optimize inference speed and token usage with approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitalyis](https://clawhub.ai/user/vitalyis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw runtime health, identify service, allowlist, plugin, session, and token pressure issues, and apply cleanup or inference tuning only after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can modify OpenClaw workspace instructions and execution approvals.

Mitigation: Review setup.sh --apply before running it, and prefer approving only the read-only audit path unless mutating commands are needed.

Risk: Preflight backups may include sensitive local OpenClaw state or workspace data.

Mitigation: Keep backups private and treat archived OpenClaw state as sensitive.

Risk: Cleanup flows can move or delete session and memory files.

Mitigation: Use the default archive behavior first and avoid --delete unless the target files have been verified.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/vitalyis/skills/inference-optimizer)
- [Repository](https://github.com/vitalyis/inference-optimizer)
- [Homepage](https://github.com/vitalyis/inference-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval-gated remediation flow; audit path is analyze-only.]

## Skill Version(s):

0.3.4 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
