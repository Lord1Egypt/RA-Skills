## Description: <br>
A command-line skill advertised to draft JSON schema structure from JSON samples and write command output plus JSON or text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askjda](https://clawhub.ai/user/askjda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill in command-line workflows to process JSON sample files, write output artifacts, and record reproducible commands. Users should review the output before relying on it because the server security review reports that the advertised schema-drafting behavior appears incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised JSON schema drafting behavior appears incomplete. <br>
Mitigation: Review generated output before relying on it and verify any schema content manually. <br>
Risk: Undisclosed network options can send local file contents to arbitrary web endpoints when endpoint and payload arguments are used. <br>
Mitigation: Do not run network-related arguments unless intentionally sending that exact file to that exact destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askjda/json-schema-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Command-line guidance with stdout plus JSON or text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the path supplied with --output; network options should only be used intentionally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
