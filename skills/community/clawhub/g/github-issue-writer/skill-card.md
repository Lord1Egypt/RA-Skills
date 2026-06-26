## Description: <br>
Generates structured GitHub issue cards for WeBuddhist API endpoint documentation from OpenAPI specs, natural language, inline details, or existing issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tech-lo](https://clawhub.ai/user/Tech-lo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn API endpoint information into scannable GitHub issue cards and, after review, create and link approved issues to a selected repository and project board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated issue body, selected repository, or project board may not match the user's intent. <br>
Mitigation: Review the generated card, target repository, and project board before approving issue creation. <br>
Risk: GitHub CLI commands may run under the wrong account or without the project scope needed to link issues. <br>
Mitigation: Confirm GitHub CLI authentication and refresh the project scope before running project commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tech-lo/github-issue-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown issue-card template with optional GitHub CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review and approval before issue creation; unknown endpoint details are marked [TBD].] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
