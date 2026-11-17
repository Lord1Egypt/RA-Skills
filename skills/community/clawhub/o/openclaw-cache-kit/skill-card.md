## Description:

Automatically apply Claude prompt caching optimizations to OpenClaw. Reduces API costs by up to 89% via cacheRetention long, 59-minute heartbeat, cache-ttl pruning, and CRON.md separation strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifeissea](https://clawhub.ai/user/lifeissea)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure OpenClaw prompt caching, cache trace logging, and short CRON.md patterns for lower recurring Claude API input-token costs. It also provides shell-based reporting for estimated daily cache savings from local trace logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The apply script persistently edits the local OpenClaw configuration and changes the Claude Sonnet model alias and cache-related defaults.

Mitigation: Review the generated configuration diff before relying on it in an important OpenClaw installation, and keep the generated backup available for rollback.

Risk: The apply script attempts to restart the OpenClaw gateway and may leave the operator needing manual recovery if restart behavior differs from expectations.

Mitigation: Run it during a maintenance window or non-critical session, then verify gateway health and restore the backup manually if needed.

Risk: Cache trace logging is enabled locally and may record operational metadata about cache hits, misses, and token usage.

Mitigation: Review the cache trace settings and log retention expectations before enabling the skill on systems with sensitive operational data.

## Reference(s):

- [OpenClaw Cache Kit on ClawHub](https://clawhub.ai/lifeissea/skills/openclaw-cache-kit)
- [OpenClaw prompt caching optimization guide](https://slashpage.com/thomasjeong/36nj8v2wq5zqj25ykq9z)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash commands and local configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scripts that edit the local OpenClaw configuration, create a backup, restart the gateway, and calculate estimated cache savings from JSONL trace logs.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
