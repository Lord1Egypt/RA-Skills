## Description:

OpenClaw Recovery Drill helps operators audit OpenClaw recovery readiness by scoring backup signals, restore-readiness gaps, and next drill actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to check whether a workspace has recent backups, core recovery files, runbook signals, and a practical drill plan before upgrades or incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The readiness report can expose local workspace paths, backup locations, artifact names, and recovery gaps.

Mitigation: Share results only with operators who are allowed to inspect the target workspace and backup paths.

Risk: A readiness score does not prove that a full restore will succeed.

Mitigation: Run any actual restore in an isolated test path and verify startup or inspection before relying on the backup.

Risk: Running the audit against implicit defaults may inspect unintended local OpenClaw paths.

Mitigation: Pass explicit --workspace and --backup-root paths for the environment the operator intends to assess.

## Reference(s):

- [Recovery Drill Checklist](references/drill-checklist.md)
- [OpenClaw Recovery Drill on ClawHub](https://clawhub.ai/x-rayluan/skills/openclaw-recovery-drill)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON readiness report with score, verdict, findings, recommendations, drillPlan, and evidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local workspace paths, backup locations, artifact names, and recovery gaps.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
