## Description: <br>
Validate and lint Prettier configuration files for structure, invalid options, deprecated fields, override conflicts, and best practices across JSON, YAML, TOML, and package.json#prettier formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CI maintainers use this skill to check Prettier configuration files for syntax, invalid or deprecated options, override issues, and project consistency before committing or enforcing formatting in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads the local configuration path supplied by the user. <br>
Mitigation: Review the target path before running the command and prefer repository-local Prettier configuration files. <br>
Risk: CI use can fail builds when validation errors are found. <br>
Mitigation: Run the validator locally or in a nonblocking CI step before making it a required gate, then review the reported issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/prettierrc-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; validator output can be text, JSON, or summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate success, validation errors, or invalid input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
