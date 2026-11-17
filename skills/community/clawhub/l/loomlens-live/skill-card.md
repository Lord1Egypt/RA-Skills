## Description:

LoomLens Live opens an OpenClaw sidebar that estimates prompt costs, recommends models across model clusters, and can dispatch the next prompt with a selected model override.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preview estimated LLM prompt costs, compare model options, and choose a model before sending a prompt through paid or quota-limited access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Signal Loom API key in browser storage.

Mitigation: Use a limited API key where possible, avoid using the skill with sensitive prompts, and remove the key when the sidebar is no longer needed.

Risk: Prompt and model-routing paths are weakly scoped.

Mitigation: Install only in workspaces where the OpenClaw route and sidebar are isolated from untrusted pages or callers, and review behavior before enabling paid model access.

## Reference(s):

- [LoomLens Live ClawHub listing](https://clawhub.ai/avale-slai/skills/loomlens-live)
- [Signal Loom AI](https://signalloomai.com)
- [Signal Loom API signup](https://signallloomai.com/signup.html)
- [OpenAI platform](https://platform.openai.com/)
- [Anthropic](https://www.anthropic.com/)
- [Google AI for Developers](https://ai.google.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, cost estimates, model recommendations, and JSON-like estimate data from the sidebar or route.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include estimated token counts, per-model cost comparisons, fit badges, quota or billing status, and a selected model override for the next prompt.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
