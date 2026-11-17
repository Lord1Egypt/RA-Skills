## Description:

Search PredictLeads for company data, financing events, job openings, news, and technology detections through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use this skill to retrieve PredictLeads company information by website domain, including firmographic data and detected business events. It is intended for read-only searching and lookup through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute installers whose effects were unavailable for inspection, including automatic installation of other agent skills.

Mitigation: Review and install the oo CLI separately, and decide whether automatic installation of other skills is acceptable before enabling this skill.

## Reference(s):

- [PredictLeads API documentation](https://docs.predictleads.com/v3/)
- [PredictLeads](https://predictleads.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-predictleads)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [PredictLeads results returned as JSON, with usage and setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected PredictLeads account and the requested company domain.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
