## Description: <br>
Designs an engineered loop for medium or large semi-autonomous AI-coding work by decomposing the task into gated sub-loops and emitting a runnable .loop/ runbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design check-driven agent loops for medium or large coding tasks before running implementation work. It produces a reviewable loop design with decision logs, validation gates, and a persisted .loop/ runbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated loop designs and runbooks can contain incorrect or misleading gates if the checks do not actually prove the intended outcome. <br>
Mitigation: Run the supplied linter, complete the fresh-reader checklist, and review each generated gate before using the runbook. <br>
Risk: The skill may propose shell commands or workflows that affect a project, deployment, or privileged environment. <br>
Mitigation: Review commands before approval, use authorized environments only, and keep normal credential and deployment access controls in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/loop-constructor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Loop selection procedure](artifact/references/loop-selection.md) <br>
- [Canonical loop-design shape](artifact/references/loop-design-shape.md) <br>
- [Loop principle map](artifact/references/loop-principle-map.md) <br>
- [Fresh-reader checklist](artifact/assets/fresh-reader-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON loop-design content and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces design artifacts and runbook paths; it does not execute the designed loop.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
