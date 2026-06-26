## Description: <br>
Configures free opencode.ai AI models in local OpenClaw or QClaw model settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinke](https://clawhub.ai/user/pinke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw or QClaw use this skill to fetch opencode.ai models whose IDs include "free" and add them to the local model provider configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent local changes to OpenClaw or QClaw model routing configuration. <br>
Mitigation: Review or back up the existing openclaw.json file before running the skill. <br>
Risk: The skill contacts opencode.ai to retrieve the model list used for configuration. <br>
Mitigation: Run it only when that network dependency is acceptable and the user wants OpenClaw or QClaw to use opencode.ai free models. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pinke/opencode-free-models) <br>
- [Publisher profile](https://clawhub.ai/user/pinke) <br>
- [opencode.ai models endpoint](https://opencode.ai/zen/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist changes to ~/.openclaw/openclaw.json or ~/.qclaw/openclaw.json and uses the public API key value "public".] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
