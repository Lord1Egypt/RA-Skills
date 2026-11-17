## Description:

Manage KlickTipp subscribers and tags through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to add or update KlickTipp subscribers, unsubscribe contacts, and remove subscriber tags through an already-connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may persistently install other agent skills without disclosing that behavior in this skill.

Mitigation: Review the CLI's installation behavior, use a verified CLI release, and consider setting OO_SKILLS_SYNC_DISABLED=1 for every invocation, as the publisher documentation describes.

Risk: Subscriber contact data is processed by OOMOL, and some actions unsubscribe contacts or remove tags.

Mitigation: Confirm the exact contact and the effect of each write or destructive action before running it.

## Reference(s):

- [KlickTipp](https://www.klicktipp.com)
- [KlickTipp Listbuilding API guide](https://developers.klicktipp.com/guides/listbuilding-api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation; contact and tag changes are performed through the connected account.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
