## Description: <br>
LME顧客にカテゴリー状況に基づいたパーソナライズメッセージを自動送信。スプレッドシート読み込み→カテゴリー分析→LME送信を完全自動化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aoaibiz](https://clawhub.ai/user/aoaibiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customer-support or marketing operators use this skill to read customer category data from a Google Sheet, generate personalized outreach messages, and send them through LME with Browser Relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer spreadsheets may contain personal or sensitive contact data. <br>
Mitigation: Use only with authorization, minimize exported fields, and avoid unnecessary sensitive or regulated notes. <br>
Risk: Browser automation can operate within the user's logged-in LME session. <br>
Mitigation: Run it only in the intended browser profile and review each generated message before sending. <br>
Risk: Bulk or poorly targeted outreach can be treated as spam or violate customer consent expectations. <br>
Mitigation: Confirm recipient consent, throttle sending, and keep message content relevant and respectful. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/aoaibiz/lme-auto-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated gws access and an active Browser Relay session for LME.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
