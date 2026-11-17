## Description:

Multi Agent Pipeline provides a reusable staged workflow pattern for sequential and parallel agent tasks with status tracking, error handling, and progress callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill as a pattern for building multi-step AI workflows such as content generation, data processing, and generate-validate-transform-deliver pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package disclosure mismatch: server security evidence says the inspected code is a provider-specific story app that sends child-related audio and text to external APIs, while the package is labeled as a generic local pipeline skill.

Mitigation: Review artifact behavior against the intended deployment and correct disclosures for ElevenLabs and Mistral use, required API keys, and outbound network access before installation.

Risk: Child-related audio, prompts, generated story content, and cached media can involve sensitive personal data.

Mitigation: Require explicit consent, data minimization, retention controls, and privacy review before processing or storing child-related content.

Risk: Server security evidence reports stored story data exposed without visible authorization controls.

Mitigation: Add authentication, per-record authorization, upload limits, and abuse controls on all routes before deploying the service behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/multi-agent-pipeline)
- [ElevenLabs speech-to-text endpoint referenced by artifact](https://api.elevenlabs.io/v1/speech-to-text)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with Python code examples and source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed token cap; behavior depends on the stage functions or service routes used by the installing agent.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
