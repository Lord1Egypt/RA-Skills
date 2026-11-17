## Description:

Freshstatus (freshworks.com). Use this skill for ANY Freshstatus request — reading, creating, updating, and deleting data. Whenever a task involves Freshstatus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and status page administrators use the skill to read and manage Freshstatus services and service groups through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup and its persistent changes to agent skills need review.

Mitigation: Review and approve the CLI installation separately, preferably using a verified, pinned release. Disable cross-agent skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not wanted.

Risk: Freshstatus write actions change status page data, and destructive actions remove data.

Mitigation: Confirm the exact payload and effect before write actions, and confirm the target and obtain explicit approval before destructive actions.

## Reference(s):

- [Freshstatus API documentation](https://support.freshstatus.io/support/solutions/articles/50000003646-freshstatus-api-documentation)
- [Freshstatus homepage](https://www.freshworks.com/statuspage)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read, write, and destructive Freshstatus actions; changes require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
