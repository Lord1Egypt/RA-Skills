## Description: <br>
沪深300多因子投研系统 v6.0 helps an agent analyze A-share and CSI 300 equities, run multi-factor and multi-strategy stock selection, and generate informational research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to run A-share and CSI 300 multi-factor research workflows, screen stocks, compare quantitative strategies, and produce informational research reports. It is intended for research support and report generation, not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded third-party JQData and Tushare credentials are present in the artifact. <br>
Mitigation: Remove embedded credentials, rotate exposed credentials, and require users to provide secrets through local configuration or environment-specific secret handling before installation. <br>
Risk: Data-source status and analysis-scope claims may be misleading, including inconsistent JQData enablement statements. <br>
Mitigation: Make data-source status truthful across documentation and scripts, and clearly state which sources are enabled, disabled, simulated, or user-configured. <br>
Risk: Some behavior can use demo or synthetic data, which could make reports look more authoritative than their inputs support. <br>
Mitigation: Label demo or synthetic-data outputs prominently and separate them from live-data reports. <br>
Risk: Generated finance reports may be mistaken for investment advice. <br>
Mitigation: Present outputs as informational research only and require human review before any trading or allocation decision. <br>
Risk: Runtime package installation can change the execution environment unexpectedly. <br>
Mitigation: Disable runtime package installation and document dependencies for explicit pre-installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/hs300-research-v6) <br>
- [README.md](artifact/README.md) <br>
- [DATA_SOURCES.md](artifact/DATA_SOURCES.md) <br>
- [Tushare Pro](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, analysis, files] <br>
**Output Format:** [Markdown reports, terminal output, JSON or Excel artifacts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local report/data files and may call external market-data services when configured.] <br>

## Skill Version(s): <br>
6.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
