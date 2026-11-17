## Description:

Operate Griptape Cloud through OOMOL's connected Griptape account to read, create, update, and delete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers who manage Griptape Cloud assistants, runs, events, and organizations can use this skill to perform those tasks through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's setup instructions run a remote installer without verifying it or obtaining separate installation approval.

Mitigation: Review and approve the CLI installation separately, using a verified release.

Risk: Automatic bundled-skill synchronization and the hosted connector implementation were not verified.

Mitigation: Check or disable automatic bundled-skill synchronization, connect only the Griptape permissions needed, and retain confirmations for changes and deletions.

## Reference(s):

- [Griptape homepage](https://www.griptape.ai)
- [Griptape Cloud API reference](https://docs.griptape.ai/stable/griptape-cloud/api/api-reference/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Griptape skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-griptape)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
