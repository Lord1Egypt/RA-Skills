## Description:

Operate an Upstash Redis database through an OOMOL-connected account, including key scans, reads, writes, expiration changes, and deletions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage data in a connected Upstash Redis database through OOMOL. It supports key scans, value reads and writes, expiration checks or changes, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified CLI installer and may make broader changes to the agent setup.

Mitigation: Review and approve a specific CLI release before installation, and decide whether it may install or update other agent skills.

Risk: The hosted connector implementation is unverified and mediates access to Redis data.

Mitigation: Connect only the intended Redis database and retain confirmation for write and destructive actions.

## Reference(s):

- [Upstash Redis](https://upstash.com/redis)
- [Upstash Redis REST API documentation](https://upstash.com/docs/redis/features/restapi)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Connect Upstash Redis in OOMOL](https://console.oomol.com/connections/upstash_redis)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-upstash-redis)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and JSON responses, accompanied by Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read Redis data or change it; write and destructive actions require user confirmation as described by the skill.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
