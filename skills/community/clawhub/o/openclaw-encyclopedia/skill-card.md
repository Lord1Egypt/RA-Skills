## Description:

OpenClaw Encyclopedia guides agents through docs-first answers and operational work for OpenClaw behavior, configuration, troubleshooting, automation, security, and runtime diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer OpenClaw-specific questions, plan commands, review configuration, troubleshoot runtime behavior, and maintain a local documentation-and-operations cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace notes may accidentally capture secrets, tokens, private URLs, or confidential access details.

Mitigation: Use .OpenClaw-Encyclopedia as operational memory only, and redact or omit secrets and sensitive access details from cached notes and inventories.

Risk: The cache helper has a bounded fetcher weakness around redirect validation, response size limits, and content-type checks.

Mitigation: Use the helper only for intended docs.openclaw.ai pages and review fetched cache content before relying on it or sharing it.

## Reference(s):

- [OpenClaw Encyclopedia on ClawHub](https://clawhub.ai/kklouzal/skills/openclaw-encyclopedia)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Workflow](references/workflow.md)
- [Cache Layout](references/cache-layout.md)
- [Topic Map](references/topic-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration notes, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace-local .OpenClaw-Encyclopedia cache and notes when used by an agent.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
