## Description: <br>
Helps secure JavaScript projects by detecting malicious npm packages, enforcing trusted publishing, verifying releases, and auditing dependencies for threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinyves](https://clawhub.ai/user/robinyves) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review npm supply-chain risks, configure trusted publishing, and apply practical dependency-audit heuristics to JavaScript projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example npm publishing workflows and token guidance could be copied into a repository without adapting permissions to the intended release process. <br>
Mitigation: Review workflows before use, prefer trusted publishing or scoped short-lived credentials, and restrict publishing permissions to the intended repository and release event. <br>
Risk: The dependency-audit snippets use simple heuristics that can produce false positives or miss malicious behavior. <br>
Mitigation: Treat snippet output as triage guidance and pair it with established package review, lockfile review, provenance checks, and security scanning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robinyves/npm-supply-chain-security) <br>
- [Publisher profile](https://clawhub.ai/user/robinyves) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON, YAML, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory content and example snippets; examples should be reviewed before use in a live release workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
