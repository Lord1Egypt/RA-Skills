## Description:

Publish HTML/JS/CSS demos as GitHub Gists and share gists.page preview links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzir](https://clawhub.ai/user/zzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to publish self-contained or multi-file HTML, CSS, and JavaScript demos to GitHub Gists and return a gists.page preview link for sharing or browser verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing a gist can expose secrets, tokens, private data, or internal material to anyone with the link.

Mitigation: Confirm the exact files to upload, choose secret or public visibility intentionally, and inspect content for sensitive data before publishing.

Risk: Gist publishing requires GitHub credentials that may be too broadly scoped.

Mitigation: Prefer a narrowly scoped GitHub token for Gist publishing and avoid sharing or persisting token values.

Risk: Previewed demo JavaScript runs in the gists.page origin and could request sensitive input from visitors.

Mitigation: Review interactive demo behavior before sharing and do not publish demos that collect secrets or private visitor data.

## Reference(s):

- [Server-resolved source provenance](https://github.com/zzir/gists.page/tree/main/skills/gists-page)
- [ClawHub skill page](https://clawhub.ai/zzir/skills/gists-page)
- [GitHub Gists](https://gist.github.com)
- [GitHub Gists API](https://api.github.com/gists)
- [gists.page preview URL pattern](https://gists.page/{gist_id}/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and preview URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include gist IDs and gists.page preview links after user-approved GitHub Gist publication.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
