## Description:

Track Meta (Facebook/Instagram) ad creative performance and hit rates across multiple accounts. Use when asked about creative win rates, which ads are hitting benchmarks, CPT/CPI/ROAS analysis, or comparing creative performance across accounts and time periods. Supports multiple benchmark metrics (CPT, CPI, IPM, ROAS) and currency conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortytwode](https://clawhub.ai/user/fortytwode)

### License/Terms of Use:


## Use Case:

External marketing teams, agencies, and developers use this skill to review Meta Ads creative performance across accounts, compare periods, and identify creatives that meet benchmark metrics such as CPT, CPI, IPM, or ROAS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta Ads access token and reads ad account performance data.

Mitigation: Use a least-privilege, revocable token and install only where access to Meta Ads data is appropriate.

Risk: Ad performance data may be cached locally in SQLite or stored in Firestore.

Mitigation: Restrict access to logs and stored data, and define retention, cleanup, and storage protection practices before deployment.

Risk: API errors or pagination behavior could expose sensitive operational details or fetch from unexpected pagination URLs.

Mitigation: Review error handling, redact sensitive details, and validate pagination hosts before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fortytwode/skills/meta-ad-creatives)
- [Meta Graph API Endpoint](https://graph.facebook.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, JSON configuration, and analysis results from Meta Ads data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache account-level and ad-level performance data locally in SQLite or Firestore depending on configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
