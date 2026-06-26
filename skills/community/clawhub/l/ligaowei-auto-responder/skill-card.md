## Description: <br>
飞书自动回复助手，定时扫描用户的私聊消息，发现业务咨询问题后自动回复对方。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal employees use this skill to automate replies to Feishu private messages about merchant issues, rates, settlement, refunds, transactions, and related business-process questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously read workplace private messages and send automated replies. <br>
Mitigation: Install only with explicit approval from the Feishu account owner and organization; use dry-run or approval-before-send where possible. <br>
Risk: Keyword-based replies may send incomplete or inappropriate business guidance. <br>
Mitigation: Review and limit allowed keywords, chats, and reply templates before enabling automated sending. <br>
Risk: The skill may retain chat metadata in local cache or memory logs. <br>
Mitigation: Define retention and deletion rules for local cache and memory logs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/ligaowei-auto-responder) <br>
- [Publisher profile](https://clawhub.ai/user/runkecheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON actions and plain-text Feishu reply templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit reply, pass, or error actions; replies are selected by keyword-matched topics and local configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
