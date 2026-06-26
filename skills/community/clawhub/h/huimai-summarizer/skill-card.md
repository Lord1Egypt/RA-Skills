## Description: <br>
上传长文档/文章/PDF/合同，自动生成结构化摘要、关键条款提取、执行清单。支持20+种摘要格式。安装即用，无需API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to summarize long documents, articles, PDFs, contracts, emails, meetings, and conversations into concise summaries, key takeaways, action items, comparisons, and custom formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summaries and metadata may be retained locally under ~/.openclaw/summarize-pro, including history.json and saved.json. <br>
Mitigation: Avoid using the skill for highly sensitive contracts, emails, or meeting notes unless local retention is acceptable; periodically review or delete retained local files. <br>
Risk: Document summaries can omit nuance or misstate details if source material is ambiguous, very long, or poorly structured. <br>
Mitigation: Review generated summaries, action items, dates, names, and contractual terms against the original document before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/huimai-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional shell commands and local JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist local preferences, summary history, saved summaries, and templates under ~/.openclaw/summarize-pro/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
