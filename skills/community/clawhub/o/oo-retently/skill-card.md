## Description:

Retently (retently.com). Use this skill for ANY Retently request — reading, creating, and updating data. Whenever a task involves Retently, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Retently through an OOMOL-connected account can retrieve account, customer, feedback, campaign, and survey-template data, and create or update customers in bulk. Customer upserts change account data and require confirmation of the specific payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup or synchronization may run unverified remote code and make broader persistent changes; the OOMOL connector mediates access to Retently customer data.

Mitigation: Install a trusted, verified CLI version yourself, review its cross-agent installation and synchronization behavior, and inspect each update payload before approving it. The hosted connector implementation was not verified.

## Reference(s):

- [Retently API documentation](https://www.retently.com/docs/api/)
- [Retently](https://www.retently.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Retently skill page](https://clawhub.ai/oomol/skills/oo-retently)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON requests and service responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results depend on the connected Retently account; customer upserts require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
