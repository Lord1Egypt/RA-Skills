## Description:

List recently uploaded images on PixelVault with their CDN URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facundofarias](https://clawhub.ai/user/facundofarias)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent retrieve recently uploaded PixelVault images and report their CDN URLs or JSON metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON output can expose filenames, folders, sizes, timestamps, pagination metadata, and image URLs from the configured PixelVault account.

Mitigation: Use the default URL-only output unless full metadata is needed, and review JSON results before sharing them outside the intended context.

## Reference(s):

- [Pixelvault List release page](https://clawhub.ai/facundofarias/skills/pixelvault-list)
- [facundofarias publisher profile](https://clawhub.ai/user/facundofarias)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and returned PixelVault URLs or JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is one CDN URL per line; --json may include id, URL, MIME type, size, filename, folder, timestamps, and pagination metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
