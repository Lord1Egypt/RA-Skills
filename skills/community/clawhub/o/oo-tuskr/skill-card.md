## Description:

Use this skill to read, create, and update Tuskr data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to list Tuskr projects, test cases, and test runs, and to create projects, cases, runs, or test results through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger unverified remote code installation without separate approval.

Mitigation: Review the CLI installation before enabling the skill and require approval before running any downloaded installer.

Risk: Connecting Tuskr gives OOMOL access to the authorized account data.

Mitigation: Make the account access clear to the user and retain exact-payload confirmation for changes.

## Reference(s):

- [Tuskr skill release](https://clawhub.ai/oomol/skills/oo-tuskr)
- [Tuskr homepage](https://tuskr.app)
- [Tuskr API documentation](https://tuskr.app/kb/latest/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands and JSON payloads with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Tuskr data require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
