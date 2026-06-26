## Description: <br>
Validates Jest configuration files and package.json Jest settings for deprecated options, transform conflicts, coverage misconfigurations, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Jest test runner configuration, migration readiness, transform setup, coverage settings, and CI-friendly validation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict mode converts warnings into errors and may block CI on findings that require project-specific review. <br>
Mitigation: Run non-strict validation first, review the reported findings, and enable strict mode only after the team accepts the resulting CI gate. <br>
Risk: The bundled checker is intended for Jest config files and package.json Jest settings; applying it outside that scope can produce irrelevant findings. <br>
Mitigation: Use it only on intended Jest configuration inputs and review results before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/jest-config-validator) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Validator script](artifact/scripts/jest_config_validator.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or one-line summary output from local validation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, json, and summary output formats with exit codes for CI use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
