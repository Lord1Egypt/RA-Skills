## Description:

Morgana Anti Infinite Loop V2 Zh is a Chinese-language Python guard for LLM agents that detects repeated or looping behavior and returns heal, pause, or abort directives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers building LLM agents use this skill to monitor agent actions, detect likely infinite loops or intent drift, and recover before repeated tool calls or token use escalate. It is aimed at agent runtimes that need lightweight loop detection with a zero-dependency core and optional Python extras.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heal mode can pass user-derived action or intent text into a system message.

Mitigation: Prefer pause or hard_kill mode for sensitive agents, or change heal handling so observed text is quoted as lower-privilege context.

Risk: LoopDNA can persist raw loop actions locally.

Mitigation: Disable or redirect LoopDNA storage where possible, and avoid passing secrets, private prompts, or raw tool arguments into observe().

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/morgana-anti-infinite-loop-v2-zh)
- [PyPI project](https://pypi.org/project/anti-loop/)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Python dictionaries, JSON-style CLI output, and Markdown documentation with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return heal, pause, or abort directives; optional extras enable additional numerical or multi-agent behavior.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and pyproject.toml report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
