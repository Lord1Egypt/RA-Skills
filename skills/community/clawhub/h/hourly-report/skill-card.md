## Description: <br>
Creates hourly Douyin livestream performance reports and sends them to DingTalk using either Douyin Open Platform APIs or webpage crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangfan158](https://clawhub.ai/user/yangfan158) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use this skill to set up automated hourly and end-of-day Douyin livestream reports for a DingTalk group. It supports API mode with Douyin Open Platform credentials and crawl mode with a live room URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction API failures can lead to fabricated order, GMV, and conversion metrics being sent as live business reports. <br>
Mitigation: Use API mode only after changing the code to fail closed or clearly mark missing transaction data instead of substituting simulated values. <br>
Risk: Crawl mode uses simulated transaction metrics and should not be treated as an operational or financial data source. <br>
Mitigation: Use crawl mode only for temporary testing or non-financial reporting, and label its transaction values as simulated in downstream use. <br>
Risk: Client secrets and DingTalk webhooks passed as shell arguments may be exposed through shell history or process listings. <br>
Mitigation: Provide credentials through environment variables or a protected configuration file and rotate any secret that may have been exposed. <br>


## Reference(s): <br>
- [Douyin Open Platform](https://open.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates DingTalk-ready hourly and daily livestream report text; requires Douyin credentials or a live URL plus a DingTalk webhook.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
