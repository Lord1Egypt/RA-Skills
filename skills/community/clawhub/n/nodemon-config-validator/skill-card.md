## Description: <br>
Validate nodemon config files (nodemon.json, .nodemonrc, package.json#nodemonConfig) for watch settings, ignore patterns, exec conflicts, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate and audit Node.js nodemon configurations for local development and CI workflows. It helps identify configuration conflicts, watch performance issues, risky exec patterns, and best-practice gaps before the config is relied on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation output can include local paths, exec commands, and environment variable names from nodemon configuration files. <br>
Mitigation: Run the validator only on config files you intend to inspect, and avoid publishing or sharing output when it contains sensitive project details. <br>
Risk: The skill runs a local Python script from the release artifact. <br>
Mitigation: Review the artifact and run it in the intended local workspace; the server security evidence reports no network, credential, persistence, or mutation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/nodemon-config-validator) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Release status](artifact/STATUS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with bash examples; validator output can be text, JSON, or one-line summary reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI-friendly exit codes; strict mode can promote warnings and info findings to errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
