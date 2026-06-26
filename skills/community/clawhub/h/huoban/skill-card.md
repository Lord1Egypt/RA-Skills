## Description: <br>
Huoban is a low-code platform assistant for multidimensional table design, automation workflows, analytics dashboards, permissions, and API integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and operations teams use this skill to design Huoban data tables, configure automations, build dashboards, manage permissions, and plan Huoban API or webhook integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API examples can expose or mishandle Huoban API tokens if users paste secrets into prompts, code, or shared files. <br>
Mitigation: Keep API tokens out of code and prompts, store them in secret managers or environment variables, and use scoped tokens where possible. <br>
Risk: Update and delete API operations can modify or remove business records. <br>
Mitigation: Require explicit confirmation before running update or delete operations and test requests against non-production data first. <br>
Risk: Webhook integrations can send business data to untrusted or incorrect endpoints. <br>
Mitigation: Verify webhook URLs, use HTTPS endpoints, and limit payload contents to the minimum data required. <br>


## Reference(s): <br>
- [Huoban API endpoint](https://api.huoban.com/v2) <br>
- [ClawHub skill page](https://clawhub.ai/zhangifonly/huoban) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown with tables and inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python API examples, webhook patterns, formulas, table schemas, and workflow configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
