## Description:

Helps agents search and read Streak data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

For users who need to read Streak data such as pipelines, boxes, and the authenticated user's profile. The skill expects the oo CLI to be installed and the Streak connection to be configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute a remote installer without a separate approval step.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and check whether the CLI installs or updates other agent skills.

Risk: Connecting Streak gives OOMOL access to the authorized business data, while external installer and CLI behavior is not fully established by the inspected skill file.

Mitigation: Connect only an account whose data access is intended, and review the CLI's behavior before setup.

## Reference(s):

- [Streak](https://www.streak.com/)
- [Streak API documentation](https://streak.readme.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover read-only Streak actions; an oo CLI installation and authorized Streak connection are required.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
