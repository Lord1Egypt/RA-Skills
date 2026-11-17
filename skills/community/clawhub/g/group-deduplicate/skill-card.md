## Description:

Provides command-line utilities for deduplicating community-group candidates with a Redis-backed memory cache, MD5-derived group keys, and a default 30-day cache TTL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiiang0529](https://clawhub.ai/user/xiiang0529)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to filter repeated WeChat, QQ, or industry group candidates and manage the Redis cache that records previously seen group names. It is best treated as an administrative deduplication helper because the security review says the packaged search behavior is not a reliable real group-search implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe executable-path handling through workspace-controlled subprocess calls.

Mitigation: Run only in a controlled workspace with a known-safe WORKSPACE value and a trusted memory-cache installation.

Risk: The security review reports that the package does not perform reliable real searches despite claiming search behavior.

Mitigation: Treat results as prototype or generated candidates and verify any group names or links before acting on them.

Risk: Cached group names and related history can persist in Redis for up to 30 days and can be listed or modified by the cache manager.

Mitigation: Avoid caching sensitive group names, limit Redis access, and clear or shorten the cache TTL when retention is not needed.

Risk: Child processes inherit the environment when calling the memory-cache helper.

Mitigation: Run with only necessary environment variables and avoid exposing secrets to the skill process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiiang0529/skills/group-deduplicate)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text command output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted memory-cache installation and Redis configuration; cached group names can persist for the configured TTL, default 30 days.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
