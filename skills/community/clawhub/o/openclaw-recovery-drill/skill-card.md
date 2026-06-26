## Description: <br>
OpenClaw Recovery Drill helps operators test recovery readiness, rehearse backup and restore procedures, validate recovery playbooks, and check restore confidence before upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Operators, developers, and reliability engineers use this skill to audit whether an OpenClaw workspace has recent backups, key recovery files, runbook signals, and a concrete drill plan before trusting a restore process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JSON report can expose local workspace paths, backup artifact names, timestamps, and sizes. <br>
Mitigation: Review and redact the report before sharing it outside the operator group. <br>
Risk: A readiness score is not proof that a restore has succeeded. <br>
Mitigation: Restore only into an isolated non-production path and verify startup or inspection before relying on the result. <br>
Risk: Running the checker against the wrong workspace or backup root can produce misleading recovery guidance. <br>
Mitigation: Run it only against workspaces and backup roots the operator controls, and confirm the target paths before acting on recommendations. <br>


## Reference(s): <br>
- [Recovery Drill Checklist](artifact/references/drill-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/X-RayLuan/openclaw-recovery-drill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON report with score, verdict, summary, findings, recommendations, drill plan, and evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report can include local paths, backup artifact names, timestamps, and sizes.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
