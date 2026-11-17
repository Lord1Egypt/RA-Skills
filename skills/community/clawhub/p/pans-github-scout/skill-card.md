## Description:

Scans GitHub for potential AI company customer leads by searching AI/ML repositories, large-model projects, and training-code activity, then filtering by stars, activity, and company-size signals for CSV or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sales engineers, and go-to-market teams can use this skill to discover AI/ML organizations and repositories that may indicate demand for AI infrastructure or services. It helps search, filter, optionally enrich, and export GitHub-based lead lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported lead files may contain contact, location, and organization profile data that needs privacy-aware handling.

Mitigation: Review CSV or JSON exports for retention, sharing, and privacy requirements before storing or distributing them.

Risk: Supplying a GitHub token on the command line can expose credentials through shell history or process listings.

Mitigation: Use a fine-grained, low-privilege GitHub token through GITHUB_TOKEN or a credential manager instead of the --token argument.

## Reference(s):

- [Pans Github Scout on ClawHub](https://clawhub.ai/dashiming/skills/pans-github-scout)
- [GitHub REST API](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON arrays, or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository metadata, organization profile fields, contact fields, and GitHub API rate-limit messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
