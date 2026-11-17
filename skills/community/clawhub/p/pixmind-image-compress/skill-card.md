## Description:

Cloud-powered image compression and resize: compress JPG/PNG/WebP/HEIC to WebP/AVIF, resize images, and batch process folders using Pixmind API and Tencent Cloud COS imageMogr2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to compress, resize, and convert individual images or image folders for web, social, email, thumbnail, and archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to Pixmind/Tencent-backed cloud processing.

Mitigation: Use the skill only for images that are appropriate to send to the cloud service, and confirm the input set before compression.

Risk: Recursive batch mode can include more local files than intended, especially from untrusted archives or shared folders.

Mitigation: Avoid recursive batch mode on untrusted folders and review the files to be processed before running the command.

Risk: Remote image download handling can access network locations beyond the original input.

Mitigation: Prefer trusted image URLs and review generated outputs before using or distributing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuyunzhishang/skills/pixmind-image-compress)
- [Pixmind](https://www.pixmind.io)
- [Tencent Cloud COS imageMogr2](https://cloud.tencent.com/document/product/460/36540)
- [Pixmind API Platform Keys](https://www.pixmind.io/api-platform/dashboard/keys)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands; compressed image files are written to the configured output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PIXMIND_API_KEY. Local image inputs may be uploaded to Pixmind/Tencent-backed cloud processing.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
