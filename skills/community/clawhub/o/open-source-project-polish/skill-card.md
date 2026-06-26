## Description: <br>
Turns a project folder into a polished open source repository by improving public documentation, community files, repository metadata, and Git/GitHub setup while preserving source code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openghz](https://clawhub.ai/user/openghz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to prepare an existing project for public open-source release by adding or improving documentation, community files, repository metadata, and GitHub setup while avoiding source-code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to creating and pushing to a public GitHub repository for projects without a configured remote, which can expose a project before the user has clearly approved publication. <br>
Mitigation: Require explicit user approval of the GitHub account, repository name, visibility, files to publish, and secrets-scan results before creating a remote or pushing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openghz/open-source-project-polish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file edits, inline shell commands, and concise completion summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is constrained to documentation and repository metadata changes unless the user explicitly approves source-code edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
