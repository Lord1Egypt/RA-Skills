## Description: <br>
Universal LG ThinQ device manager that discovers appliances, helps users obtain and configure LG ThinQ credentials, and generates device-specific OpenClaw skills for home automation control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UtkarshTheDev](https://clawhub.ai/user/UtkarshTheDev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover LG ThinQ appliances connected to their account, create local per-device control skills, and operate supported appliances through OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an LG ThinQ Personal Access Token that can list and control appliances on the user's account. <br>
Mitigation: Install only from a trusted publisher, use the least privilege available for the PAT, keep the token in the shell environment or universal skill root, and avoid copying it into generated device folders. <br>
Risk: Generated commands can perform physical device actions through the LG ThinQ API. <br>
Mitigation: Review each setup manifest and generated command before approval, then verify device state before and after mutating controls. <br>
Risk: The skill workflow asks the agent to persist trigger phrases, skill paths, and command summaries in global memory. <br>
Mitigation: Decline or remove global MEMORY.md persistence unless those device details should be retained across sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/UtkarshTheDev/lg-thinq-universal) <br>
- [LG ThinQ PAT portal](https://connect-pat.lgthinq.com) <br>
- [LG ThinQ API technical reference](references/api-reference.md) <br>
- [Manual setup guide](references/manual-setup.md) <br>
- [Device skill generation guide](references/skill-generation-guide.md) <br>
- [Device skill template](references/device-skill-template.md) <br>
- [Generated device skill example](references/device-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated Python, JSON, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local device profiles and per-device skill workspaces after user-confirmed setup steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
