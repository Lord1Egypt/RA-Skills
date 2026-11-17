## Description:

Chooses the video model a Phantra scene renders on and writes the scene for it: `video_models` for what each model takes (lengths, frames, credits, a draft frame), `recommend_model` for a job described in words, and the wording that follows from the catalogue. Use when someone asks which model to use, what a model takes, why a quote is what it is, or how to write for a model. NOT for the scene's story and beats (write-scene), the balance (credits-and-limits) or camera language (camera-moves).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

### License/Terms of Use:

MIT-0

## Use Case:

Creators using Phantra can compare video models against a scene's length, frame, sound needs, and credit budget, then shape scene wording to the selected model. They can review the quote and approve rendering with the stated cost before it runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering sends scene text to the selected provider and spends credits.

Mitigation: Review the quote and explicitly approve its price before rendering.

Risk: Workspace model defaults can persist and affect later quotes.

Mitigation: Check the workspace defaults when selecting or changing a preferred model.

## Reference(s):

- [Phantra AI: Model Prompting on ClawHub](https://clawhub.ai/zeropage-onryo/skills/phantra-ai-model-prompting)
- [Publisher profile: zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Concise model recommendations, scene wording guidance, and quote and approval instructions in Markdown text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the model catalogue and current quote for capabilities and pricing; does not promise that different models will render identically.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
