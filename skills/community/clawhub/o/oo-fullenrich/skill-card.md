## Description:

Search and read FullEnrich data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check workspace credit balance and look up company or person records in FullEnrich.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded code and change other installed agent skills; the remote installer contents were not inspected.

Mitigation: Review the setup behavior and separately approve a verified CLI installation; consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: FullEnrich requests and account access are mediated through OOMOL.

Mitigation: Use the skill only when comfortable routing lookups through the connected OOMOL account.

## Reference(s):

- [FullEnrich](https://www.fullenrich.com)
- [FullEnrich API documentation](https://docs.fullenrich.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on the connected FullEnrich account and available credits.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
