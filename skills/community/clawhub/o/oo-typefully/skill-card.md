## Description:

Operate Typefully to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Typefully account use this skill to inspect social sets and drafts, create or update drafts, and delete drafts through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup path uses remote installers whose behavior was unavailable for inspection.

Mitigation: Review the installation source and use a reviewed, version-pinned CLI installation; require approval before running local setup.

Risk: Startup skill synchronization can make persistent agent changes.

Mitigation: Review the synchronization control before first use and set OO_SKILLS_SYNC_DISABLED=1 when startup synchronization should be disabled.

## Reference(s):

- [Typefully](https://typefully.com)
- [Typefully API documentation](https://typefully.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Typefully on ClawHub](https://clawhub.ai/oomol/skills/oo-typefully)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Configuration instructions]

**Output Format:** [JSON command responses and concise text summaries, with shell commands for the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read Typefully data or change drafts; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
