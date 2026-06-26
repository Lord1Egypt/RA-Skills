## Description: <br>
Google Model Armor: Sanitize a model response through a Model Armor template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route generated model responses through a configured Google Model Armor template before returning content to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends response content to the configured Google service for sanitization. <br>
Mitigation: Use least-privilege Google credentials and avoid sending content that should not be processed by the configured service. <br>
Risk: Using the wrong Model Armor template can apply unintended sanitization behavior. <br>
Mitigation: Verify the target Model Armor template resource before running the command. <br>
Risk: The skill depends on generated shared gws instructions and the gws CLI. <br>
Mitigation: Install only if you trust the gws CLI and the generated shared gws instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-modelarmor-sanitize-response) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI flag guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and a configured Google Model Armor template.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
