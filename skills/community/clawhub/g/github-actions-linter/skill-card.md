## Description: <br>
Lint and validate GitHub Actions workflow YAML files for common mistakes, security issues, deprecated actions, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to lint, validate, and audit GitHub Actions workflow files before committing or running CI changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide GitHub tokens or other credentials even though the linter does not need them. <br>
Mitigation: Do not provide GitHub tokens or other credentials when using this local workflow linter. <br>
Risk: Broad directory scans may include files outside the intended workflow review scope. <br>
Mitigation: Run the linter against specific workflow files or the .github/workflows/ directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/github-actions-linter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text, JSON, or Markdown lint reports with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports workflow issues by severity, rule, location, and message; strict mode can fail on warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
