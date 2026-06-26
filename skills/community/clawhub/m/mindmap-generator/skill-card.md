## Description: <br>
Generates visual mindmap images from conversations, goals, decisions, and daily priorities, delivered as PNG images viewable directly in Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParasHarnagle](https://clawhub.ai/user/ParasHarnagle) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to turn conversations, goals, daily priorities, decisions, meeting notes, and weekly reviews into readable mindmap images for Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mindmaps may contain private conversation, calendar, memory, priority, or meeting-note content that is sent through Telegram. <br>
Mitigation: Use only approved Telegram destinations, verify the chat ID before sending, avoid regulated or confidential material unless Telegram is approved for that use, and get clear user intent before sending sensitive content. <br>
Risk: A misconfigured or exposed Telegram bot token could send images or fallback text to unintended recipients. <br>
Mitigation: Use a dedicated bot token for the intended chat, store it as a secret environment variable, restrict bot usage operationally, and rotate the token if exposure is suspected. <br>
Risk: Runtime Mermaid CLI installation through npx can add supply-chain and availability risk. <br>
Mitigation: Prefer preinstalling and pinning the Mermaid CLI version in the deployment environment instead of relying on runtime npx installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ParasHarnagle/mindmap-generator) <br>
- [Mermaid Mindmap Syntax](references/mermaid_mindmap_syntax.md) <br>
- [Mindmap Best Practices for AI Personal Assistants](references/mindmap_best_practices.md) <br>
- [Mermaid Mindmap Documentation](https://mermaid.js.org/syntax/mindmap.html) <br>
- [Telegram Bot API sendPhoto Endpoint](https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Mermaid mindmap syntax rendered as a PNG image with a short Telegram caption; falls back to a text tree when image rendering fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx or a preinstalled Mermaid CLI, curl, a Telegram bot token, and a target chat ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
