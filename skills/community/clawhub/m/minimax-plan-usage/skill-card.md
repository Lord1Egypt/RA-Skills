## Description:

Query MiniMax Token Plan usage and reset times for supported text, speech, video, image, and music models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-zxyz](https://clawhub.ai/user/alex-zxyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check MiniMax Token Plan remaining usage and reset times from an agent slash command without opening the MiniMax web console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MiniMax API key can be sent to a configurable API host or exposed if passed as a command-line argument.

Mitigation: Leave MINIMAX_API_HOST unset or restrict it to the MiniMax HTTPS host, provide MINIMAX_API_KEY through a protected secret mechanism, and avoid passing the key with --api-key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-zxyz/skills/minimax-plan-usage)
- [MiniMax Token Plan](https://platform.minimax.io/subscribe/token-plan)
- [MiniMax coding plan remains API endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown usage summary by default, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and supports optional MINIMAX_API_HOST.]

## Skill Version(s):

1.0.0 (source: server release metadata and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
