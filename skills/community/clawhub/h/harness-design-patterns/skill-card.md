## Description:

A guidance-only knowledge base for agent harness architecture design, including context handoff, multi-agent coordination, and hook system patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to choose architecture patterns for long-running agent workflows, including handoff documents, compaction memory extraction, denial tracking, delegation modes, adaptive complexity, and hook profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hook and memory patterns may be implemented with insufficient safeguards around permissions, persistence, transcript access, or copied snippets.

Mitigation: Treat the content as architecture reference material; require explicit opt-in, per-project or per-session isolation, secret and personal-data redaction, restrictive file permissions, retention cleanup, validated transcript paths, and secure temporary files before implementation.

Risk: Permission-bypass guidance can reduce user or policy control if used outside a controlled setting.

Mitigation: Avoid permission-bypass mode except inside a deliberately isolated evaluation sandbox.

## Reference(s):

- [Pattern 2: Handoff Documents](references/02-handoff.md)
- [Pattern 6: Atomic File Writes](references/06-atomic-write.md)
- [Pattern 8: Compaction Memory Extraction](references/08-compaction-extract.md)
- [Pattern 9: Denial Circuit Breaker](references/09-denial-tracking.md)
- [Pattern 10: Memory Consolidation](references/10-memory-consolidation.md)
- [Pattern 11: Hook Pair Bracket](references/11-hook-bracket.md)
- [Pattern 12: Component-Scoped Hooks](references/12-scoped-hooks.md)
- [Pattern 14: Delegation Modes](references/14-delegation-modes.md)
- [Pattern 16: Adaptive Complexity Scoring](references/16-adaptive-complexity.md)
- [Pattern 18: Hook Runtime Profiles](references/18-hook-profiles.md)
- [Distillation Methodology](references/distillation-methodology.md)
- [Prompt Hardening Integration](references/prompt-hardening-integration.md)
- [Skill Quality Pipeline Integration](references/quality-pipeline-integration.md)
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Agentic Harness Patterns Skill](https://github.com/keli-wen/agentic-harness-patterns-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, implementation steps, shell snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; it does not bundle executable scripts.]

## Skill Version(s):

1.1.0 (source: server release evidence and metadata.json; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
