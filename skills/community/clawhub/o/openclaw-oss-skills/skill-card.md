## Description:

Upload generated artifacts from an OpenClaw workspace to an Alibaba Cloud OSS bucket using credentials from environment variables, then return a temporary signed download link in the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenghuanluck](https://clawhub.ai/user/zhenghuanluck)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to upload generated files, directories, archives, reports, images, documents, videos, or build outputs to Alibaba Cloud OSS and return temporary signed download links to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local artifacts to a configured Alibaba Cloud OSS bucket and return signed download links.

Mitigation: Confirm exact upload paths before execution, avoid sensitive directories, and use narrowly scoped OSS credentials.

Risk: Directory or batch uploads are archived before upload and may include unintended files, especially because directory uploads may follow symlinks.

Mitigation: Review directory contents before upload, prefer explicit file paths for sensitive workspaces, and inspect generated archives when handling confidential material.

Risk: Temporary ZIP copies may be left behind after directory or multi-file uploads.

Mitigation: Clean temporary artifact archives after use and avoid placing secrets in generated upload bundles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenghuanluck/skills/openclaw-oss-skills)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown link with upload metadata; JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns object_key, download_url, expires_at, and source for uploaded artifacts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
