## Description:

Pre-release code review that converges - parallel review agents sized to the diff, findings validated against evidence in a run ledger, fixes on approval, then re-reviews its own fixes until a round warrants no edits. Run on /polish-new.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review code changes before release, validate findings against evidence, and converge on approved fixes through repeated review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phase 1 may repair unrelated pre-existing failures before the approval gate described for fixes.

Mitigation: Require approval for Phase 1 repairs, including pre-existing failures outside the requested changes. Use an isolated checkout and inspect all edits before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenequm/skills/polish-new)
- [Project homepage](https://github.com/tenequm/skills/tree/main/skills/polish-new)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown review findings and run ledger, with approved code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are tied to evidence; fixes are re-reviewed until a round warrants no edits.]

## Skill Version(s):

0.1.3 (source: frontmatter, changelog, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
