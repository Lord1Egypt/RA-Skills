## Description: <br>
每日综合新闻简报，自动抓取并生成包含科技、财经和热点内容的综合报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arsoooo](https://clawhub.ai/user/arsoooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and news-monitoring users use this skill to collect daily items from technology, finance, and trending-news sources, organize them into four sections, save a Markdown report, and optionally create a Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a referenced news-aggregator-skill and network-fetched news sources. <br>
Mitigation: Verify that the referenced skill and selected news sources are trusted before use. <br>
Risk: The artifact includes example HTTP and HTTPS proxy settings. <br>
Mitigation: Use only a proxy you own or trust, and replace or remove untrusted proxy values before running commands. <br>
Risk: Reports may be saved locally or optionally sent to Feishu documents. <br>
Mitigation: Require confirmation before saving reports or creating Feishu documents, and review generated content before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arsoooo/news-aggregator-skill-news-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with shell commands and optional Feishu document creation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports under reports/YYYY-MM-DD/ and can create a Feishu document after confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
