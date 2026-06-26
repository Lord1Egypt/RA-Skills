## Description: <br>
Improvement Learner evaluates agent skill quality, tracks score changes, and can run guarded self-improvement loops for SKILL.md structure and supporting files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-skill maintainers use this skill to score skill quality across documented dimensions, diagnose weak checklist areas, track progress, and apply iterative improvements with Pareto-front regression checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill can modify the selected skill directory and create best-effort git commits. <br>
Mitigation: Run it on a version-controlled copy of the intended skill, inspect diffs and commits, and keep backups before relying on generated changes. <br>
Risk: Default evaluation can send SKILL.md content through Claude for LLM-based judging. <br>
Mitigation: Use --mock when skill content should not be sent to Claude, accepting the lower-fidelity regex fallback described by the skill. <br>
Risk: The skill can run tests for the target skill and should not be treated as a read-only scorer. <br>
Mitigation: Use it only when active improvement behavior is acceptable, and sandbox untrusted skills before evaluation or self-improvement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/improvement-learner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON score reports, Markdown progress reports, and proposed or applied skill-file changes with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Evaluation outputs include per-dimension scores and checklist details; self-improvement outputs may include iteration decisions, diffs, memory statistics, and final scores.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
