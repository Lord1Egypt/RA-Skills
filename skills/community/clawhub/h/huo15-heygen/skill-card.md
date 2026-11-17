## Description:

Helps agents generate HeyGen digital avatar videos from text scripts using local HeyGen API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create digital-avatar videos, greetings, marketing shorts, product introductions, and batch video jobs through HeyGen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a local HeyGen credentials file containing an API key and avatar ID.

Mitigation: Keep heygen_creds.json protected, do not commit or share it, and restrict access to approved local users.

Risk: Text scripts are sent to HeyGen and API calls may be billed.

Mitigation: Review scripts before generation, avoid secrets or regulated data unless approved, and monitor HeyGen usage and costs.

Risk: Generated videos may depend on HeyGen processing time, service limits, and API rate limits.

Mitigation: Use polling with timeouts, handle failed statuses, and respect HeyGen rate-limit guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-heygen)
- [HeyGen API base URL](https://api.heygen.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated code uses local HeyGen credentials and can return video IDs, generation status, and video URLs when executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
