## Description:

JF Tech Pro AI Smart Search searches JF cloud storage alarm videos with semantic queries such as "person with a hat," "car," or "dog" and returns matching video clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search AI-labeled JF cloud alarm video by natural-language concepts and retrieve matching clips or playback links for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles surveillance playback links and authentication material.

Mitigation: Run it only in a trusted runtime, provide credentials through tightly controlled JF_* environment variables, and avoid logging or broadly sharing generated playback URLs.

Risk: A configurable API host can affect where authenticated requests are sent.

Mitigation: Set JF_ENDPOINT only to documented official JF Tech hosts before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jftech-open-pro-ai-smart-search)
- [JF Open Platform](https://open.jftech.com/)
- [JF Tech API Documentation](https://docs.jftech.com/)
- [JF Tech AI Smart Search Documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557)
- [JF Tech Playback URL Documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python script commands and optional JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF_* environment variables and can return sensitive playback URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
