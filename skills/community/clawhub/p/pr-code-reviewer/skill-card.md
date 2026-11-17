## Description:

Revisa Pull Requests con reglas de calidad, seguridad y estilo para JavaScript, TypeScript, Node.js, PHP, Python, CSS y HTML, y genera comentarios y resúmenes de revisión en español.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nesquitmx](https://clawhub.ai/user/nesquitmx)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review pull request diffs before merge, with findings grouped by file and severity. It is intended to help identify bugs, security issues, maintainability problems, style concerns, and team-convention violations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce overly strict or project-mismatched review guidance if team conventions are left generic.

Mitigation: Review and customize artifact/references/team-conventions.md before use, including language, severity thresholds, architecture expectations, test coverage, and project-specific rules.

Risk: Example unsafe code snippets in the reference files may look executable when copied outside their review context.

Mitigation: Treat unsafe snippets as examples of patterns the reviewer should detect, not as code to run or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nesquitmx/skills/pr-code-reviewer)
- [README](artifact/README.md)
- [General review rules](artifact/references/general.md)
- [Security review rules](artifact/references/security.md)
- [JavaScript and TypeScript review rules](artifact/references/javascript-typescript.md)
- [Node.js review rules](artifact/references/nodejs.md)
- [PHP review rules](artifact/references/php.md)
- [Python review rules](artifact/references/python.md)
- [CSS and HTML review rules](artifact/references/css-html.md)
- [Team conventions template](artifact/references/team-conventions.md)
- [Review summary template](artifact/assets/review-summary.md)
- [Review comment template](artifact/assets/review-comment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review summaries and inline-style review comments with suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-language output with severity labels for blockers, warnings, suggestions, and nits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
