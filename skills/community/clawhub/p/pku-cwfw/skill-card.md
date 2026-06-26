## Description: <br>
北京大学财务综合信息门户 (cwfw.pku.edu.cn / WF_CWBS) CLI 工具。当用户提及 cwfw、财务门户、财务综合信息门户、个人酬金、工资查询、报销查询 时使用此 skill。Also use when dealing with cwfw IAAA 登录 (app_id=IIPF)、home2.jsp→findpages_postData.action→home3.jsp 多步 bootstrap、WF_CWBS 子系统入口、或 cwfw 的加密表单字段。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a CLI client for PKU's financial information portal, including login, session status, logout, and personal payment, salary, or reimbursement queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to log in to a PKU financial portal and access sensitive salary, remuneration, or reimbursement records. <br>
Mitigation: Require explicit user approval before login and before each financial query, and avoid copying query results into logs or shared chat unless the user requests it. <br>
Risk: The skill describes persistent session storage for the local CLI. <br>
Mitigation: Run logout or remove the persisted session after the task is complete, especially on shared or long-lived environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-cwfw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve sensitive PKU financial portal sessions and query results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
