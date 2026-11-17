## Description:

Use the OOMOL-connected Shodan service to search host data and retrieve host, DNS, and account information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search Shodan host data and retrieve host, DNS, and account information through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installer scripts that were unavailable for inspection, so their exact system changes are uncertain.

Mitigation: Review the installer and use a verified CLI release; explicitly approve installation before running it.

Risk: Automatic skill synchronization could propagate changes across agent installations.

Mitigation: Disable automatic synchronization unless you want changes to propagate across installations.

Risk: Shodan requests made through OOMOL may consume credits.

Mitigation: Check available credits and monitor usage before running searches.

## Reference(s):

- [Shodan](https://www.shodan.io)
- [Shodan API documentation](https://developer.shodan.io/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON Shodan responses with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host searches, host and DNS lookups, and account information.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
