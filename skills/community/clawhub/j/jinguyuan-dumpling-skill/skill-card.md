## Description: <br>
Jinguyuan Dumpling Skill helps agents answer questions about Jinguyuan Dumpling Restaurant, retrieve restaurant service information, and handle Meituan queue actions such as taking, checking, or canceling a number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinguyuan](https://clawhub.ai/user/jinguyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer restaurant questions, get current service details, surface pickup links, and perform user-confirmed queue operations for Jinguyuan Dumpling Restaurant. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The embedded queue and login flow uses Meituan account authorization and may cache tokens locally. <br>
Mitigation: Install only for a trusted publisher and avoid shared or production machines; use the minimum needed account authorization and clear local credentials after use where supported. <br>
Risk: The embedded authentication flow can install global software or change local tooling. <br>
Mitigation: Review the bundled install and authentication scripts before use and run them in an isolated user environment when possible. <br>
Risk: The embedded queue component can automatically fetch remote updates and modify local skill files. <br>
Mitigation: Review and rescan the skill after any update notice before repeating queue operations. <br>
Risk: Queue actions and cancellation are real business actions tied to the user's restaurant visit. <br>
Mitigation: Require explicit user confirmation before taking or canceling a queue number. <br>
Risk: Pickup and ordering responses can include clickable links. <br>
Mitigation: Verify that the destination and requested action match the user's intent before opening or presenting the link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinguyuan/jinguyuan-dumpling-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jinguyuan) <br>
- [README](README.md) <br>
- [Machine-readable skill configuration](skill.json) <br>
- [Embedded Meituan queue skill](references/meituan-queue/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, links, and shell-command steps for embedded queue operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live restaurant data, clickable pickup links, and queue status or action results from external services.] <br>

## Skill Version(s): <br>
0.6.6 (source: frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
