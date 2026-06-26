## Description: <br>
Naver Datalab Cli helps agents run NAVER DataLab search-keyword and shopping-insight trend queries for Korean market research, content planning, campaign timing, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market-research agents use this skill to query Korean NAVER DataLab trend signals, compare keyword or category interest over time, and produce JSONL data for downstream reporting or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend query inputs and NAVER API credentials are sent to NAVER DataLab. <br>
Mitigation: Use only intended keywords, categories, dates, and filters; keep NAVER_CLIENT_ID and NAVER_CLIENT_SECRET private and out of committed files. <br>
Risk: The API base URL can be changed with NAVER_DATALAB_BASE, which could redirect credentials and query data away from the official endpoint. <br>
Mitigation: Leave NAVER_DATALAB_BASE unset or verify it points to https://openapi.naver.com/v1/datalab before using real credentials. <br>
Risk: NAVER DataLab returns normalized relative ratios, which can be mistaken for absolute search or shopping volume. <br>
Mitigation: Present outputs as relative trend indices and avoid claims about raw demand volume unless supported by another data source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/naver-datalab-cli) <br>
- [NAVER Developers application registration](https://developers.naver.com/apps/#/register) <br>
- [NAVER Shopping Insight category reference](https://datalab.naver.com/shoppingInsight/sCategory.naver) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [JSONL trend records from shell commands, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, and NAVER DataLab credentials; results are relative trend ratios rather than absolute counts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
