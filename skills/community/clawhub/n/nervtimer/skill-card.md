## Description:

Set one-shot or recurring timers across channels and keep nagging every 5 minutes until the user explicitly says it is done. Uses cron for scheduling, deterministic local state for nagging lifecycle, and LLM-generated reminder text that escalates in urgency over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fragwuerdig](https://clawhub.ai/user/fragwuerdig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Nervtimer to create one-shot or recurring reminder timers that keep notifying the current channel until the user explicitly confirms completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled reminders and local timer state may continue until timers are completed or canceled.

Mitigation: Review active cron jobs and the local Nervtimer state store during installation, use, and removal.

Risk: Scheduled agent turns are instructed to run shell commands built from timer data.

Mitigation: Validate timer IDs before scheduling and encode reminder title and reason as inert data rather than executable instructions.

Risk: Escalating reminder language can become intrusive or inappropriate for some users or channels.

Mitigation: Keep reminder text within the escalation policy guardrails and make reminder language user-configurable before broad deployment.

## Reference(s):

- [Nervtimer ClawHub release](https://clawhub.ai/fragwuerdig/skills/nervtimer)
- [fragwuerdig publisher profile](https://clawhub.ai/user/fragwuerdig)
- [NervTimer Intent Schema](artifact/references/intent-schema.md)
- [NervTimer Escalation Policy](artifact/references/escalation-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates cron scheduling payloads, persistent local timer state, and short reminder messages with escalation guardrails.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
