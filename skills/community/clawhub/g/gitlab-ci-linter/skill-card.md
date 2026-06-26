## Description: <br>
Lint and validate GitLab CI/CD pipeline YAML files (.gitlab-ci.yml) for syntax errors, security issues, deprecated patterns, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to lint, validate, audit, and inspect GitLab CI/CD pipeline YAML before committing or publishing pipeline changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When given a directory, the linter recursively reads .yml and .yaml files, which may include unrelated configuration or secret-bearing YAML. <br>
Mitigation: Run it on a specific .gitlab-ci.yml file or a narrowly scoped CI directory unless broad repository YAML review is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/gitlab-ci-linter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown issue reports with file, line, severity, rule, and summary details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command exit status indicates whether errors were found, and strict mode can fail on warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
