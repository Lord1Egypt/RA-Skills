## Description: <br>
Setup and utility scripts for muapi.ai: configure API keys, test connectivity, and poll for async generation results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anil-matcha](https://clawhub.ai/user/Anil-matcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure MuAPI credentials, verify MuAPI CLI access, and check asynchronous prediction results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed when passed directly on the command line or stored in shell history. <br>
Mitigation: Prefer running setup without an inline key so the MuAPI CLI can prompt securely, avoid long-lived keys in commands, and rotate any key that may have been exposed. <br>
Risk: The scripts invoke the local muapi command, so a user could run an unexpected binary if their PATH is misconfigured. <br>
Mitigation: Confirm which muapi command will run before executing the scripts and install the MuAPI CLI only from a trusted MuAPI source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anil-matcha/muapi-platform) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MuAPI CLI commands that configure credentials, inspect account configuration, or poll prediction results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
