## Description: <br>
Use this skill when the user wants to report task results to Feishu/Lark after completion, with a preflight check that the reporting channel is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukp20](https://clawhub.ai/user/xukp20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to confirm a Feishu/Lark reporting channel, then send compact task completion or progress reports to that channel after work is finished. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A task report could be sent to the wrong Feishu/Lark group. <br>
Mitigation: Verify the exact group identity in the current session, send a test message, and confirm the destination before reporting. <br>
Risk: Task summaries may include sensitive, confidential, or customer data. <br>
Mitigation: Keep reports compact and exclude secrets, credentials, customer data, and confidential artifacts unless the confirmed group is appropriate. <br>
Risk: Creating a default work group could establish an unintended reporting destination. <br>
Mitigation: Ask for user identity details and explicit creation approval, then confirm the new group with a test message before use. <br>


## Reference(s): <br>
- [API Playbook (Lark MCP, Reporting Only)](references/api-playbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/xukp20/lark-work-report-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Concise text or Markdown reports sent through Feishu/Lark MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a confirmed chat_id and may split long reports into sequential messages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
