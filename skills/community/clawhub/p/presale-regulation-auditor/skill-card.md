## Description: <br>
Audit regulation freshness and update policy-driven controls without hardcoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTsiomo](https://clawhub.ai/user/DTsiomo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operations, compliance, and engineering teams use this skill to compare current sales or process regulations against operational behavior and incidents, then produce evidence-backed policy and configuration change proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated policy or configuration diffs may be incorrect or misaligned with current regulation, incidents, or operations. <br>
Mitigation: Review every proposed diff against authoritative regulation sources, incident history, and active operational behavior before applying it. <br>
Risk: The workflow may recommend code changes when configuration cannot express the needed control. <br>
Mitigation: Treat code-change recommendations as proposals requiring engineering review, testing, and normal change approval before implementation. <br>


## Reference(s): <br>
- [Regulation Check Workflow](references/regulation-check-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/DTsiomo/presale-regulation-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, configuration, code] <br>
**Output Format:** [Markdown report with staleness matrix, proposed configuration diffs, backward-compatibility notes, and rollout recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated config diffs and code-change recommendations are proposals for human review before application.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
