## Description:

Model Fallback Retry detects LLM rate-limit, quota, and overload failures, queues the original user message locally, and retries it on a scheduled exponential backoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehe973781230](https://clawhub.ai/user/hehe973781230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to preserve user messages when model calls fail because of rate limits, quota exhaustion, or temporary service overload, then retry those messages without manual re-entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores full AI replies and queued user messages locally, which may include sensitive conversation content.

Mitigation: Enable it only where local retention is acceptable; review file permissions, retention expectations, and whether sensitive conversations should be excluded before deployment.

Risk: The recurring retry job can resend queued user content automatically.

Mitigation: Review cron configuration, destination routing, and maximum retry settings before enabling automatic replay.

## Reference(s):

- [Model Fallback Retry ClawHub Page](https://clawhub.ai/hehe973781230/skills/model-fallback-retry)
- [Artifact README](artifact/README.md)
- [Artifact Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Text responses, local JSON queue records, and shell command invocations for scheduled retry delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores retry state locally and uses configured retry intervals and maximum retry counts.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
