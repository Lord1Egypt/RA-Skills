## Description: <br>
Provides review-workflow scaffolding for context, evidence, and output so detailed reviews produce consistent, comparable findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and agents use this skill at the start of review workflows to establish context, inventory scope, capture evidence, structure findings, and document contingencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language may cause the skill to influence more review workflows than intended. <br>
Mitigation: Narrow trigger phrases or invocation rules when only specific review types should use this workflow. <br>
Risk: Review scaffolding can lead to incomplete or misleading conclusions if evidence is not actually captured. <br>
Mitigation: Require concrete commands, file paths, or citations in the evidence log before relying on findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-review-core) <br>
- [Imbue plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with checklist items and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review scaffolding for downstream analysis; no hidden execution was reported by ClawScan.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
