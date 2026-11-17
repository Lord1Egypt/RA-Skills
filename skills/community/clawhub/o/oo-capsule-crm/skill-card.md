## Description:

Operate Capsule CRM through an OOMOL-connected account to read, create, update, and delete CRM records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage Capsule CRM parties, tasks, and opportunities through their connected account, including reading, searching, creating, updating, and deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI startup synchronization can add or refresh skills across agent tools.

Mitigation: Review CLI setup and installed skills; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Create, update, and delete actions can change Capsule CRM data.

Mitigation: Keep account access limited, inspect the live action schema, and obtain user approval for the exact write or deletion before running it.

## Reference(s):

- [Capsule CRM](https://capsulecrm.com)
- [Capsule CRM API documentation](https://developer.capsulecrm.com/v2/overview/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON action payloads and CRM results issued through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Capsule CRM account and its permissions.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
