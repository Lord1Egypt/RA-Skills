## Description: <br>
Validate and lint Maven pom.xml files for structure, dependencies, plugins, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate, lint, and audit Maven pom.xml files before release or CI integration. It helps identify structural XML errors, dependency hygiene issues, plugin configuration problems, and Maven best-practice gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Python script against a chosen Maven POM file. <br>
Mitigation: Review the bundled script before installation and run it only on intended pom.xml files in a trusted workspace. <br>
Risk: Strict-mode failures can block CI when warnings are present. <br>
Mitigation: Review reported findings before enabling strict mode in CI and tune adoption around the project's release policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charlie-morrison/maven-pom-validator) <br>
- [Maven POM 4.0.0 namespace](http://maven.apache.org/POM/4.0.0) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with pass/fail status and findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports lint, validate, dependencies, and plugins modes; strict mode exits nonzero on warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
