## Description: <br>
Collects direct-message ideas prefixed with `idea:` or `灵感：`, stores them in Feishu/Lark Bitable, and uses a configured model provider to summarize, categorize, tag, and digest new entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiaolin](https://clawhub.ai/user/hanxiaolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users use this skill to capture private-chat ideas into a structured Feishu/Lark Bitable inbox, classify them with an LLM or rules fallback, and receive a daily digest when new ideas were added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private-message idea text is stored in Feishu/Lark Bitable and may be sent to the configured model provider. <br>
Mitigation: Use only with approved Feishu/Lark workspaces and model providers, and avoid sending secrets, regulated data, or confidential business plans unless those services are approved for that data. <br>
Risk: The skill persists local configuration for the created Bitable and model setup. <br>
Mitigation: Delete `~/.openclaw/idea-inbox/config.json` and the created Bitable when the skill is no longer in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiaolin/idea-inbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Bitable records, JSON classification fields, and daily digest text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes content, AI summary, category, tags, status, source, and created time fields; returns a record ID or an error reason.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
