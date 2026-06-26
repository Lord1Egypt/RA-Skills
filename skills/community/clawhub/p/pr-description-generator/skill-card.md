## Description: <br>
Auto-generates structured pull request descriptions from git diffs and commit history, with conventional commit parsing, impact analysis, reviewer hints, and Markdown or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to summarize branch changes, prepare pull request bodies, and generate reviewer-oriented PR descriptions from local git diffs and commit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local git diffs and commit messages, which may include sensitive repository-derived text. <br>
Mitigation: Review generated output before posting it and avoid clipboard use on sensitive repositories unless sharing that text is intended. <br>
Risk: The optional output path can create or overwrite a file selected by the user. <br>
Mitigation: Use the output option only with a path that is acceptable to create or replace. <br>
Risk: Generated pull request summaries may omit context or misstate the intent of changes. <br>
Mitigation: Treat generated descriptions as drafts and have a developer review them before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/pr-description-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown pull request description by default, with optional JSON output and optional file or clipboard delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can compare against a selected base branch, inspect another repository path, choose minimal, standard, or detailed templates, and save or copy generated output when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
