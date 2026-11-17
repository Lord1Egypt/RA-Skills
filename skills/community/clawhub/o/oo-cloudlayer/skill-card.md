## Description:

Use the connected cloudlayer.io account to create PDF jobs and read account, job, and asset data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create HTML, template, or public URL PDF jobs and inspect cloudlayer.io account usage, jobs, and generated assets through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local setup may run unverified downloaded code and make broader changes to the agent environment.

Mitigation: Review setup scripts, install a verified fixed CLI release, and decide whether to allow its bundled skill synchronization.

Risk: Connected-account credentials and submitted document data are handled by OOMOL, and PDF job creation submits data to the provider.

Mitigation: Use an account appropriate for the data and confirm the exact payload and effect before creating a PDF job.

## Reference(s):

- [cloudlayer.io](https://cloudlayer.io)
- [cloudlayer.io API documentation](https://docs.cloudlayer.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service responses with concise task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job status and account, job, or asset details; PDF creation returns an asynchronous job status.]

## Skill Version(s):

1.0.5 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
