## Description: <br>
全链路新媒体运营技能，覆盖行业分析、竞品分析、账号养号、爆款内容创作和互动钩子设计，并结合 opencli、ima 知识库、联网搜索和违禁词检测支持抖音、视频号、小红书等平台的品牌账号运营。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swcxy12315](https://clawhub.ai/user/swcxy12315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, brand teams, and agents use this skill to plan and execute social-media operations workflows: industry research, competitor monitoring, account warm-up, content drafting, interaction hooks, data cleanup, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate real logged-in social-media accounts through opencli, including publish, follow, comment, download, or upload actions. <br>
Mitigation: Use a dedicated browser profile or test accounts, require manual approval for account-changing actions, and review commands before execution. <br>
Risk: The workflow may scrape, store, or import business, account, client, or customer data into local files or ima. <br>
Mitigation: Avoid confidential client data unless approved, limit collection to necessary fields, and store API keys or credentials securely. <br>
Risk: Bundled fetch-script outputs may be synthetic sample data and can produce misleading analytics if treated as live platform evidence. <br>
Mitigation: Label sample or synthetic outputs clearly and validate provenance before using reports for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/swcxy12315/newmedia-operations) <br>
- [OpenCLI Repository](https://github.com/jackwener/opencli) <br>
- [ima Agent Interface](https://ima.qq.com/agent-interface) <br>
- [OpenCLI 集成指南](artifact/references/OPENCLI.md) <br>
- [ima-skill 知识库集成指南](artifact/references/IMA_KNOWLEDGE.md) <br>
- [行业分析完整指南](artifact/references/INDUSTRY_ANALYSIS.md) <br>
- [竞品分析完整指南](artifact/references/COMPETITOR_ANALYSIS.md) <br>
- [账号养号操作手册](artifact/references/ACCOUNT_NURTURING.md) <br>
- [爆款内容创作指南](artifact/references/VIRAL_CONTENT.md) <br>
- [互动钩子设计与话术库](artifact/references/ENGAGEMENT_HOOKS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON configuration, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce social-media strategy reports, content drafts, interaction scripts, cleaned data files, and publishing or data-collection commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
