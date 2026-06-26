## Description: <br>
Generates automated daily and weekly research paper reports by searching arXiv, using an LLM to select and summarize relevant papers, and publishing the results to Feishu Wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leogoat2004](https://clawhub.ai/user/leogoat2004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to monitor a configured research direction, filter recent arXiv papers, generate concise Chinese-language research digests, and publish the results into a Feishu Wiki space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app credentials and can create remote Wiki documents automatically. <br>
Mitigation: Confirm the target Feishu space and parent node before running, keep credentials out of logs and shared prompts, and require manual approval before scheduled or agent-triggered publication. <br>
Risk: The Feishu document creation script prints a tenant access token prefix during execution. <br>
Mitigation: Remove token-prefix logging before use and avoid sharing execution logs that may expose credential material. <br>
Risk: Generated reports are based on arXiv abstracts and LLM scoring, so relevance and summaries may be incomplete or misleading. <br>
Mitigation: Review selected papers and generated summaries before publishing reports to a shared workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leogoat2004/paper-lark-report) <br>
- [Publisher profile](https://clawhub.ai/user/leogoat2004) <br>
- [arXiv API](https://export.arxiv.org/api/query) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Daily report template](artifact/templates/daily_report.md) <br>
- [Weekly report template](artifact/templates/weekly_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown report templates, JSON paper selection files, CLI commands, and Feishu Wiki document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local data files and can publish documents to the configured Feishu Wiki space.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
