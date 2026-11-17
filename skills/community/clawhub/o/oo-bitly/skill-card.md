## Description:

Bitly (bitly.com). Use this skill for ANY Bitly request — reading, creating, and updating data. Whenever a task involves Bitly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read Bitly account, group, and link information, create short links, and update editable Bitlink fields through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented automatic CLI setup runs an unverified installer, and startup synchronization can change other agents' skills.

Mitigation: Review and pin the installation, and set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you do not want skill synchronization.

Risk: Creating short links and updating Bitlinks change Bitly data.

Mitigation: Preserve user confirmation for the exact link changes before running write actions.

## Reference(s):

- [Bitly API Reference](https://dev.bitly.com/api-reference/)
- [Bitly](https://bitly.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured Bitly connector responses and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create and update actions change Bitly data and require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
