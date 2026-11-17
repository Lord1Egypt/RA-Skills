## Description:

Build backends with PocketBase collections, auth, and realtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a concise PocketBase reference for collections, authentication, realtime subscriptions, file uploads, collection rules, hooks, and admin API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PocketBase admin API and authentication examples may involve privileged credentials or tokens.

Mitigation: Use real credentials or admin tokens only when explicitly required, keep them scoped to the task, and follow the project's credential handling policy.

Risk: Expired PocketBase auth state or orphaned realtime subscriptions can cause stale behavior or resource leaks in applications.

Mitigation: Check auth validity before using authStore data and unsubscribe realtime listeners during cleanup.

## Reference(s):

- [PocketBase skill page](https://clawhub.ai/ivangdavila/skills/pocketbase)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pocketbase binary when users apply the guidance locally; supports linux, darwin, and win32 according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
