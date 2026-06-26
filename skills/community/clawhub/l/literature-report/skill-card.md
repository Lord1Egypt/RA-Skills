## Description: <br>
Automates literature monitoring by retrieving recent journal and PubMed papers, using an LLM to filter and summarize them, and preparing bilingual reports for Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZJUZhiyuCai](https://clawhub.ai/user/ZJUZhiyuCai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers and developers use this skill to monitor selected research areas, collect recent papers from configured sources, generate bilingual summaries and key findings, and schedule recurring literature reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an LLM API key locally and sends paper metadata plus the configured research topic to the selected LLM provider. <br>
Mitigation: Use a virtual environment, keep config.yaml out of source control, verify base_url before running, and avoid sensitive unpublished topics unless the provider is approved. <br>
Risk: Feishu delivery is documented as incomplete and currently prints messages rather than sending a real notification. <br>
Mitigation: Treat Feishu support as a placeholder, verify delivery behavior before relying on scheduled reports, and review generated reports locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZJUZhiyuCai/literature-report) <br>
- [Publisher profile](https://clawhub.ai/user/ZJUZhiyuCai) <br>
- [OpenAI platform](https://platform.openai.com) <br>
- [Anthropic console](https://console.anthropic.com) <br>
- [SiliconFlow cloud](https://cloud.siliconflow.cn) <br>
- [PubMed paper links](https://pubmed.ncbi.nlm.nih.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the included scripts are run, they can create local JSON, text, and PDF report files.] <br>

## Skill Version(s): <br>
1.0.4 (source: package.json, artifact documentation, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
