## Description:

Create a text-to-video job from user-provided copy. Submits to the remote video service via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuangao](https://clawhub.ai/user/zhangyuangao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit user-provided text to a remote video service, poll the generated task, and report the resulting task_id and video_url.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented shell-command usage with raw user text can create local command execution risk.

Mitigation: Do not run the documented command with raw user text; pass text through a structured no-shell argument API or stdin.

Risk: API-key exposure risk is elevated when the client is used on untrusted networks.

Mitigation: Use only non-sensitive text, restore normal TLS verification, and rotate MAGIC_API_KEY if it was used on untrusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyuangao/skills/magic-text2video)
- [Remote video service endpoint](https://open-test.magiclight.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown chat response with parsed JSON fields and optional JSON code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAGIC_API_KEY; returns task_id first and video_url after polling when successful.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
