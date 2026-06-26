## Description: <br>
HS300 Research V5 helps agents run multi-factor A-share and CSI 300 research workflows, collect market data from several sources, score stocks, assess risk, and produce investment research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to analyze A-share and CSI 300 equities, run multi-factor scoring, inspect technical and fundamental signals, and generate research reports for review. The generated research should be treated as decision support, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes live third-party credentials and enabled credentialed data access. <br>
Mitigation: Rotate or remove bundled credentials, replace them with environment-managed credentials, and disable unwanted external data sources before installation. <br>
Risk: The skill can send market queries to external data providers and create local caches, logs, reports, and downloaded files. <br>
Mitigation: Review provider terms and local data-handling requirements, and run it only in environments where those queries and artifacts are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/hs300-research-v5) <br>
- [README.md](artifact/README.md) <br>
- [DATA_SOURCES.md](artifact/DATA_SOURCES.md) <br>
- [Tushare Pro](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown research reports, Excel workbooks, CSV factor data, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use live third-party market data sources and local caches; generated research is not investment advice.] <br>

## Skill Version(s): <br>
5.2.1 (source: server release evidence; artifact frontmatter lists 5.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
