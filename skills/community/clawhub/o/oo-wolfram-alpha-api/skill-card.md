## Description:

Use Wolfram|Alpha to search for answers and validate queries through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can ask an agent to retrieve concise or spoken-style Wolfram|Alpha answers, or check whether a query can be interpreted, using their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run unchecked software and make broader agent changes than the skill explains.

Mitigation: Review setup before enabling; use a reviewed, pinned CLI installation and set OO_SKILLS_SYNC_DISABLED to disable startup skill synchronization when desired.

Risk: The remote installers and hosted connector were not verified, and queries may incur charges.

Mitigation: Review the installer and connector before use, and account for possible query charges.

## Reference(s):

- [Wolfram|Alpha API](https://products.wolframalpha.com/api/)
- [Wolfram|Alpha API documentation](https://products.wolframalpha.com/api/documentation)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a concise answer, a spoken-style answer, or a query validation result.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
