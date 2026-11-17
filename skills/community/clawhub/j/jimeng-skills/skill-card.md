## Description:

Produces image and video generation requests through Volcengine Jimeng AI and returns plain text summaries, remote URLs, public share URLs, and local file paths suitable for enterprise IM clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klaus1534](https://clawhub.ai/user/klaus1534)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to request Jimeng image or video generation and package results for Feishu, WeCom, DingTalk, and debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runnable implementation referenced by the skill is missing from the artifact.

Mitigation: Ask the publisher to include skill.yaml, scripts/openclaw-jimeng.ts, package.json, and a lockfile before installing or running the skill.

Risk: The examples execute an unpinned npm tool.

Mitigation: Prefer pinned dependency execution or local-only dependency execution after review.

Risk: Volcengine credentials may be present during testing.

Mitigation: Use least-privilege or temporary Volcengine credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/klaus1534/skills/jimeng-skills)
- [Publisher profile](https://clawhub.ai/user/klaus1534)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Plain text with URL and file-path lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remoteUrls, publicUrls, localFiles, and pending status when a task is not complete.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
