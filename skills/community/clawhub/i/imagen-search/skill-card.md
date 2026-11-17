## Description:

Search Imagen Chat for relevant existing images, deliver watermarked links or downloads, and optionally unlock originals with an API key and credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-cn](https://clawhub.ai/user/liu-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and developers use this skill to find existing images for articles, produce numbered Markdown references, and optionally download originals using authorized Imagen credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Imagen.

Mitigation: Send only generic terms needed for the search, not private article or project context.

Risk: Paid original downloads consume credits, and temporary original links can be accessed by anyone who holds them.

Mitigation: Set an explicit total credit budget and share temporary links only with intended recipients.

Risk: Optional catalog suggestions send the approved email and request to Imagen; removing a saved local key does not revoke it remotely.

Mitigation: Submit suggestions only with explicit approval, and revoke unwanted keys in the Imagen account.

## Reference(s):

- [Imagen Search skill documentation](https://imagen.chat/skills/imagen-search)
- [Imagen Search installation and update guide](https://imagen.chat/install/imagen-search.md)

## Skill Output:

**Output Type(s):** [Markdown, Image URLs, Files, Guidance]

**Output Format:** [Numbered Markdown image references with source links and optional downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search candidates are metadata-based until visually reviewed; watermarks and asset usage conditions must be preserved.]

## Skill Version(s):

1.1.2 (source: frontmatter, release.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
