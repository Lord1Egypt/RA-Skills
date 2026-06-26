## Description: <br>
抓取用户可访问的微信公众号文章，将正文保存为 Markdown，并保留渲染后的 HTML 快照。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhedev](https://clawhub.ai/user/liuhedev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and content archivists use this skill to convert WeChat public-account articles they can access into local Markdown, HTML snapshots, and optional image files for personal archiving, offline reading, or authorized content reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional image downloading may send Referer headers and domain-matching browser cookies while fetching article images. <br>
Mitigation: Use a dedicated low-privilege browser profile or session, enable image downloading only when needed, and avoid using accounts or profiles with broader access than the article requires. <br>
Risk: Generated Markdown, HTML snapshots, and local images may contain login-gated or copyrighted article content. <br>
Mitigation: Store outputs privately unless redistribution is authorized, and confirm that saved content complies with the publisher's rights and applicable platform terms. <br>
Risk: WeChat page structure changes or lazy-loaded content can lead to incomplete or imperfect extraction. <br>
Mitigation: Use headed wait mode for pages that require login or manual loading, then review the captured HTML snapshot and generated Markdown before relying on the archive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuhedev/lh-wechat-to-markdown) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, html, files, shell commands, guidance] <br>
**Output Format:** [Markdown files with YAML front matter, rendered HTML snapshots, optional local image files, and terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When image downloading is enabled, image links may be rewritten to local relative paths under an images directory; failed image downloads keep their original URLs.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
