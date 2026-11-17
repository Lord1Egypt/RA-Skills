## Description:

Operate PostHog through an OOMOL-connected account to read and manage analytics data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect PostHog projects, dashboards, cohorts, events, insights, and feature flags, and to make approved changes through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may install persistent skills across agents without that behavior being clearly described in the skill.

Mitigation: Review any additional skills before enabling them, use a verified fixed CLI release, and set OO_SKILLS_SYNC_DISABLED=1 if startup skill synchronization is unwanted.

Risk: PostHog write and deletion actions can change connected account data.

Mitigation: Use a narrowly scoped PostHog connection and retain user approval for changes and deletions.

## Reference(s):

- [PostHog homepage](https://posthog.com)
- [PostHog API documentation](https://posthog.com/docs/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [PostHog skill release](https://clawhub.ai/oomol/skills/oo-posthog)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands, JSON request payloads, and returned PostHog data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete PostHog data require user confirmation; outputs depend on the connected account and PostHog response.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
