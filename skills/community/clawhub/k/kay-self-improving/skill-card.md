## Description:

A universal self-improving agent that learns from all skill experiences, uses semantic, episodic, and working memory to evolve the codebase, and supports hooks-based self-correction on completion or error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to capture lessons from agent work, turn repeated experiences into reusable patterns, and propose updates to skill guidance. It supports manual self-improvement triggers and optional hooks for session, command, and error logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain session-derived data across work sessions.

Mitigation: Install only when cross-session learning is intended, and avoid storing sensitive tool inputs, outputs, or user data in memory files.

Risk: Global hooks can log raw tool inputs and outputs.

Mitigation: Keep automatic hooks disabled for sensitive work and enable them only after reviewing what each hook records.

Risk: Memory-derived patterns can propose or make changes to skill instructions.

Mitigation: Require reviewable diffs and human approval before applying changes to installed skills.

## Reference(s):

- [Appendix](references/appendix.md)
- [SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/html/2601.02553v1)
- [A Survey on the Memory Mechanism of Large Language Model Agents](https://dl.acm.org/doi/10.1145/3748302)
- [Lifelong Learning of LLM based Agents](https://arxiv.org/html/2501.07278v1)
- [Evo-Memory: DeepMind's Benchmark](https://shothota.medium.com/evo-memory-deepminds-new-benchmark)
- [Let's Build a Self-Improving AI Agent](https://medium.com/@nomannayeem/lets-build-a-self-improving-ai-agent-that-learns-from-your-feedback-722d2ce9c2d9)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to memory files and skill instructions; review changes before applying.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
