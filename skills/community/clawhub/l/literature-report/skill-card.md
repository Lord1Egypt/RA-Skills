## Description:

Automates literature reports by retrieving recent papers from RSS and PubMed sources, using an LLM to filter and summarize them bilingually, and optionally preparing notifications for Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuzhiyucai](https://clawhub.ai/user/zjuzhiyucai)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and technical teams use this skill to monitor recent papers in configured research areas, filter them with LLM assistance, and generate concise bilingual literature updates. It can be run manually or scheduled for recurring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper titles, abstracts, and research-focus text may be sent to the configured LLM provider.

Mitigation: Use only a trusted HTTPS base_url, avoid submitting sensitive unpublished material, and choose an LLM provider acceptable for the intended data.

Risk: The local config.yaml may contain an LLM API key and optional Feishu user identifier.

Mitigation: Keep config.yaml out of source control, restrict file access, and prefer limited-spend or scoped API credentials.

Risk: Scheduled execution can repeatedly trigger network requests and LLM usage.

Mitigation: Review cron entries before enabling daily runs, validate the configuration first, and monitor provider costs or rate limits.

Risk: Installation adds Python dependencies to the active environment.

Mitigation: Install in a virtual environment and review dependency installation before running install.sh.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjuzhiyucai/skills/literature-report)
- [README.md](README.md)
- [GUIDE.md](GUIDE.md)
- [OpenAI Platform](https://platform.openai.com)
- [Anthropic Console](https://console.anthropic.com)
- [SiliconFlow Cloud](https://cloud.siliconflow.cn)
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [Nature RSS](https://www.nature.com/nature.rss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets; generated reports are saved as text or JSON and can optionally be converted to PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a configured LLM API key, and optional Feishu target; scheduled runs may create recurring API usage.]

## Skill Version(s):

1.0.4 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
