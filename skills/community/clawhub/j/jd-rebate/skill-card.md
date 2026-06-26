## Description: <br>
京东返利 helps users handle rebate authorization and tutorials, convert supported product links into rebate links, search for rebate-eligible products, check balances, and confirm withdrawals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfile](https://clawhub.ai/user/skyfile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers use this skill to find rebate-eligible products, turn supported Taobao, JD, and Pinduoduo product links into rebate links, and manage account balance or withdrawal flows after WeChat authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links WeChat/openId identity and local authorization state to rebate activity. <br>
Mitigation: Install only if you trust the rebate backend and intentionally complete the authorization flow. <br>
Risk: Product queries and product links can be sent to rebate services and to the configured LLM provider for intent recognition. <br>
Mitigation: Avoid submitting sensitive text and use only trusted model-provider configuration. <br>
Risk: A withdrawal can be submitted after the user prepares an amount and confirms with the expected confirmation phrase. <br>
Mitigation: Review the amount and account state before confirming withdrawal requests. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/skyfile/jd-rebate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown user-facing responses with supporting JSON and shell-command execution paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes user messages through authorization/tutorial, link rebate, and product-search flows; script stdout is intended to be returned verbatim.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
