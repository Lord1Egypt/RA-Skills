## Description:

LibTV Skill Pro helps agents generate, edit, monitor, download, and export image and video work through the LibTV AI creation platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuxiangxiang](https://clawhub.ai/user/qiuxiangxiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route image and video creation requests to LibTV, including text-to-image, text-to-video, reference-based edits, batch jobs, polling, downloads, and report exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe network and file-write behavior in download and export helpers.

Mitigation: Review generated download and export paths before execution, and run the skill only for deliberate LibTV work from a trusted publisher.

Risk: A LibTV access key is required for live operations.

Mitigation: Keep LIBTV_ACCESS_KEY secret and avoid placing it in prompts, logs, shared shell history, or exported reports.

Risk: Direct URL downloads can fetch untrusted content and filename prefixes can affect local write paths.

Mitigation: Avoid the direct --urls download option with untrusted URLs, avoid path-like filename prefixes, and write outputs to an intended directory.

Risk: Uploaded source media and exported HTML reports may contain private or active content.

Mitigation: Upload private media only when intended, and treat exported HTML reports as untrusted files unless their source session is trusted.

## Reference(s):

- [LibTV Skill Pro on ClawHub](https://clawhub.ai/qiuxiangxiang/skills/libtv-skill-pro)
- [qiuxiangxiang publisher profile](https://clawhub.ai/user/qiuxiangxiang)
- [LibTV AI creation platform](https://www.liblib.tv)
- [Original LibTV ClawHub skill](https://clawhub.ai/haofanwang/libtv-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts return JSON and can save downloaded media files or exported Markdown, HTML, or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and LIBTV_ACCESS_KEY for live LibTV operations; dry-run mode can preview generation requests without calling the service.]

## Skill Version(s):

0.4.4 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
