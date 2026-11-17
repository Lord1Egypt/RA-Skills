## Description:

Use BoloForms to retrieve form responses, review documents and signing participants, and start template signing requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with a BoloForms workspace use this skill to retrieve form responses, review documents and signing status, and initiate template signing requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can make persistent changes to other agents' skills that the skill does not explain.

Mitigation: Review and preinstall a verified CLI release; set OO_SKILLS_SYNC_DISABLED=1 before running oo commands if you do not want it changing other agents' skills.

Risk: Starting a signing request changes BoloForms state and relies on connected credentials.

Mitigation: Use narrowly scoped BoloForms credentials and confirm the signing recipients and payloads before sending.

## Reference(s):

- [BoloForms](https://www.boloforms.com)
- [BoloSign API documentation](https://bolosign-developer-docs.readme.io/reference/intro/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text]

**Output Format:** [Structured JSON results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate template signing requests; action inputs are checked against the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
