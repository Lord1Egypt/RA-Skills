## Description:

Access JPX stock market data via J-Quants API - search stocks, get daily OHLCV prices, financial summaries (revenue, profit, EPS, ROE), and earnings calendar for Tokyo Stock Exchange (TSE) listed companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp)

### License/Terms of Use:

J-Quants Terms of Service

## Use Case:

External users and agents use this skill to query TSE-listed company search results, daily OHLCV prices, financial summaries, and earnings calendar data through the jquants-mcp command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party jquants-mcp command that handles J-Quants credentials.

Mitigation: Confirm the package source is trusted, pin a reviewed version before deployment, and update only after review.

Risk: J-Quants credentials are supplied through environment variables.

Mitigation: Use credentials scoped to the intended J-Quants account, avoid exposing unrelated secrets in the same environment, and rotate the password if compromise is suspected.

Risk: J-Quants data redistribution is restricted by the service terms.

Mitigation: Use retrieved market data only within the allowed personal-use scope and review the J-Quants Terms of Service before sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajtgjmdjp/skills/jquants-mcp)
- [J-Quants service](https://jpx-jquants.com/)
- [J-Quants Terms of Service](https://jpx-jquants.com/termsofservice)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; command results may be text or JSON when --json-output is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the jquants-mcp command and JQUANTS_MAIL_ADDRESS and JQUANTS_PASSWORD environment variables.]

## Skill Version(s):

0.1.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
