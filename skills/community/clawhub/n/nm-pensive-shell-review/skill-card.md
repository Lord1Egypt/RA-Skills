## Description: <br>
Audits shell scripts for correctness, portability, and common pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review shell scripts used in CI/CD pipelines, hooks, wrappers, and build automation for reliability, portability, and safety issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad shell or CI-related wording outside the intended review context. <br>
Mitigation: Use it when reviewing shell scripts and confirm the target files before acting on findings. <br>
Risk: Suggested package-manager, ShellCheck, or formatting commands may change local tools or files. <br>
Mitigation: Review proposed commands before execution and inspect any resulting file changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-shell-review) <br>
- [Source homepage from package metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands] <br>
**Output Format:** [Markdown review with file references, categorized findings, recommendations, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized around scripts reviewed, exit-code behavior, portability, safety patterns, structure, and an approval recommendation.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
