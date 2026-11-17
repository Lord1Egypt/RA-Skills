## Description:

Deterministic verification + reputation scoring for AI sub-agents. Prevents hallucinated success via 4 code gates (files, tests, lint, AST) and a 3-layer pipeline (Structural \u2192 Grounding \u2192 LLM Council) for open-ended tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nefas11](https://clawhub.ai/user/nefas11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to spawn governed sub-agents, independently verify their claimed results, and maintain reputation scores that influence future supervision levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local commands through external CLIs.

Mitigation: Run it in a sandboxed workspace and use trusted task contracts with explicit acceptance criteria.

Risk: HTTP spawn mode can receive authentication tokens.

Mitigation: Do not set GOVERNED_AUTH_TOKEN or AUTH_TOKEN unless the HTTP endpoint is pinned to a known trusted local service.

Risk: Persistent reputation data may be written outside the declared OpenClaw state path.

Mitigation: Set GOVERNED_DB_PATH explicitly to an approved location before use.

## Reference(s):

- [Governed Agents ClawHub Page](https://clawhub.ai/nefas11/skills/governed-agents)
- [Governed Agents Source](https://github.com/Nefas11/governed-agents)
- [README](artifact/README.md)
- [Security Notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate task contracts, verification summaries, council prompts, and configuration guidance for local CLI execution.]

## Skill Version(s):

0.1.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
