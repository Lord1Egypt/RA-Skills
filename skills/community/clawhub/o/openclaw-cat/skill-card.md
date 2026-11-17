## Description:

Cat Life Status Query Skill. Triggers when you send /cat command or ask about your cat. The skill calls the underlying LLM model to interact with you as a sassy and funny cat, telling you what the cat is doing and thinking. For OpenClaw deployment environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tony888880lang](https://clawhub.ai/user/tony888880lang)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to ask for a short, humorous status update from a configured virtual cat persona. The skill builds a cat-character prompt, calls the selected LLM provider, and returns the cat's current activity, thoughts, and mood.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom API endpoint can receive the configured LLM API key and prompt data.

Mitigation: Leave base_url empty unless the endpoint is trusted and expected to receive both credentials and prompts.

Risk: Provider API keys are required for normal use.

Mitigation: Use scoped or low-quota API keys and review the selected provider configuration before running the skill.

Risk: The skill creates a local cat-profile cache file.

Mitigation: Account for the local .cat_cache.json file when reviewing workspace persistence or cleanup requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tony888880lang/skills/openclaw-cat)
- [OpenAI-compatible API base URL example](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text response with console status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are generated through the configured LLM provider and are intended to be short, humorous cat-persona status updates.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
