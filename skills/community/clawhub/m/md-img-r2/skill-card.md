## Description: <br>
Upload local images referenced in Markdown to Cloudflare R2 and replace the paths with public URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangchao228](https://clawhub.ai/user/yangchao228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to prepare Markdown articles for publication by uploading local image assets to their own Cloudflare R2 bucket and rewriting references to public URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local images referenced by processed Markdown can be uploaded and made publicly accessible through the configured public URL. <br>
Mitigation: Run with --dry-run first and process only Markdown whose local image paths are intended for publication. <br>
Risk: Cloudflare R2 credentials are required to upload files. <br>
Mitigation: Keep real R2 credentials in environment variables or a private .env file, and do not commit credentials into the skill source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangchao228/md-img-r2) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown files rewritten in place, shell status output, and JSON replacement reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates .bak backups for modified Markdown files and .replace-report.json reports for processed files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
