## Description:

Checks Kimi API usage, subscription quota, account status, and Kimi Code limits, with optional saved login state for repeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muselinn](https://clawhub.ai/user/muselinn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kimi users use this skill to check current API usage, subscription details, feature quota, and reset timing from a Kimi account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a reusable Kimi login cookie and can store it locally; server security evidence warns that saved cookies may have weak or no real encryption.

Mitigation: Avoid saving the cookie unless cryptography is installed and a strong KIMI_QUOTA_KEY is set; clear saved credentials with --clear when no longer needed.

## Reference(s):

- [Kimi](https://www.kimi.com)
- [Kimi subscription page](https://www.kimi.com/membership/subscription)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text quota report or JSON, with setup and credential-management commands when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Kimi cookie or token; can optionally save and later clear the local login cookie.]

## Skill Version(s):

1.0.1 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
