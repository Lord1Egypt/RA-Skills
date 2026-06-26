## Description: <br>
Publishes Markdown or HTML articles to WeChat Official Account drafts, with local image upload, cover resizing, CDN image replacement, retry handling, and optional publish submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golikegod](https://clawhub.ai/user/golikegod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, marketers, and developers use this skill to turn local Markdown or HTML articles into WeChat Official Account drafts, including image handling, cover preparation, and optional publish/status API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes and may persist WeChat publishing credentials or access tokens in local files. <br>
Mitigation: Replace the bundled config credentials with user-controlled values, remove secrets before sharing, and avoid committing token cache or configuration files. <br>
Risk: Non-dry-run execution can upload local article content and images and create or submit posts through the configured WeChat account. <br>
Mitigation: Run dry-run previews first, review rendered content and image paths, and only execute publish actions from an isolated environment with the intended account. <br>
Risk: Dependency installation can modify the Python environment. <br>
Mitigation: Install requirements inside an isolated virtual environment before running the publisher. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/golikegod/lobster-wechat-publisher) <br>
- [Project homepage](https://github.com/victor-skills/wechat-article-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the publishing script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The publishing script can produce draft_media_id, publish_id, status, preview_html, success, title, and error fields depending on execution mode.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
