## Description: <br>
Read and write Google Forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Google Forms commands and generate gws CLI calls for reading forms, creating forms, updating form content and publish settings, and managing responses or watches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide read and write actions against Google Forms, including batch updates, publish settings, response access, and watches. <br>
Mitigation: Install the gws CLI from a trusted source, use the intended Google account, and review generated write actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-forms) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the shared gws authentication setup.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata); skill metadata 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
