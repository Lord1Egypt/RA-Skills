## Description:

Operate Browserless through an OOMOL-connected account to fetch rendered page content, generate PDFs, and capture screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use the skill to retrieve rendered web page content, create PDFs, and capture screenshots through an existing OOMOL Browserless connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Browserless workflow is coherent, but its automatic software setup and undisclosed agent-skill changes need review.

Mitigation: Review and install the CLI yourself before enabling this skill. Consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented by the publisher, and send only URLs and payloads you intend OOMOL and Browserless to process.

## Reference(s):

- [Browserless API documentation](https://docs.browserless.io/)
- [Browserless](https://www.browserless.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, PDF, Screenshots]

**Output Format:** [JSON responses containing rendered HTML or base64-encoded PDF and image data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Browserless action and its live input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
