## Description: <br>
PigBun RedNote helps agents automate RedNote workflows for search, content publishing, comment management, social interaction, and account analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PigBun-AI](https://clawhub.ai/user/PigBun-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, operators, and developers use this skill to connect an OpenClaw agent to PigBun's RedNote tools for account operations such as searching posts, publishing content, managing comments, and generating analytics reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live RedNote account actions including publishing, editing, deleting, commenting, following, liking, and collecting content. <br>
Mitigation: Use a test or low-value RedNote account first and require explicit per-action approval before enabling publish, delete, edit, comment, follow, or collect operations. <br>
Risk: The skill requires a PigBun API key and an authenticated browser session. <br>
Mitigation: Keep the API key out of shared files and chats, verify pigbunai.com and the publisher profile before installation, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PigBun-AI/pigbun-rednote) <br>
- [PigBun AI website](https://pigbunai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown and natural-language agent responses with JSON configuration examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PigBun API key, Playwright Chromium setup, and an authenticated RedNote session before live account actions.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
