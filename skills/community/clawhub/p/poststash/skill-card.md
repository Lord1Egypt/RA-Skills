## Description:

Schedule posts and threads to Threads and X via PostStash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliendsv](https://clawhub.ai/user/juliendsv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create drafts, schedule single posts, schedule threads, list posts, and inspect post status or analytics for a PostStash account connected to Threads or X.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can schedule or publish agent-generated social posts using the configured PostStash account.

Mitigation: Review content before scheduling and use Draft for unreviewed content.

Risk: The skill requires a PostStash API key that can schedule or draft posts and read post status or analytics for the account.

Mitigation: Store the key only in POSTSTASH_API_KEY, use the least-privileged key available, and avoid exposing production credentials to untrusted agents.

Risk: Example commands may run package dependencies while credentials are present.

Mitigation: Pin or install dependencies locally before running examples with production credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juliendsv/skills/poststash)
- [PostStash API documentation](https://poststash.com/docs/api)
- [PostStash dashboard API keys](https://poststash.com/dashboard/api-keys)
- [PostStash](https://poststash.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON responses from PostStash tools, with human-facing guidance from the agent when used conversationally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTSTASH_API_KEY. Tool responses can include post IDs, content, schedules, statuses, platforms, pagination, and analytics metrics.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
