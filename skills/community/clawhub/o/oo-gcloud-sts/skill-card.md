## Description:

Uses the oo CLI to exchange an OOMOL-connected identity for a Google Cloud STS federated access token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to obtain a Google Cloud federated access token through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance understates that the action returns a sensitive Google Cloud access token.

Mitigation: Redact token output and use narrowly scoped Google Cloud access.

Risk: Installation can run unverified scripts and may install additional agent skills.

Mitigation: Verify the CLI release before installation and review any additional skills separately.

## Reference(s):

- [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Google Security Token Service API](https://cloud.google.com/iam/docs/reference/sts/rest/v1/TopLevel/token)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-gcloud-sts)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a Google Cloud federated access token in the connector response.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
