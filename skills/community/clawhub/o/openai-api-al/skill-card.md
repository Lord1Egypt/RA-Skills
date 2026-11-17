## Description:

Access OpenAI API for text generation, reasoning, embeddings, images, audio, and moderation using cost-effective, safe, and model-appropriate calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose OpenAI API tools, models, parameters, and workflows for generation, embeddings, image, audio, moderation, and structured extraction tasks while controlling cost and security risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenAI API calls can incur billed usage if an agent uses chat, responses, embeddings, images, audio, uploads, fine-tuning, or vector-store operations.

Mitigation: Set spend limits, require clear user intent before broad openai_request operations, cap output tokens, batch and cache embeddings, and review reported usage.

Risk: Sensitive documents, secrets, or regulated personal data could be sent to an external API if used without review.

Mitigation: Review sensitive documents before embedding or sending them, avoid secrets and regulated personal data unless approved, and never expose OPENAI_API_KEY or authorization headers.

Risk: Model output and retrieved documents can contain untrusted instructions or unsafe content.

Mitigation: Treat generated output and documents as untrusted, moderate untrusted input when appropriate, and avoid executing returned code, commands, or URLs blindly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/skills/openai-api-al)
- [OpenAI API reference](https://platform.openai.com/docs/api-reference)
- [README](README.md)
- [Models reference](reference/models.md)
- [Endpoints reference](reference/endpoints.md)
- [Best practices reference](reference/best-practices.md)
- [Failure cases](tests/failure-cases.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration, shell commands]

**Output Format:** [Markdown guidance with checklists, JSON examples, and operational recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cost-control, model-selection, moderation, error-handling, and secret-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
