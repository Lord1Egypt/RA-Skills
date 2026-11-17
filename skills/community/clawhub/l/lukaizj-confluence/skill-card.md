## Description:

Confluence REST API integration via curl - lightweight solution without Python dependencies. Supports search, page operations, and file attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search Confluence, inspect spaces and pages, create or update wiki pages, and upload attachments through Confluence REST API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Confluence wiki content and upload attachments.

Mitigation: Review create, update, append, and upload requests before execution and test with non-critical pages or spaces first.

Risk: The skill handles Confluence credentials through shell and curl workflows.

Mitigation: Use a least-privilege API token over HTTPS and avoid passing secrets directly on the command line.

Risk: The security evidence reports unsafe shell practices around credential handling, HTTPS enforcement, JSON construction, and temporary files.

Mitigation: Do not use highly privileged accounts until those issues are fixed and the skill has been reviewed.

## Reference(s):

- [Confluence Integration Skill](https://clawhub.ai/lukaizj/skills/lukaizj-confluence)
- [Project homepage](https://github.com/lukaizj/confluence-integration-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with Confluence API text or JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CONFLUENCE_URL, CONFLUENCE_USER, and CONFLUENCE_PASS; operations may read, create, update, or attach content in the configured Confluence instance.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
