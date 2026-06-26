## Description: <br>
Coder-focused incident response and hotfix execution for production issues requiring reproducible triage, patch or rollback decisions, CI-safe hotfix branches, evidence capture, and postmortem action tracking tied to code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill during production incidents when code-level action is required. It guides severity classification, hotfix branch setup, focused validation, rollback planning, evidence capture, and postmortem action tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the hotfix setup script in the wrong repository or from the wrong production base could create misleading incident artifacts or branch from the wrong code. <br>
Mitigation: Confirm the intended repository and production base branch or commit before running the script. <br>
Risk: Captured evidence files may include repository state, diffs, changed file lists, and selected environment metadata that should be reviewed before sharing. <br>
Mitigation: Review generated evidence files before committing, attaching to tickets, or distributing them outside the incident team. <br>
Risk: Hotfix guidance can lead to incorrect or incomplete remediation if the incident root cause is uncertain. <br>
Mitigation: Use containment first when root cause is unclear, document the rollback path, and require focused tests before merge. <br>


## Reference(s): <br>
- [Corrective Actions Template](references/action-template.md) <br>
- [Severity Matrix (Code/Service)](references/severity-matrix.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Broedkrummen/incident-hotfix) <br>
- [Publisher Profile](https://clawhub.ai/user/Broedkrummen) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and generated incident documentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local incident workspace files and an evidence bundle under docs/incidents/<id>/ when the bundled scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
