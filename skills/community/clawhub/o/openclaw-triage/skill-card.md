## Description:

OpenClaw Triage investigates agent workspace compromises, builds timelines, assesses blast radius, and collects forensic evidence by correlating local OpenClaw security-tool data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and security responders use this skill to investigate suspicious changes in agent workspaces, reconstruct timelines, estimate blast radius, and preserve forensic evidence before recovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has workspace write authority and includes automated remediation paths that can move or delete skills, overwrite files, and run scripts from the workspace being investigated.

Mitigation: Use read-only investigation, timeline, scope, status, and evidence commands first; run containment, remediation, and protection commands only after reviewing their actions, making backups, and limiting filesystem privileges.

Risk: Generated evidence bundles may contain source code, hashes, audit data, security-tool state, and other sensitive workspace details.

Mitigation: Store evidence bundles in access-controlled locations, share them only with responders who need them, and handle retention or deletion according to the incident-response process.

## Reference(s):

- [Openclaw Triage on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-triage)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text reports, Markdown guidance, JSON evidence and report files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard library only. Evidence bundles may contain workspace file hashes, audit data, security-tool state, and copied local security-tool data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
