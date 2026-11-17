## Description:

Convert Markdown (inline text or a `.md` file path) into a single PNG image using local code (Markdown -> HTML -> headless browser screenshot). Use when the user asks for a PNG image output from Markdown content or a `.md` file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520mianxiangduixiang520](https://clawhub.ai/user/520mianxiangduixiang520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content authors, and agents use this skill to convert inline Markdown or `.md` files into a single PNG image for sharing, previews, or documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown image references can fetch remote URLs or read local image paths during rendering.

Mitigation: Run only with trusted Markdown in a contained environment, prefer `--no-inline-images` for untrusted inputs, and avoid documents with external URLs or local absolute image paths.

Risk: The skill renders content in an unsandboxed headless browser.

Mitigation: Use a disposable virtualenv or container with restricted filesystem and network access before rendering untrusted documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/520mianxiangduixiang520/skills/md2img)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG file plus Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single full-page PNG screenshot; rendering width can be adjusted with `--image-width`.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
