## Description: <br>
Polishes working code through successive correctness, clarity, consistency, and production-readiness passes in fresh subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after tests pass to iteratively refine working code across correctness, clarity, consistency, and release polish before review or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs tests and makes iterative edits to selected code, which can introduce regressions or unintended behavior. <br>
Mitigation: Review all code changes and test results before release, and keep the workflow focused on working code that already passes basic tests. <br>
Risk: The workflow stores resume state in a local .attune state file that may include target paths and pass history. <br>
Mitigation: Inspect or remove .attune/dorodango-state.json when state should not persist across sessions or be shared. <br>
Risk: A polishing run may continue across multiple passes even when the target is too broad for reliable convergence. <br>
Mitigation: Use the 10-pass cap as a stop point and split large or unresolved targets into smaller units before continuing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-dorodango) <br>
- [clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [Pass definitions](artifact/modules/pass-definitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown workflow guidance with shell/test execution, code edit recommendations, and JSON state tracking] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a local .attune/dorodango-state.json resume file and caps the polishing workflow at 10 passes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
