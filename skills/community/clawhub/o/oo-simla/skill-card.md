## Description:

Use a connected Simla.com account to read, create, and update customer and order data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find Simla customers, orders, and order statuses, and to create or edit customer and order records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run remote installer scripts whose contents were not reviewed.

Mitigation: Review the installer separately and use a verified, pinned release; inspect the agent-skill synchronization settings before allowing setup to run.

Risk: Create and edit actions change Simla customer or order records.

Mitigation: Confirm the exact payload and effect with the user before running each write action.

## Reference(s):

- [Simla.com](https://www.simla.com/en)
- [Simla API v5 documentation](https://docs.simla.com/Developers/API/APIVersions/APIv5)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON payloads and shell commands with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
