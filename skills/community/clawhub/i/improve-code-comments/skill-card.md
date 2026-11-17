## Description:

Use when auditing, adding, removing, or improving code comments, docstrings, JSDoc/TSDoc, TODO/FIXME/HACK notes, public API comments, inline rationale, stale/comment rot, redundant comments, documentation gaps, or "why not what" comment quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit comment and docstring quality, identify stale or misleading comments, and make focused comment-only improvements that preserve code behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comment-only edits can still create misleading public API contracts or stale rationale if claims are not checked against code.

Mitigation: Verify comment claims against nearby code behavior, signatures, units, fallbacks, side effects, and public contract expectations before applying edits.

Risk: Broad comment rewrite requests can create unnecessary churn or remove useful institutional context.

Mitigation: Audit first, report candidates with file and line evidence, and apply only confirmed or clearly requested comment targets.

Risk: Changing tool directives such as lint suppressions, formatter ignores, coverage pragmas, or generated-code markers can affect build or test behavior.

Mitigation: Preserve tool directives exactly and run the narrow relevant formatter or check when comment syntax can affect validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wufei-png/skills/improve-code-comments)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown audit reports, proposed comment-only code edits, and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve tool directives and avoid code, test, configuration, or external documentation changes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
