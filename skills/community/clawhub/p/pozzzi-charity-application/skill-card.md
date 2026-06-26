## Description: <br>
噗滋（pozzzi）慈善 - 帮助中小型 NGO 自动生成项目申报书草稿，支持腾讯公益99公益日、通用基金会申请和政府购买服务三种格式，内置占位符强制机制防止 AI 编造预算和编号数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External NGO staff and grant writers use this skill to draft Chinese charity project application materials for general foundation applications, Tencent 99 Giving Day, and government service-purchase submissions. It structures user-provided project, budget, team, timeline, and impact details into review-ready Markdown drafts. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Application and budget details may be sent to the configured model provider. <br>
Mitigation: Confirm the model provider and data handling terms before use, and avoid entering information that should not be processed by that provider. <br>
Risk: Limited local history may be retained through the configured storage adapter. <br>
Mitigation: Confirm the storage adapter and retention policy before installation, and review stored history according to the deploying organization's privacy requirements. <br>
Risk: Generated application drafts may contain legal, financial, submission, or factual errors. <br>
Mitigation: Treat output as a draft, manually fill placeholders, and have qualified staff review all budgets, identifiers, compliance statements, and submission details before filing. <br>


## Reference(s): <br>
- [Tencent Charity](https://gongyi.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/pozzzi-charity-application) <br>
- [Publisher profile](https://clawhub.ai/user/aikawabigsky309) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown application draft with warnings and generation metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full application drafts and single-section regeneration; outputs include AI disclosure text and placeholder replacement metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
