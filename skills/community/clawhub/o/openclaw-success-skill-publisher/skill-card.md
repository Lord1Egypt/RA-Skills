## Description:

Captures successful OpenClaw interactions, extracts an optimized reusable execution path, generates a reusable skill, and prepares ClawHub publishing plus bilingual sharing drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmywangjimmy](https://clawhub.ai/user/jimmywangjimmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to convert a completed OpenClaw success case into reusable skill assets, an optimal-path summary, publishing payloads, and bilingual distribution copy. It is intended for productizing proven workflows after human review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing flow can send generated skill bundles, share drafts, and tokens to configured endpoints.

Mitigation: Use dry-run first, inspect generated artifacts, require explicit approval for real publishing, and use narrowly scoped tokens with trusted HTTPS endpoints.

Risk: Untrusted success-case text can become operative skill instructions or public sharing content.

Mitigation: Review generated_skill/SKILL.md and share_payloads before publishing, scan for sensitive data, and avoid automatic publish/share without human approval.

## Reference(s):

- [OpenClaw Success Skill Publisher on ClawHub](https://clawhub.ai/jimmywangjimmy/skills/openclaw-success-skill-publisher)
- [Publisher Profile](https://clawhub.ai/user/jimmywangjimmy)
- [Publish Contract](references/publish_contract.md)
- [ClawHub API Endpoint](https://api.clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON reports, generated skill files, ZIP bundles, and optional HTTP publish/share payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode can generate local drafts without remote publishing; real publishing requires configured endpoints and explicit approval.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
