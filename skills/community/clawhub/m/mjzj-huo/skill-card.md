## Description: <br>
帮助代理使用卖家之家跨境电商接口搜索货盘、查询账号货盘与申请记录，并提交货盘发布申请。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
跨境电商卖家、服务商和运营代理可使用该技能查询卖家之家货盘标签与货盘列表，并在授权账号下上传图片、提交货盘发布申请、查看自己的货盘和审核中申请。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an MJZJ API key to access account-specific pallet data, upload images, and submit pallet publishing applications. <br>
Mitigation: Keep MJZJ_API_KEY private, rotate it if exposed, and review prices, dates, stock, labels, descriptions, and images before allowing publish submissions. <br>
Risk: Large MJZJ snowflake identifiers can lose precision if handled as numbers. <br>
Mitigation: Treat id, labelIds, oldApplicationId, nextPosition, and similar identifier fields as strings end to end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-huo) <br>
- [MJZJ supply and demand page](https://mjzj.com/gongxu) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with API request guidance and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MJZJ_API_KEY for account-specific pallet publishing, uploads, and private account queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
