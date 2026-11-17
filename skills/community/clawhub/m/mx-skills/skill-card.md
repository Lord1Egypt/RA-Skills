## Description:

东方财富妙想提供的金融技能集合，涵盖金融数据查询、资讯搜索、智能选股、自选股管理和模拟组合管理，所有技能均需通过MX_APIKEY进行认证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial workflow users use this skill collection to install and operate Eastmoney Miaoxiang finance skills for market data, financial search, stock screening, watchlist management, and simulated portfolio tasks. The skill requires an MX_APIKEY for authenticated use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow downloads remote ZIP packages that may change over time and are not accompanied by signature or checksum verification in the artifact.

Mitigation: Use signed or checksum-verified releases when available, inspect the downloaded sub-skills before loading them, and pin reviewed artifacts for production use.

Risk: The cleanup command removes local mx-skills directories before installation.

Mitigation: Back up existing skill folders and review the deletion target before running cleanup commands.

Risk: The skill requires MX_APIKEY for authenticated use.

Mitigation: Provide MX_APIKEY only through a confidential secret-handling path and avoid exposing it in shell history, logs, or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqk000/skills/mx-skills)
- [Publisher profile](https://clawhub.ai/user/qqk000)
- [Eastmoney Miaoxiang skills API key page](https://dl.dfcfs.com/m/itc4)
- [Financial data skill package](https://marketdfs.dfcfw.com/file/download/E220260320DRQ9S9.zip)
- [Financial search skill package](https://marketdfs.dfcfw.com/file/download/E2202603204ELGGZ.zip)
- [Stock selection skill package](https://marketdfs.dfcfw.com/file/download/E1202603204ETIIS.zip)
- [Watchlist management skill package](https://marketdfs.dfcfw.com/file/download/E220260320556PGW.zip)
- [Simulated portfolio skill package](https://marketdfs.dfcfw.com/file/download/E220260320DECQBH.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY for authenticated sub-skill use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
