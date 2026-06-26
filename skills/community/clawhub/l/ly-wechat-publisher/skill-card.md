## Description: <br>
Automatically prepares AI news content as HTML and creates WeChat Official Account draft posts using configured account credentials, templates, and scheduling settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to generate AI-news draft articles and place them in a WeChat Official Account draft box for review before public posting. It is suited for scheduled newsletter-style publishing workflows that still require credential handling and editorial review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat AppID/AppSecret credentials and may cache access tokens locally. <br>
Mitigation: Use a test WeChat account first, prefer environment variables or a secret store for AppSecret, and restrict permissions on configuration and token-cache files. <br>
Risk: Command-line or configuration-file credential entry can expose secrets through shell history, local files, or screenshots. <br>
Mitigation: Avoid command-line AppSecret entry and review stored configuration before running in a shared environment. <br>
Risk: Scheduled publishing workflows can create public-facing drafts before the operator has reviewed content quality or accuracy. <br>
Mitigation: Disable scheduling until the generated drafts are trusted and inspect each draft in WeChat before public posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/403914291/ly-wechat-publisher) <br>
- [User guide](artifact/docs/user_guide.md) <br>
- [Changelog](artifact/changelog.md) <br>
- [Publisher profile](https://clawhub.ai/user/403914291) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and generated WeChat draft content submitted through API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local status, log, usage, token-cache, and result files during execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
