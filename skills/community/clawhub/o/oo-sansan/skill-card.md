## Description:

Sansan (jp.sansan.com). Use this skill for ANY Sansan request — reading, creating, updating, and deleting data. Whenever a task involves Sansan, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other Sansan users can use the skill to search and read business cards, people, tags, contact reports, and organization settings, and to create, update, or delete supported Sansan records. Administrative actions are limited to users with the required Sansan permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded CLI installer software without integrity checks or separate user approval.

Mitigation: Review and approve CLI installation separately, using a verified release.

Risk: Using the connected Sansan account means OOMOL handles the connection and business data.

Mitigation: Review whether OOMOL should handle your Sansan connection and business data before connecting.

Risk: Bundled-skill synchronization can introduce additional skill content into the environment.

Mitigation: Review or disable bundled-skill synchronization before use.

Risk: Write and destructive actions can change or remove Sansan data.

Mitigation: Retain the skill's confirmation requirements and confirm the exact payload and effect before running those actions.

## Reference(s):

- [Sansan API documentation](https://docs.ap.sansan.com/ja/api/openapi/index.html)
- [oo CLI source](https://github.com/oomol-lab/oo-cli)
- [Sansan homepage](https://jp.sansan.com)

## Skill Output:

**Output Type(s):** [API results, Text, CSV data, Download URLs]

**Output Format:** [JSON responses with human-readable summaries; CSV report or image download URLs where provided by Sansan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results reflect the connected account's permissions. State-changing and destructive actions require confirmation of the exact action and its effect.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
