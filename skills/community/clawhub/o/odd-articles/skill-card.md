## Description: <br>
odd-articles helps agents turn collected notes or WeChat article links into drafted articles, styled HTML, covers, platform copy, and publishing actions across supported Chinese content platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyhwei](https://clawhub.ai/user/jackyhwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to collect article material, draft and format posts, generate visual assets, convert content for multiple platforms, and publish or archive outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic publishing and stored credentials can expose accounts or publish content before review. <br>
Mitigation: Use preview or dry-run modes first, review generated content and manifests, and add real publishing credentials only after the workflow is understood. <br>
Risk: Unsafe credential handling or exposed keys can compromise connected services. <br>
Mitigation: Rotate any exposed API key that belongs to the installer, keep secrets in local environment configuration, and avoid committing credential files. <br>
Risk: Background-style material capture can record sensitive conversation details. <br>
Mitigation: Avoid using the skill on sensitive conversations and review or clear collected material before generating drafts. <br>
Risk: TLS bypass and AI-detection evasion guidance are not appropriate for production use. <br>
Mitigation: Remove or change those behaviors before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyhwei/odd-articles) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Writing guide](references/writing-guide.md) <br>
- [WeChat to chartlet workflow](references/wechat_to_chartlet.md) <br>
- [CNBlogs publishing guide](references/publishing_to_cnblogs.md) <br>
- [Archive outputs guide](references/archive_outputs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML, JSON manifests, platform copy, and executable Python or TypeScript command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local draft, preview, cover, carousel, archive, and manifest files; publishing flows can call external platform APIs or browser automation when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
