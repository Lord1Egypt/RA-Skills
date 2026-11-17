## Description:

Read Intercom conversations by listing, finding, or searching them through Intercom's Conversations API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duyeng](https://clawhub.ai/user/duyeng)

### License/Terms of Use:

MIT

## Use Case:

Developers and support operations teams use this skill to let an agent retrieve Intercom conversation lists, individual conversations, or search results for support analysis and workflow assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Intercom conversations may contain customer or support data that becomes part of agent context.

Mitigation: Use a least-privilege Intercom token and limit prompts to the conversation data needed for the task.

Risk: Dependency drift can reduce reproducibility because the package declares a semver range for intercom-client.

Mitigation: Install with a lockfile or exact vetted dependency version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duyeng/skills/intercom-conversations)
- [OpenAPI contract](artifact/openapi.yaml)

## Skill Output:

**Output Type(s):** [JSON, API data]

**Output Format:** [JSON object with ok/action fields and conversation, conversations, pagination, or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Intercom conversation data; errors return ok: false with error details and may include supported actions.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json, clawhub.skill.json, OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
