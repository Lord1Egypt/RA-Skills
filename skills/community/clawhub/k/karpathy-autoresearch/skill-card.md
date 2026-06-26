## Description: <br>
Autonomously optimize any OpenClaw skill by running it repeatedly, scoring outputs against binary evals, mutating the prompt, and keeping improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alannjaf](https://clawhub.ai/user/Alannjaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to run repeated mutation, evaluation, and keep-or-revert loops against a measurable prompt, configuration, strategy, or template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit files and change repository history while running optimization experiments. <br>
Mitigation: Run it in a disposable clone or clean branch, name the exact mutable file, and review diffs before keeping or publishing results. <br>
Risk: The skill can run shell evaluation commands supplied for scoring. <br>
Mitigation: Use only evaluator commands you wrote or trust, and keep secrets and production configuration out of the workdir. <br>
Risk: Autonomous prompt or strategy changes can optimize for a narrow evaluator and introduce misleading or brittle guidance. <br>
Mitigation: Review accepted mutations manually and validate results against representative holdout cases before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Alannjaf/karpathy-autoresearch) <br>
- [Gold Trading Strategy Optimization Case Study](references/gold-results.md) <br>
- [YouTube Shorts Script Optimization Case Study](references/youtube-results.md) <br>
- [Karpathy Autoresearch Pattern](https://x.com/karpathy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and experiment summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write files, run evaluator commands, create git commits, revert unsuccessful mutations, and produce an autoresearch log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
