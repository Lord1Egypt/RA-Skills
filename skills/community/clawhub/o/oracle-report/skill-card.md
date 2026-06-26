## Description: <br>
生成 A 股收盘日报，汇总大盘指数、情绪资金和全球市场数据，并可发送飞书卡片和保存 Markdown 归档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icemanzb](https://clawhub.ai/user/icemanzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
投资研究或市场运营人员可用该 skill 在交易日收盘后生成 A 股市场日报，汇总指数、资金情绪、估值和全球市场指标。输出可用于飞书发送、Markdown 归档或人工复核。 <br>

### Deployment Geography for Use: <br>
Global; the report content is focused on China A-share market data. <br>

## Known Risks and Mitigations: <br>
Risk: Embedded API credentials may expose private service access or be misused. <br>
Mitigation: Remove embedded keys, rotate any keys that belong to you, and load required credentials from environment variables or a managed secret store before running. <br>
Risk: The Feishu delivery target defaults to a specific user ID when FEISHU_TARGET is not set. <br>
Mitigation: Set FEISHU_TARGET explicitly to the intended user or chat and verify the destination before enabling delivery. <br>
Risk: The skill depends on qveris, mx_data, and multiple external market-data sources whose behavior and access controls are outside this artifact. <br>
Mitigation: Install and review qveris and mx_data separately, confirm their permissions, and validate report data before relying on it. <br>
Risk: The documented cron schedule can send reports automatically every weekday. <br>
Mitigation: Add the cron entry only when recurring report generation and Feishu delivery are intentional, and monitor logs for failures or unexpected sends. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/icemanzb/oracle-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report, Feishu card payload, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated Markdown archive under /root/.openclaw/workspace/ and can send a Feishu card to FEISHU_TARGET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
