## Description: <br>
Validate .pre-commit-config.yaml files for structure, repository entries, hook definitions, local hooks, and best practices. 23 rules across 5 categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check pre-commit configuration files before committing or publishing them. It helps identify malformed YAML, missing repository or hook fields, unsafe floating revisions, duplicate entries, local hook issues, and best-practice warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads user-specified local YAML files and can print paths and configuration-derived diagnostics to the terminal. <br>
Mitigation: Run it only on files intended for inspection, and avoid pasting or logging outputs from sensitive workflows without review. <br>
Risk: The bundled parser may fall back to a basic YAML parser when PyYAML is unavailable, which can be less complete for complex YAML constructs. <br>
Mitigation: Use PyYAML where possible and manually review unusual YAML features or parser-related diagnostics before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/pre-commit-config-validator) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [CLI validation reports in text, JSON, or summary format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish pass, validation errors, and parse or input errors; --strict treats warnings as errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
