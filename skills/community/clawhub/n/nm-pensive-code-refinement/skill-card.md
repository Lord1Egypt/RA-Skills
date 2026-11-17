## Description:

Improves code quality across duplication, efficiency, and architectural fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review existing code for duplication, inefficiency, clean-code issues, error handling, and architectural fit, then produce a prioritized, evidence-based refinement plan. It can apply selected fixes when the request explicitly asks for execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the skill may post code review findings to GitHub Discussions without clearly disclosing the side effect or visibility.

Mitigation: Before use, verify the destination and its visibility settings, and confirm that publishing is opt-in and approved.

Risk: The scanner also flags source-derived content being used in executable Python.

Mitigation: Review source-derived code before executing it. Treat the scan as partial because referenced local paths were missing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-code-refinement)
- [Declared project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown findings and refactoring plans, with code edits when execution is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include code locations and evidence; execution scope follows the user's request.]

## Skill Version(s):

1.10.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
