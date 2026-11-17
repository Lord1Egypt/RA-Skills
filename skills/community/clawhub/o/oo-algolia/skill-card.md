## Description:

Algolia (algolia.com). Use this skill for ANY Algolia request — reading, creating, updating, and deleting data. Whenever a task involves Algolia, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to search and browse Algolia indices and to retrieve, add, update, or delete records, rules, and synonyms through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unchecked installer whose broader changes to agent skills are under-disclosed.

Mitigation: Review and install the CLI separately, consult its command reference and startup-sync opt-out, connect only needed Algolia permissions, and retain approval checks for changes and deletions.

## Reference(s):

- [Algolia](https://www.algolia.com)
- [Algolia Search REST API documentation](https://www.algolia.com/doc/rest-api/search/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Algolia data; writes and destructive actions require user confirmation according to the skill's instructions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
