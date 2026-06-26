## Description: <br>
Use for Pixelhub API direct calls when users need image generation or editing, video generation or post-processing, or audio and music generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leik1000](https://clawhub.ai/user/leik1000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover Pixelle/Pixelhub media workflow tools, submit generation or editing jobs, and poll task results through the bundled Python runner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance asks users to share or store an API key in ways that can expose credentials. <br>
Mitigation: Use the Pixelhub_API_KEY environment variable or a secret manager, avoid pasting keys into chat or hardcoding them, and rotate any key that has already been shared or stored in files. <br>
Risk: Media generation calls may consume paid Pixelle/Pixelhub credits or incur service costs. <br>
Mitigation: Confirm pricing, balance, and intended parameters before running generation jobs. <br>


## Reference(s): <br>
- [Pixelle Labs](https://www.pixellelabs.com/) <br>
- [Pixelle API Keys](https://www.pixellelabs.com/user/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/leik1000/pixelhub-api-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Python runner to list tools, validate parameters against server schemas, submit tasks, and poll for completion.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
