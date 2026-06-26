## Description: <br>
橙子通（orange-office.cn）库存管理系统 API 自动化，用于通过 API 创建出库单、查询库存、管理主播仓库等，无需浏览器。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiao1230123](https://clawhub.ai/user/xiao1230123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Orange Office inventory workflows, including stock-out creation, stock queries, warehouse mapping, and DingTalk inventory table updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter Orange Office inventory records and related DingTalk inventory tables using a live session cookie. <br>
Mitigation: Use a least-privileged account, keep the session cookie out of chat logs and transcripts, and require explicit human confirmation before create, update, delete, or table-write actions. <br>
Risk: Incorrect inventory inputs or stale session context could create inaccurate business records. <br>
Mitigation: Confirm current stock through the API before writes and review generated request bodies before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiao1230123/orange-office-api) <br>
- [Orange Office API site](https://orange-office.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with API examples and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes request signing, session-cookie handling, warehouse identifiers, DingTalk table identifiers, and inventory operation rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw.skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
