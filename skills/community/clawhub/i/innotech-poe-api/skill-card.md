## Description:

Poe Api enables OpenClaw agents to route prompts through the Poe API with task-based model selection across text, search, image, video, and audio workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwcalvin](https://clawhub.ai/user/nwcalvin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to call Poe-hosted models from OpenClaw workflows, automatically selecting models for coding, design, analysis, web search, and media-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, attachments, code, documents, and search queries are sent to Poe and may be processed by downstream model providers.

Mitigation: Do not send secrets or regulated data unless the deployment environment permits it, and review provider data-handling requirements before use.

Risk: The Poe API key can be exposed if it is hardcoded, logged, or committed.

Mitigation: Set POE_API_KEY only through the runtime environment or a secrets manager and rotate the key if exposure is suspected.

Risk: The Python dependency is declared as openai>=1.0.0, which can admit unreviewed future dependency versions.

Mitigation: Pin dependencies in a lockfile before production deployment and update them through normal dependency review.

Risk: External model responses may include incorrect guidance, code, configuration, or shell commands.

Mitigation: Review generated outputs before using them in workflows, especially before executing code or commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nwcalvin/skills/innotech-poe-api)
- [Publisher profile](https://clawhub.ai/user/nwcalvin)
- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [Model selection guide](artifact/MODEL_SELECTION_GUIDE.md)
- [Poe client implementation](artifact/scripts/poe_client.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionary responses and strings from Poe API calls, typically containing plain text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POE_API_KEY and sends prompts to Poe-hosted external models.]

## Skill Version(s):

1.0.0 (source: artifact/skill.json, artifact/SKILL.md, artifact/CHANGELOG.md, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
