## Description: <br>
Call PartnerBoost merchant APIs to manage transactions, performance, billing, partners and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[partnerboost-tech-team](https://clawhub.ai/user/partnerboost-tech-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchant operators and developers use this skill to have an agent prepare authenticated PartnerBoost API requests for transaction, performance, billing, account, and partner data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PartnerBoost merchant API key and can access sensitive account, billing, transaction, and partner records. <br>
Mitigation: Use a least-privilege API key where available, provide it only through the agent runtime environment, and avoid exposing keys or raw merchant records in chats or logs. <br>
Risk: Agent-requested API queries may retrieve sensitive merchant data. <br>
Mitigation: Confirm intent before retrieving account, billing, transaction, or partner records, and limit query ranges and filters to the business need. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/partnerboost-tech-team/partnerboost-brand) <br>
- [PartnerBoost API base URL](https://app.partnerboost.com) <br>
- [OpenClaw Skills configuration](https://docs.openclaw.ai/tools/skills-config) <br>
- [QClaw](https://qclaw.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash curl examples and JSON API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARTNERBOOST_API_KEY in the agent runtime environment.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
