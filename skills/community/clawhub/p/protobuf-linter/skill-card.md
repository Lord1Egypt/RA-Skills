## Description: <br>
Lint Protocol Buffer (.proto) files for style, naming conventions, breaking changes, and best practices. Supports proto2 and proto3 syntax with 24 rules across structure, naming, security, and compatibility categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API engineers use this skill to lint Protocol Buffer files for style, naming, structure, compatibility, and best-practice issues before publishing or changing schemas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive linting can inspect more local .proto files than intended if it is pointed at a broad directory. <br>
Mitigation: Run it only on project paths you intend to inspect and review the path before using --recursive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; linter output can be text, JSON, or summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes 0, 1, and 2 indicate no errors, errors found, and invalid input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
