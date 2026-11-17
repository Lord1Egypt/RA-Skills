## Description:

Yelp (yelp.com). Use this skill for ANY Yelp request — searching and reading data. Whenever a task involves Yelp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search Yelp businesses, find a business by phone number or identifier, and retrieve business details through a connected Yelp account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads and executes an installer whose contents and exact downloaded release are unverified.

Mitigation: Review and install a verified oo CLI release before using the skill.

Risk: The linked CLI can install additional agent skills without disclosure in this skill.

Mitigation: Consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and account for OOMOL mediating Yelp access.

## Reference(s):

- [Yelp skill release](https://clawhub.ai/oomol/skills/oo-yelp)
- [Yelp homepage](https://www.yelp.com)
- [Yelp Fusion API authentication documentation](https://docs.developer.yelp.com/docs/fusion-authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Business information, JSON]

**Output Format:** [JSON responses containing Yelp business details or search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Yelp action and available business data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
