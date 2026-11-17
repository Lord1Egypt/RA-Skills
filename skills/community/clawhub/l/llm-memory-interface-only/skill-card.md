## Description:

LLM Memory Integration is an interface-only package that defines Memory, Search, and Vector interfaces while leaving implementations to a separate package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkzs2007](https://clawhub.ai/user/xkzs2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give agents stable memory, search, and vector interface contracts without bundling storage, network, or embedding implementations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public artifact only defines interfaces; a separate private implementation package may add network, storage, credential, or memory behavior that is outside this artifact.

Mitigation: Review and scan any separate implementation package before installing or using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xkzs2007/skills/llm-memory-interface-only)
- [ClawHub package homepage metadata](https://clawhub.ai/skill/llm-memory-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python interface examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interface-only output; no runtime dependencies, required environment variables, network access, command execution, or persistence are included in this artifact.]

## Skill Version(s):

9.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
