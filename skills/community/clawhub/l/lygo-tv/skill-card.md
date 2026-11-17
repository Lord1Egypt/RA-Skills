## Description:

Directs users to the LYGO TV player and provides code to embed the player on a website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Viewers can find and bookmark the LYGO TV player; website owners and developers can add the player to a site using the supplied embed code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A site using the embed loads third-party browser content and a mutable channel catalog.

Mitigation: Review the embedding guide and the sites the player contacts; use the self-hosted player option if tighter control is needed.

Risk: Optional donation links may be mistaken for a requirement to use the player.

Mitigation: Treat donations as optional; they are not needed to play channels.

## Reference(s):

- [LYGO TV player](https://chatagent.ca/sources/)
- [LYGO TV channel catalog](https://chatagent.ca/sources/catalog.json)
- [LYGO TV on ClawHub](https://clawhub.ai/deepseekoracle/skills/lygo-tv)
- [ClawHub security audit](https://clawhub.ai/deepseekoracle/skills/lygo-tv/security-audit)
- [Embedding guide](embed/README.md)
- [Security notes](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Code, JSON]

**Output Format:** [Plain-text guidance, HTML embed snippet, or JSON link map]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides player links and embed instructions; does not generate or proxy video streams.]

## Skill Version(s):

1.3.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
