## Description: <br>
Lint and validate Helm charts for structure, security, dependencies, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect Helm chart directories for structure, security, dependency, and Kubernetes best-practice issues before release or CI deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lint reports may include values.yaml content or findings that reveal real secrets. <br>
Mitigation: Run the skill only on chart directories intended for inspection and avoid publishing reports when values.yaml may contain sensitive values. <br>
Risk: The artifact capability tags mention wallet or sensitive credential access even though the security evidence says the skill does not need them. <br>
Mitigation: Do not provide wallet access or credentials to this skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown lint reports with command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports errors and warnings; strict mode can fail on warnings for CI use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; STATUS.md reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
