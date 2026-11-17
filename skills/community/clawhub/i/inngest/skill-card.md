## Description:

Manage Inngest serverless background jobs and event-driven workflows via REST API, including sending events, triggering functions, listing runs, canceling jobs, and inspecting workflow history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwhite-oss](https://clawhub.ai/user/dwhite-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Inngest event-driven workflows through REST API calls, including sending events, inspecting runs, and taking job actions such as cancel or replay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide cancel, replay, and event-sending actions that may affect production Inngest workflows.

Mitigation: Review user prompts before allowing account-affecting actions, especially against production environments.

Risk: Over-scoped event or signing keys could allow broader Inngest account operations than intended.

Mitigation: Use keys scoped to the intended environment and rotate or revoke them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwhite-oss/skills/inngest)
- [Inngest management API base](https://api.inngest.com/v1)
- [Inngest event ingestion endpoint](https://inn.gs/e/$INNGEST_EVENT_KEY)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INNGEST_EVENT_KEY and INNGEST_SIGNING_KEY environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
