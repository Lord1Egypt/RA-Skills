## Description:

Prompt Optimizer Toolkit helps agents analyze, improve, template, store, and score LLM prompts using built-in prompt-engineering strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prompt engineers use this skill to evaluate prompt quality, generate improvement suggestions, apply common prompt templates, and maintain a local prompt library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved prompts are stored locally in plaintext JSON when the prompt library is used.

Mitigation: Do not store secrets, credentials, proprietary prompts, or sensitive personal data unless local plaintext retention is acceptable.

Risk: The runtime requirements include an unpinned pytest dependency that is only needed for tests.

Mitigation: Move pytest to development-only dependencies or pin it before installation in managed environments.

Risk: Prompt optimization and scoring are heuristic and can produce incomplete or misleading guidance.

Mitigation: Review optimized prompts and suggestions before using them in production or customer-facing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/prompt-optimizer-toolkit)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON-compatible prompt analysis objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local plaintext JSON prompt-library files when the PromptLibrary helper is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
