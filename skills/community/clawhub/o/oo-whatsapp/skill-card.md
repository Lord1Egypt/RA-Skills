## Description: <br>
WhatsApp (whatsapp.com). Use this skill for WhatsApp requests involving reading, creating, updating, and deleting data through the OOMOL WhatsApp connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external operators, and developers use this skill to inspect WhatsApp Business account data, send WhatsApp messages, manage media, and create or delete WhatsApp message templates through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected WhatsApp account. <br>
Mitigation: Install only for trusted workspaces and review requested permissions before use. <br>
Risk: Write actions can send WhatsApp messages, upload media, or create message templates. <br>
Mitigation: Confirm the exact recipient, payload, and expected effect before running write actions. <br>
Risk: The destructive template deletion action removes all variants sharing the same template name. <br>
Mitigation: Require explicit approval for the target template name before running destructive actions. <br>


## Reference(s): <br>
- [WhatsApp homepage](https://www.whatsapp.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-whatsapp) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before action execution and returns connector responses as JSON when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
