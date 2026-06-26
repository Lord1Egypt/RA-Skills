## Description: <br>
Discover valuable GitHub issues with smart positive-label detection and analyze bug fix feasibility for open source contribution opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find, prioritize, and evaluate GitHub issues before contributing fixes, features, or documentation updates. It helps identify positive maintainer signals, estimate effort, assess project health, and produce structured issue analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill expects GitHub CLI use and may access issue, pull request, label, and repository metadata for repositories selected by the user. <br>
Mitigation: Run it only against repositories you intend to inspect and review GitHub CLI authentication scope before use. <br>
Risk: Generated issue recommendations or feasibility assessments may be incorrect or incomplete. <br>
Mitigation: Review the analysis before posting comments, opening pull requests, or committing to implementation work. <br>
Risk: The optional output path can create or overwrite a report file. <br>
Mitigation: Use the output option only for file paths you intend to create or replace. <br>


## Reference(s): <br>
- [Issue Analysis Report Template](references/analysis-template.md) <br>
- [Issue Evaluation Criteria](references/evaluation-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional Markdown analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GitHub CLI commands against selected repositories and may write an optional report file when an output path is provided.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
