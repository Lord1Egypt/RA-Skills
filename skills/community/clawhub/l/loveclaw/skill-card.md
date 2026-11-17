## Description:

LoveClaw is an OpenClaw agent skill for conversational dating profile registration, daily bazi-based local matching, optional photo handling, and evening match report delivery through a cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackysly88](https://clawhub.ai/user/jackysly88)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use LoveClaw to create dating profiles, submit optional photos, receive daily city-and-preference-compatible bazi match results, and manage evening push notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo handling, credential, environment, and scheduling behavior are broader than users would reasonably expect.

Mitigation: Install only after reviewing the publisher, preferably in an isolated OpenClaw workspace with a dedicated LOVECLAW_API_TOKEN.

Risk: A shared workspace .env could expose unrelated API_TOKEN-style secrets or route the skill to an unexpected API endpoint.

Mitigation: Keep unrelated API_TOKEN secrets out of the shared workspace .env and verify LOVECLAW_API_BASE before use.

Risk: Photo inputs and local session files may create privacy or access-control risk when used with real users.

Mitigation: Avoid submitting local file paths as photos and require fixes for photo path validation, session-file permissions, and global session-registry access before production use.

Risk: Dependency age and scheduled notification behavior require operational review.

Mitigation: Update dependencies and review scheduled match/report delivery behavior before deploying with real users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackysly88/skills/loveclaw)
- [Publisher Profile](https://clawhub.ai/user/jackysly88)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text chat responses and JSON-marked scheduled report payloads, with shell commands and configuration guidance for cron delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed image URLs for uploaded photos or match reports.]

## Skill Version(s):

21.21.21 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
