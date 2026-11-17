## Description:

Webflow (webflow.com). Use this skill for ANY Webflow request — reading, creating, updating, and deleting data. Whenever a task involves Webflow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to read and manage Webflow sites and CMS collections through an OOMOL-connected account. It supports retrieving content and making changes such as creating, updating, publishing, or deleting items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run downloaded code before its behavior is verified.

Mitigation: Review the CLI installer and installation guide before running them, and check whether bundled-skill synchronization affects other agents.

Risk: Write and destructive actions can change Webflow content or publish a site.

Mitigation: Use narrowly scoped Webflow access and confirm the exact target and payload before publishing, editing, or deleting content.

## Reference(s):

- [Webflow Data API documentation](https://developers.webflow.com/data/reference/rest-introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON Webflow connector results and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Webflow action and connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
