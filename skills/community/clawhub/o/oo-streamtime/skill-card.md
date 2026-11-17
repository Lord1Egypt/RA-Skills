## Description:

Streamtime (streamtime.net). Use this skill for ANY Streamtime request — reading, creating, and updating data. Whenever a task involves Streamtime, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Streamtime-connected business account can use this skill to retrieve organisation, company, contact, job, branch, rate-card, and user information, or create and update companies, contacts, and jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded CLI code that the security review marks unverified.

Mitigation: Review the CLI installation before enabling automatic setup.

Risk: Create and update actions change records in the connected Streamtime business account.

Mitigation: Confirm the exact action payload and effect before each change.

Risk: The CLI may automatically synchronize agent skills, which can affect local skill files.

Mitigation: Review synchronization behavior and the OO_SKILLS_SYNC_DISABLED control before running the CLI.

## Reference(s):

- [Streamtime public API documentation](https://help.streamtime.net/en/articles/12854233-using-the-streamtime-public-api)
- [Streamtime](https://www.streamtime.net)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action results with command and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results include data and execution metadata; input fields are determined from the live action schema.]

## Skill Version(s):

1.0.5 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
