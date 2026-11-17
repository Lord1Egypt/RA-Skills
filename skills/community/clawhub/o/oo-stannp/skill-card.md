## Description:

Stannp (stannp.com). Use this skill for ANY Stannp request — reading, creating, updating, and deleting data. Whenever a task involves Stannp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to work with Stannp through an OOMOL-connected account. It retrieves account, recipient, and group information; creates or changes recipients and groups; and validates postal addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI setup runs remote installer code whose contents and exact system effects are unverified, without a separate approval step.

Mitigation: Review and approve CLI installation separately using a verified release, and review its bundled-skill synchronization settings.

Risk: The connected Stannp account can be used to change or delete recipients and groups.

Mitigation: Keep the skill's confirmation requirements for write and destructive actions, and review the exact target and effect before approving.

## Reference(s):

- [Stannp API documentation](https://www.stannp.com/us/direct-mail-api/guide)
- [Stannp](https://www.stannp.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON connector requests and responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
