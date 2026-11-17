## Description:

Publishes a single self-contained HTML page to htmlcode.fun for fast sharing as a live URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520xiaomumu](https://clawhub.ai/user/520xiaomumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish or update self-contained HTML pages when they need a fast live link for demos, reports, landing pages, QR share pages, or generated frontends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML sent to htmlcode.fun may become publicly accessible.

Mitigation: Deploy only content intended for public sharing, and remove private data, secrets, or local-only material before publishing.

Risk: Version-management commands can change, unpublish, overwrite, or delete hosted content.

Mitigation: Inspect version history before changes, avoid liked versions, and require clear user intent before deletion or status changes.

Risk: Fetching deployed source with an output path can write content to the local workspace.

Mitigation: Use an intentional output path and review existing files before saving fetched HTML.

## Reference(s):

- [htmlcode.fun live guide](https://www.htmlcode.fun/s/htmlcode-fun-guide)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment responses can include live URLs, detail URLs, version URLs, QR codes, version numbers, and preservation hints.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
