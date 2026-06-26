## Description: <br>
Json Formatter Pro helps agents format, validate, minify, sort, diff, and query JSON locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, API testers, and data-processing users can use this skill to format, validate, compact, sort, compare, and extract values from JSON during local workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive JSON supplied directly as command-line arguments may be exposed through shell history or process listings. <br>
Mitigation: Avoid passing highly sensitive JSON directly on the command line; use less exposed local handling patterns when sensitive data is involved. <br>
Risk: The query behavior is a simple local JSONPath-like helper and may not match full JSONPath or JMESPath semantics. <br>
Mitigation: Review query results before relying on them for important decisions or automation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/darbling/json-utility-tools) <br>
- [Publisher profile](https://clawhub.ai/user/darbling) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text and JSON emitted by local command-line actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on JSON strings supplied to the local script; no network access or credential use is reported in the security evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
