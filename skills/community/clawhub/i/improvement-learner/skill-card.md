## Description:

Improvement Learner evaluates agent skill quality, proposes or applies targeted skill improvements, protects against score regressions with a Pareto front, and tracks score trends over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate an agent skill across quality dimensions, identify where points are lost, run guarded self-improvement loops, and generate progress reports for trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill can run target code, rewrite files, delete and restore directories, and auto-commit changes with insufficient safeguards.

Mitigation: Install and run it only in a disposable workspace or sandbox, keep the target skill under version control, and inspect all diffs before accepting or publishing changes.

Risk: The skill may submit skill contents to an external LLM CLI during default accuracy evaluation.

Mitigation: Use mock mode for local checks when external submission is not approved, and avoid evaluating directories that contain secrets or confidential material.

Risk: The security verdict is suspicious despite no individual risk findings being listed.

Mitigation: Prefer restricted execution and review test execution, file mutation, external LLM calls, and git commit behavior before using the skill on trusted work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/improvement-learner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON score reports, Markdown progress reports, and direct file changes or command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May mutate the target skill directory, create memory or state files, run subprocesses, and call an external LLM judge unless mock mode is used.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
