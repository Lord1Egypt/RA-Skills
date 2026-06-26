## Description: <br>
Define, measure, and enforce web performance budgets for bundle sizes, asset counts, image weights, third-party scripts, and CI budget failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after a web project build to measure static asset size, define performance budgets, enforce budget checks in CI, track trends, and identify optimization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update local performance budget and history files. <br>
Mitigation: Review proposed .perfbudget.json and .perfbudget-history.json changes before committing them. <br>
Risk: CI enforcement can fail builds if budgets are set too aggressively or before baseline measurements are calibrated. <br>
Mitigation: Start enforcement in a non-blocking or calibrated mode, then tighten budgets after representative build measurements are available. <br>
Risk: Measurements depend on existing build artifacts and can be misleading if run before the intended build output exists. <br>
Mitigation: Run the skill from the target repository after a successful build and verify the detected build output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/performance-budget-enforcer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, CI snippets, human-readable reports, machine-readable JSON, PR comment markdown, and GitHub annotations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update .perfbudget.json and .perfbudget-history.json when the agent applies the budget or trend workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
