## Description:

Autonomously optimizes prompts, strategy configurations, and other mutable files by running evaluation loops that score changes and keep only improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alannjaf](https://clawhub.ai/user/alannjaf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to iteratively improve prompts, skill instructions, strategy configs, and other measurable artifacts against a numeric evaluation function. It is intended for optimization workflows where each experiment can be evaluated, kept, reverted, and summarized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimization loop may edit or stage unintended project files.

Mitigation: Run it in a disposable clone or dedicated branch and approve the exact mutable file before starting.

Risk: Evaluation commands can execute arbitrary shell code.

Mitigation: Use only trusted, reviewed eval commands and avoid untrusted eval strings.

Risk: Git commits and reverts can change project history or hide unrelated changes.

Mitigation: Check the worktree before each run and confirm that secrets or unrelated files cannot be staged.

## Reference(s):

- [Gold Trading Strategy Optimization Case Study](references/gold-results.md)
- [YouTube Shorts Script Optimization Case Study](references/youtube-results.md)
- [Karpathy Autoresearch Reference](https://x.com/karpathy)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify files, run evaluation commands, make git commits, revert failed experiments, and produce an experiment summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
