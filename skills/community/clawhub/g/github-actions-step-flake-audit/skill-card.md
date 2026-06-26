## Description: <br>
Detect flaky GitHub Actions job steps by finding mixed success/failure conclusions across runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze exported GitHub Actions run JSON and identify job steps that alternate between passing and failing across workflow runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub Actions JSON exports may include repository names, branches, run IDs, job and step names, and GitHub URLs. <br>
Mitigation: Keep RUN_GLOB narrow and run the skill only against intended local exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-step-flake-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON summary with ranked flaky step groups and optional CI fail gate behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; reads local GitHub Actions JSON exports matched by RUN_GLOB.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
