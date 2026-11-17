## Description:

Use Pinboard through an OOMOL-connected account to retrieve, add, update, or delete bookmarks and inspect tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing bookmarks in Pinboard use this skill to find bookmarks, inspect tags and update Pinboard data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can change installed agent skills without clearly disclosing those effects.

Mitigation: Review the CLI release and its effects before proceeding; set OO_SKILLS_SYNC_DISABLED=1 to disable automatic skill synchronization.

Risk: Adding or deleting a bookmark can replace or remove Pinboard data.

Mitigation: Confirm the exact target and payload before running add_bookmark or delete_bookmark, as the skill directs.

## Reference(s):

- [Pinboard](https://pinboard.in/)
- [Pinboard API documentation](https://pinboard.in/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Connect Pinboard in OOMOL](https://console.oomol.com/connections/pinboard)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured Pinboard results and concise task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return bookmark or tag data; add and delete actions change Pinboard data and require confirmation as described in the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
