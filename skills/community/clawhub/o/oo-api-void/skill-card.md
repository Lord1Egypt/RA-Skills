## Description:

Provides APIVoid domain, IP, and URL reputation checks, email verification, and account usage information through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts can use the skill to check domain, IP, and URL reputation, verify email addresses, and review APIVoid account usage. It runs lookups through the user's connected OOMOL account and returns structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may install lasting instructions into other agents without making that behavior clear.

Mitigation: Review and pin a known CLI release before enabling it. Where supported, set OO_SKILLS_SYNC_DISABLED=1 before starting the CLI to prevent startup skill synchronization.

Risk: Lookup inputs may contain credentials or other sensitive data sent to OOMOL and APIVoid; the external installers and server-side connector were not verified by this artifact review.

Mitigation: Review the CLI and connector setup, and remove URL credentials, tokens, and any lookup data you do not intend to share before making a request.

## Reference(s):

- [APIVoid API documentation](https://docs.apivoid.com/)
- [APIVoid](https://www.apivoid.com/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API results, JSON, Guidance]

**Output Format:** [Structured JSON results with concise natural-language summaries and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on the requested APIVoid action and the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
