## Description:

Coresignal (coresignal.com). Use this skill for ANY Coresignal request — searching and reading data. Whenever a task involves Coresignal, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Coresignal company records and collect a company record through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can install downloaded CLI software and affect installed agent skills; the remote installers were not available for review.

Mitigation: Review and approve CLI installation separately, and use a fixed release whose contents have been independently verified before allowing installation.

Risk: Using this connector entrusts OOMOL with Coresignal credentials and queries.

Mitigation: Use an approved account connection and avoid sending sensitive queries or records unless their use with OOMOL is permitted.

## Reference(s):

- [Coresignal API authorization documentation](https://docs.coresignal.com/api-introduction/authorization)
- [Coresignal](https://coresignal.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON connector responses and concise Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company search results and collected company records depend on the Coresignal connection and the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
