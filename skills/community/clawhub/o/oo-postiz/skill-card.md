## Description:

Postiz (postiz.com). Use this skill for ANY Postiz request — reading, creating, and updating data. Whenever a task involves Postiz, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Postiz through an OOMOL-connected account can use this skill to inspect connected channels and posts, create or schedule social posts, and import media from a URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified oo CLI release.

Mitigation: Review and explicitly approve CLI installation, preferably using a verified release.

Risk: Automatic skill synchronization may introduce broader agent changes without clear user control.

Mitigation: Consider disabling synchronization with the publisher-documented OO_SKILLS_SYNC_DISABLED setting before running the CLI.

Risk: Postiz write actions can create, publish, or schedule content on connected channels.

Mitigation: Confirm the connected channels and the exact publishing payload before running a write action.

## Reference(s):

- [Postiz](https://postiz.com)
- [Postiz Public API documentation](https://docs.postiz.com/public-api/introduction)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-postiz)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action payloads and Postiz action responses, invoked through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Postiz data or create drafts, publish or schedule posts, and import media.]

## Skill Version(s):

1.0.3 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
