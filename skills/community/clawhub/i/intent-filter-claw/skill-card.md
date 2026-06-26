## Description: <br>
从授权的公域评论、帖子和消息数据中识别真实购买意向，生成带评分的高意向销售线索供销售团队跟进。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and customer operations teams use this skill to classify authorized social comments or message data for purchase intent, score leads, and prepare follow-up tables or Feishu dispatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Comment or message inputs may contain personal data or material the user is not authorized to process. <br>
Mitigation: Analyze only authorized comments or message data, minimize personal fields, and avoid private messages unless there is clear permission and a compliant workflow. <br>
Risk: Lead exports could be sent to the wrong Feishu group, user, or table. <br>
Mitigation: Confirm the Feishu destination before dispatch and review exported rows before sending. <br>


## Reference(s): <br>
- [Intent Keywords](references/intent-keywords.md) <br>
- [Semantic Rules](references/semantic-rules.md) <br>
- [User Value Model](references/user-value-model.md) <br>
- [Intent Scanner Command Reference](scripts/intent-scanner.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/intent-filter-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables or CSV-style lead lists with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scored 0-100 with a default high-intent threshold of 70; optional Feishu dispatch requires authorized destination details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
