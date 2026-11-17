## Description:

Dispatch coding tasks to Warp Oz cloud agents, manage runs and schedules, and chain specialized agents into multi-stage review pipelines from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in-liberty420](https://clawhub.ai/user/in-liberty420)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to launch and monitor Warp Oz cloud coding agents, manage scheduled agent runs, retrieve run artifacts, and orchestrate multi-agent coding and review pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote cloud agents receive repository access and task context.

Mitigation: Install only if you trust Warp Oz with the target repository and tasks, and use a least-privilege Warp API key and environment.

Risk: The skill requires an API token to launch and manage Warp Oz runs.

Mitigation: Store WARP_API_KEY securely or use OP_WARP_REFERENCE, and avoid exposing credentials in prompts, logs, or shared artifacts.

Risk: Shared conversation sandboxes can carry context across stages.

Mitigation: Avoid reusing conversation sandboxes for sensitive or untrusted work; use isolated environments or the no-conversation mode when appropriate.

Risk: Schedule create, update, pause, resume, and delete commands affect remote automated runs.

Mitigation: Review schedule commands, target environments, and cron settings before execution.

Risk: Generated code or pull requests may be incorrect or unsuitable for the target repository.

Mitigation: Review, test, and scan generated changes before merging or deploying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/in-liberty420/skills/oz)
- [Oz Agent REST API Reference](references/api.md)
- [Agent Role Definitions](references/agent-roles.md)
- [Warp Oz API](https://app.warp.dev/api/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, and WARP_API_KEY; may produce run IDs, status payloads, artifact data, session links, schedule changes, and pipeline summaries.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
