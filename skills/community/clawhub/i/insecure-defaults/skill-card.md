## Description: <br>
Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atlas-secint](https://clawhub.ai/user/atlas-secint) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and reviewers use this skill to audit production-reachable code and configuration for fail-open defaults such as hardcoded secrets, weak authentication, permissive access, weak cryptography, and debug behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches code and configuration and may encounter real secrets. <br>
Mitigation: Use it only on repositories the operator is authorized to audit and require reports to redact secret values. <br>
Risk: The skill may propose Bash search commands during an audit. <br>
Mitigation: Review commands before execution and keep searches scoped to the intended repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atlas-secint/insecure-defaults) <br>
- [Insecure Defaults Examples and Counter-Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with findings, verification notes, and suggested search commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include evidence, production impact, and exploitation notes without exposing secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
