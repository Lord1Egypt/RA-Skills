## Description:

Use Apple Maps through an OOMOL-connected account to search for places and read map data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use the skill to search Apple Maps, look up places and addresses, and request routes or travel estimates through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI setup downloads and executes installer code that was not verified in the security review.

Mitigation: Review and approve CLI installation separately before allowing the fallback; use an already installed CLI when possible.

Risk: Automatic skill synchronization may introduce changes to other agent skills without clear approval.

Mitigation: Consider disabling automatic synchronization with OO_SKILLS_SYNC_DISABLED as documented in the oo CLI command reference.

Risk: Maps queries pass through OOMOL.

Mitigation: Avoid sending location or search details that should not be shared with OOMOL.

## Reference(s):

- [Apple Maps](https://developer.apple.com/maps/)
- [Apple Maps Server API documentation](https://developer.apple.com/documentation/applemapsserverapi)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Apple Maps ClawHub skill page](https://clawhub.ai/oomol/skills/oo-apple-maps)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured Apple Maps results and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Apple Maps service and OOMOL account.]

## Skill Version(s):

1.0.2 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
