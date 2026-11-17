## Description:

Campaign link builder and pre-launch validator for AI agents. Build UTM-tracked links, validate destinations, and inspect landing pages for social sharing readiness (OG tags, Twitter Cards, viewport, canonical, favicons). The mlz preflight command does everything in one call and returns a go/no-go report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewlamamills-tech](https://clawhub.ai/user/andrewlamamills-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and developer agents use MissingLinkz to generate UTM-tracked campaign URLs, validate destinations, and inspect landing pages before social, email, paid-ad, or campaign launches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send marketing URLs and campaign metadata to the MissingLinkz service.

Mitigation: Use it only when sharing that campaign metadata with MissingLinkz is acceptable, and review URLs before execution.

Risk: API-backed features require MLZ_API_KEY and may store credentials in ~/.missinglinkz/config.json.

Mitigation: Require explicit approval before registration or login, protect the API key, and rotate or revoke it if exposure is possible.

Risk: The skill encourages broad service use, paid-plan recommendations, and global CLI installation.

Mitigation: Require human approval before purchase recommendations and prefer a pinned or project-local install where feasible.

## Reference(s):

- [MissingLinkz homepage](https://missinglinkz.io)
- [ClawHub skill page](https://clawhub.ai/andrewlamamills-tech/skills/missinglinkz)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the mlz CLI and may require MLZ_API_KEY for API-backed storage, campaign management, and account features.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
