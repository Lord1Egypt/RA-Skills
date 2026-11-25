## Description:

Collects publicly available videos from a Kuaishou profile and exports the results as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide a Kuaishou profile link to review and export a creator's public video list for creator screening, content inventory, or competitor account monitoring. Before collection, the agent confirms the profile, page count, and estimated point cost with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags risky transport or certificate settings, exposed bearer credentials, and capabilities beyond profile video collection. Its scan is incomplete and does not establish malicious intent.

Mitigation: Before installation or use, clarify endpoint transport and certificate validation, token handling, and the additional collection and logout capabilities.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mystery77777777/skills/ks-profile)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [CSV file and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV includes a UTF-8 BOM for Excel. Each task covers one profile and 1–10 pages; some fields may be blank when unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
