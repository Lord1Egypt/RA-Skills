## Description:

Generates music from text prompts and optional lyrics using MiniMax music models with a MINIMAX_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external creators use this skill to call MiniMax's music-generation API from Python, choose a supported model, provide a text prompt and optional lyrics, and save the generated audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, and request metadata are sent to MiniMax.

Mitigation: Avoid sensitive unpublished lyrics or confidential prompts, and use the skill only when MiniMax processing is acceptable for the intended content.

Risk: MINIMAX_API_KEY grants access to the configured MiniMax account.

Mitigation: Set the API key only for authorized users and prefer environment or secret-management controls that limit exposure.

Risk: The skill downloads generated audio from a provider-returned URL.

Mitigation: Run it from a network environment where that download flow cannot expose private internal services.

Risk: The Python dependency is installed manually and may drift over time.

Mitigation: Use a virtual environment with pinned dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/skills/minimax-music-gyh)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples and an audio file output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests package, and MINIMAX_API_KEY; generated audio is saved to the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
