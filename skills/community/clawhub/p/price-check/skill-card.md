## Description: <br>
Searches major Chinese ecommerce platforms for current prices, filters noisy or mismatched listings, recommends whether to buy, and records local price history for later comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuxiaoyang2007-prog](https://clawhub.ai/user/yuxiaoyang2007-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to compare product prices across Taobao/Tmall, JD, PDD, Suning, Vipshop, Kaola, Douyin, Kuaishou, and 1688, then receive a buy, wait, or insufficient-data recommendation. It also supports local SQLite price history and optional Feishu Bitable sync for users who want cross-device tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub price-check skill page](https://clawhub.ai/yuxiaoyang2007-prog/price-check) <br>
- [Report template](references/report-template.md) <br>
- [Configuration example](config.example.json) <br>
- [shopmind-price-compare source acknowledgement](https://clawhub.ai/skills/shopmind-price-compare) <br>
- [Upstream author profile](https://clawhub.ai/users/xiaohaook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the CLI plus a human-facing Markdown shopping report rendered by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes product verdicts, filtered candidate listings, search links, local SQLite history summaries, and optional Feishu sync records; product search terms are sent to the maishou88.com price API.] <br>

## Skill Version(s): <br>
0.6.4 (source: server release evidence and CHANGELOG, released 2026-04-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
