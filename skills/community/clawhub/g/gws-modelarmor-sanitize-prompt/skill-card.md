## Description: <br>
Google Model Armor: Sanitize a user prompt through a Model Armor template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Google Workspace CLI commands that sanitize user prompt text through a named Google Model Armor template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content may include secrets or regulated data sent through the configured Model Armor template. <br>
Mitigation: Use only templates and Google Cloud configurations whose data-handling terms are appropriate for the submitted content. <br>
Risk: The skill depends on the local gws CLI and Google Cloud configuration. <br>
Mitigation: Install and run it only in environments where the local gws CLI, authentication, and project configuration are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-modelarmor-sanitize-prompt) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gws CLI and a configured Google Cloud environment.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
