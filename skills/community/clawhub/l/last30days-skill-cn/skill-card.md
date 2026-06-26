## Description: <br>
Searches recent content across major Chinese platforms and helps an agent generate source-linked research reports. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[jesseovo](https://clawhub.ai/user/jesseovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to collect and compare recent public discussions from Chinese social, search, and media platforms, then produce cited research summaries. <br>

### Deployment Geography for Use: <br>
Global; content sources focus on Chinese platforms. <br>

## Known Risks and Mitigations: <br>
Risk: Automatic session-start execution may run a local configuration check whenever a supported agent session starts. <br>
Mitigation: Review or disable the SessionStart hook before use, especially in untrusted projects. <br>
Risk: API keys, cookies, and local environment files may be used to access platform data sources. <br>
Mitigation: Keep .env files private, use least-privilege credentials, and avoid high-privilege personal session cookies. <br>
Risk: Crawler-style behavior can contact multiple external platforms and save research reports locally. <br>
Mitigation: Install only where this behavior is expected and review generated local files before sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jesseovo/last30days-skill-cn) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jesseovo) <br>
- [Original last30days skill reference](https://github.com/mvanhorn/last30days-skill) <br>
- [MediaCrawler reference](https://github.com/NanmiCoder/MediaCrawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Compact terminal summaries, Markdown reports, JSON, context snippets, and local report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can emit compact, json, md, context, or path output and can write report.md, report.json, and last30days.context.md.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
