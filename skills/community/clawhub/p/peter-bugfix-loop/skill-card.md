## Description: <br>
Guides agents through a disciplined bug-fix loop that reproduces the issue, identifies root cause, applies a minimal fix, adds tests, and connects to Peter review, CI, and PR closure workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to move a bug report from problem description to merge-ready fix with reproducible evidence, root-cause notes, minimal code changes, tests, and PR gate status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide code changes, tests, commits, PRs, and reverts when the user only intended to discuss a bug. <br>
Mitigation: Confirm intent before starting the full repair workflow and keep normal review controls in place. <br>
Risk: Bug-fix guidance can lead to incorrect or overly broad changes if the issue is not reproduced first. <br>
Mitigation: Require a minimal failing reproduction, make the smallest root-cause fix, add focused regression tests, and review gate results before closure. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Code, Shell commands] <br>
**Output Format:** [Structured Markdown bug-fix report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bug card details, reproduction evidence, root cause, changed files, test results, gate status, PR status, and a closure conclusion.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
