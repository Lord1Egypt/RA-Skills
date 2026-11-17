## Description:

Use this skill to search Explorium business data and retrieve company firmographic or technographic profiles through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Explorium to match businesses by name, domain, or URL, look up filter values, and retrieve firmographic or technographic data. Requests run through the user's OOMOL-connected account, and some data requests may consume credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A routine Explorium request could trigger an unverified software installer without a clear approval step.

Mitigation: Review the installation fallback before use, deliberately install a verified CLI version, check its agent-skill installation behavior, and review OOMOL connection permissions.

## Reference(s):

- [Explorium](https://www.explorium.ai/)
- [Explorium API documentation](https://explorium-api.readme.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON results with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can handle batches of one to fifty businesses for enrichment; some requests may consume credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
