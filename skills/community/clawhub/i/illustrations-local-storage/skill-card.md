## Description:

Localize HTTP(S) images in SoMark Markdown into ZIP-like directory packages for one Markdown file or a batch of .md/.markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to preserve SoMark-exported Markdown documents by downloading remote image assets, rewriting image references to local paths, and packaging each document with its images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown can cause the downloader to fetch arbitrary HTTP(S) image URLs, which may be inappropriate on sensitive networks.

Mitigation: Process trusted Markdown where possible, use --allowed-host for known SoMark or object-storage domains, or run the skill in a network-restricted environment.

Risk: The skill depends on Pillow to validate, decode, and convert downloaded images.

Mitigation: Install Pillow in a virtual environment and keep dependency installation scoped to the conversion task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soul-code/skills/illustrations-local-storage)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated packages contain main.md and JPEG images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads remote HTTP(S) images, rewrites references to ./images/image_NNN.jpg, and can process one file or a recursive batch.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
