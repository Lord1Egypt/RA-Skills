## Description:

Use this skill for Namely requests involving searching and reading data, instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR administrators use the skill to search and read Namely profile information and available profile fields through an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When the oo CLI is missing, setup directs the agent to execute a downloaded installer whose contents and bundled-skill behavior were not verified.

Mitigation: Review and approve CLI installation separately, including its bundled-skill installation behavior, before allowing setup to run.

Risk: The connected Namely account can expose employee profile data, and OOMOL handles authentication and requests.

Mitigation: Connect only an authorized account with the minimum employee-data access needed, and consider OOMOL's role in handling authentication and requests.

## Reference(s):

- [Namely skill release](https://clawhub.ai/oomol/skills/oo-namely)
- [Namely](https://www.namely.com)
- [Namely API documentation](https://developers.namely.com/docs/namely-api/72f9086e4f0e7-introduction)
- [oo CLI repository (CLI reference)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only profile information; results depend on the connected Namely account's permissions.]

## Skill Version(s):

1.0.5 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
