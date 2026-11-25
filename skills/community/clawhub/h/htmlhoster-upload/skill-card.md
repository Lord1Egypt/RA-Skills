## Description:

Publish HTML pages, images, PDFs, ZIP (unzip hosting) and Markdown documents to htmlhoster.com and get back a public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethandavis0411](https://clawhub.ai/user/ethandavis0411)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to publish generated HTML, images, PDFs, ZIP archives, and Markdown as shareable public pages. It returns public URLs and a token for deleting an upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the release suspicious with medium confidence because protection for ZIP uploads is incompletely documented.

Mitigation: Treat uploaded content as public and avoid ZIPs that may contain secrets or personal information; inspect the files before uploading.

Risk: The included delete token can remove its associated upload.

Mitigation: Keep the delete token private and share only the public page URL.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/ethandavis0411/htmlhoster-upload)
- [htmlhoster Agent documentation](https://htmlhoster.com/agent/)
- [ClawHub skill release](https://clawhub.ai/ethandavis0411/skills/htmlhoster-upload)

## Skill Output:

**Output Type(s):** [JSON, URLs, Guidance]

**Output Format:** [JSON response containing a public entry URL, per-file URLs, and a delete token, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The public URLs can be shared; keep the delete token private.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
