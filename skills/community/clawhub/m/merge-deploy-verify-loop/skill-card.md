## Description: <br>
Guides an agent through a disciplined release loop from selective staging and commit through merge, CI deployment, workload restart, end-to-end verification, and patch iteration when validation fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to run an auditable merge, deploy, restart, and verification workflow after local code changes are ready. It emphasizes selective staging, target-branch confirmation, CI SHA reconciliation, workload readiness checks, API and database validation, and a new patch commit when failures require another loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real merge, deploy, restart, and verification workflows that may affect shared or production systems. <br>
Mitigation: Confirm the target branch, CI job, Kubernetes namespace, API account, database environment, and production-data scope before invoking the workflow. <br>
Risk: Deployment verification can require credentials, API calls, database assertions, and workload restarts. <br>
Mitigation: Use only approved credentials and environments, require explicit approval for production credentials or data, and follow the skill's built-in checks for destructive or ambiguous operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/merge-deploy-verify-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, reconciliation tables, and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation for ambiguous branch, environment, credential, shared-data, or destructive-operation decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
