## Description:

Helps agents apply high-performance computing principles when writing or optimizing performance-critical code across batch processing, concurrency, async pipelines, GPU computing, scientific computing, and long-running resumable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanktechnology](https://clawhub.ai/user/tanktechnology)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get performance-oriented coding guidance for optimization, resource-aware parallelism, async pipelines, GPU workloads, and interruption-tolerant long-running jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags under-scoped Docker and repository cleanup advice that could remove containers or files beyond the intended project scope.

Mitigation: Require the agent to list exact containers and repositories first, use dry-run previews such as git clean -nd, and limit Docker removals to disposable project-owned resources.

Risk: The skill can suggest concurrency or lock-free optimization patterns that are difficult to implement correctly without measurement and validation.

Mitigation: Profile before optimizing, validate changes on small workloads first, and require targeted correctness tests or thread-sanitizer checks before scaling or replacing lock-based code.

## Reference(s):

- [High Performance Coding README](artifact/README.md)
- [High Performance Coding Skill Source](artifact/SKILL.md)
- [Evaluation Prompts](artifact/evals/evals.json)
- [ClawHub Skill Page](https://clawhub.ai/tanktechnology/skills/high-performance-coding)
- [Repository URL Listed in README](https://github.com/TankTechnology/high-performance-coding.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include profiling steps, benchmark plans, resource-sizing advice, concurrency patterns, and checkpointing strategies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
