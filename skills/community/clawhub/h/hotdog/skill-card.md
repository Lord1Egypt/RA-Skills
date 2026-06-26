## Description: <br>
Hot dog or not? Classify food photos and battle Nemotron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mishafyi](https://clawhub.ai/user/mishafyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to classify submitted food photos as hot dogs or not, compare the agent's description against Nemotron in a blind battle, and return the battle result and reveal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected food photos, model names, answers, and descriptions to a third-party service. <br>
Mitigation: Use only when the user explicitly requests a hotdog battle or consents to the upload, and review the service's retention and sharing practices before deployment. <br>
Risk: The skill text exposes a shared API token used for the battle API. <br>
Mitigation: Remove or rotate the exposed token and use a scoped secret supplied by the runtime before deployment. <br>
Risk: The security verdict is suspicious because the upload behavior and exposed token create privacy and credential exposure concerns. <br>
Mitigation: Review the clawscan guidance, narrow activation to explicit requests, and document the data sent to the third-party API. <br>


## Reference(s): <br>
- [Hotdog ClawHub Page](https://clawhub.ai/mishafyi/hotdog) <br>
- [Publisher Profile](https://clawhub.ai/user/mishafyi) <br>
- [Hot Dog or Not Battle](https://hotdogornot.xyz/battle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown text with shell command execution steps and API-derived battle results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and image input for the battle workflow; no-photo activation returns a prompt to send a photo.] <br>

## Skill Version(s): <br>
10.1.1 (source: server release evidence; artifact frontmatter lists 10.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
