## Description:

Lightweight anti-infinite-loop guard for LLM agents that detects repeated or collapsing behavior and returns healing, pause, or abort directives with zero required runtime dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to monitor LLM agent loops, check plans before execution, and receive structured intervention directives when an agent begins repeating actions, drifting from intent, or entering a cycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Observed agent text can be promoted into a returned system_message.

Mitigation: Review host integration so returned system_message values are separated, sanitized, or downgraded before they affect privileged prompts.

Risk: Raw loop action samples may be stored locally under ~/.anti_loop/loops.json by default.

Mitigation: Clear, relocate, or patch local LoopDNA storage when the agent handles sensitive prompts, customer data, credentials, or powerful tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kofna3369/skills/morgana-anti-infinite-loop-v2)
- [PyPI Package](https://pypi.org/project/anti-loop/)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Python code examples with JSON-like directive objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime directives may include heal, pause, or abort actions; the CLI can emit stats as JSON.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
