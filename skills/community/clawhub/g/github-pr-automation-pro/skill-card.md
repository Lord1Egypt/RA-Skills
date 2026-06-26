## Description: <br>
Automate GitHub pull request workflows including creation, monitoring, PR templates, auto-labeling, CI status checks, and review automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create pull requests with standardized templates, check PR readiness, assign labels and reviewers, and monitor CI and review state in GitHub repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitHub CLI commands can create or edit pull requests, and the security review recommends fixing shell command handling before use. <br>
Mitigation: Review command construction before installation, use a least-privilege GitHub account or token, test in a non-sensitive repository, and avoid untrusted PR input values. <br>
Risk: The advertised auto-merge and batch-review commands are not supplied in the artifact. <br>
Mitigation: Do not rely on those workflows unless the missing scripts are supplied and reviewed. <br>


## Reference(s): <br>
- [Automation rules](references/automation_rules.json) <br>
- [Bugfix PR template](references/pr_templates/bugfix.md) <br>
- [Feature PR template](references/pr_templates/feature.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and PR status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated GitHub CLI for repository operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
