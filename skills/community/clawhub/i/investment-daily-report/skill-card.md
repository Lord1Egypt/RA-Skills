## Description: <br>
Generates structured daily investment research reports for A-share, Hong Kong, and U.S. markets by collecting market data, fund flows, sector rotation, announcements, and technical signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolfzb](https://clawhub.ai/user/coolfzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment teams use this skill to run a Node.js report generator that summarizes daily public-market activity into an archiveable Markdown report. It is intended for market review and research support, not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator contacts NeoData through a local gateway and depends on external market data availability. <br>
Mitigation: Run it only where localhost gateway access is expected, and review failed or partial query sections before sharing the report. <br>
Risk: The script writes to the selected report path and can replace content at that path. <br>
Mitigation: Choose output paths intentionally and keep backups for existing reports. <br>
Risk: Portfolio-linked information may be sensitive if future Trade Arena account tracking is enabled. <br>
Mitigation: Do not provide private portfolio data unless a future release clearly documents how account-linked data is handled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolfzb/investment-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/coolfzb) <br>
- [NeoData gateway endpoint](https://jprx.m.qq.com/aizone/skillserver/v1/proxy/teamrouter_neodata/query) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report file with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes investment-report-YYYY-MM-DD.md by default; supports market selection, quick mode, and custom output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact changelog and script mention v1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
