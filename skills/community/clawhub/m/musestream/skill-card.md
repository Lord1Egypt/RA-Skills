## Description:

AI-Music-Stream helps an agent turn text prompts or user context into continuous browser-playable AI music streams, saving generated tracks and metadata to a local library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asriverwang](https://clawhub.ai/user/asriverwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to create and share AI-generated music streams from prompts, mood, weather, activity, or other context, then browse generated tracks in a local library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web server can expose paid music generation controls and saved library data without built-in access control.

Mitigation: Keep the server bound to localhost by default; before sharing links or exposing the port, add authentication, rate limits, HTTPS proxying, and firewall restrictions.

Risk: Continuous auto-queue behavior can continue requesting songs and consuming provider credits while a player window remains active.

Mitigation: Stop the stream or close the player when listening ends, and monitor provider API usage when generating long sessions.

Risk: Prompts, metadata, audio files, and provider credentials are stored or used locally.

Mitigation: Protect the configuration and output directory, avoid committing API keys, and review saved library contents before sharing the machine or directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asriverwang/skills/musestream)
- [Sonauto](https://sonauto.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands, JSON configuration examples, and local HTTP endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shareable player URLs, setup steps, prompt guidance, and local server endpoint usage.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
