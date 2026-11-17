## Description:

Provides an OpenClaw-callable MiniMax-M2.7/OpenSpace LLM wrapper for chat, long-form writing, text analysis, and code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhuiguo](https://clawhub.ai/user/linhuiguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to call MiniMax-M2.7 through OpenSpace for conversational responses, article drafting, text analysis, and code generation from a command line or Python workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published documentation contains a real-looking API key.

Mitigation: Treat the documented key as compromised, rotate or revoke it, remove it from published material, and use a user-provided secret stored outside documentation.

Risk: The skill installs an unpinned executable dependency.

Mitigation: Install a trusted, pinned version of openspace in an isolated environment before deploying the skill.

Risk: Prompts and files sent through the skill may be processed by external MiniMax/OpenSpace services.

Mitigation: Do not send confidential or regulated data unless that processing path is approved for the intended use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linhuiguo/skills/openspace-llm-xiaowei)
- [HKUDS OpenSpace project](https://github.com/HKUDS/OpenSpace)
- [MiniMax API base](https://api.minimax.chat/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-formatted CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the configured MiniMax/OpenSpace model, API key, network proxy, timeout, and retry settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
