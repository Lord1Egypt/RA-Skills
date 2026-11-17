## Description:

Converts Markdown into WeChat-compatible HTML and can help create WeChat or Juejin drafts with configurable article and news styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysdhb](https://clawhub.ai/user/ysdhb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to convert Markdown articles or news digests into WeChat-ready HTML, then optionally prepare drafts for WeChat Official Accounts or Juejin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WeChat and Juejin publishing credentials.

Mitigation: Install only when credentialed publishing is acceptable, store the local config file with restrictive permissions, and avoid using it with private or proprietary content unless publishing is intended.

Risk: Generated drafts may include hard-coded author or promotional footer content.

Mitigation: Review generated HTML and draft metadata before publishing, and remove or override default ending_lines and hard-coded author behavior where inappropriate.

Risk: The ClawHub security verdict is suspicious.

Mitigation: Treat draft publishing actions as sensitive, review outputs before submission, and limit use to trusted Markdown files and images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysdhb/skills/mukun-md-push-wechat)
- [README](README.md)
- [WeChat credential configuration guide](how_to_config_wechat.md)
- [Default article style preset](references/article_default.yaml)
- [Modern article style preset](references/article_modern.yaml)
- [News and article configuration example](examples/config_example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are HTML files and publishing draft metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python scripts and external publishing APIs when the user requests draft creation.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
