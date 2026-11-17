## Description:

卖家之家(跨境电商)问答搜索

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search 卖家之家 Q&A categories and questions, post new questions, and retrieve the user's own posted questions through the documented service endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger rules may route generic question-search or posting requests to 卖家之家.

Mitigation: Confirm the user's intent before posting questions or using bounty and watch payment fields.

Risk: Token-backed endpoints can access the user's account data or create questions with MJZJ_API_KEY.

Mitigation: Install only when the agent is intended to access 卖家之家, keep MJZJ_API_KEY scoped to that purpose, and review token use before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-ask)
- [ClawHub publisher profile](https://clawhub.ai/user/mjzj-tec)
- [卖家之家问答](https://mjzj.com/ask)
- [卖家之家智能体 API KEY](https://mjzj.com/user/agentapikey)
- [卖家之家发布问题](https://mjzj.com/ask/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require MJZJ_API_KEY for token-backed account lookup and question posting.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
