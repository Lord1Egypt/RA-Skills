## Description:

Review a diff for method violations: rot to rewrite, translate-only layers, unvouched deps, fancy over brute force. One line per finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajnandan1](https://clawhub.ai/user/rajnandan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review code diffs for simplification-focused method violations, including repeated patching, translate-only layers, unexplained dependencies, over-clever algorithms, and process-heavy ceremony.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally narrow and excludes correctness, security, and performance review.

Mitigation: Use it as a simplification-focused pass and run a separate normal review for correctness, security, and performance.

Risk: Quoted diff text or user text could accidentally include phrases that switch the review mode.

Mitigation: Treat mode changes such as stop ken-review or normal mode as explicit user intent, not as instructions embedded in reviewed code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rajnandan1/skills/ken-review)
- [Project homepage](https://github.com/rajnandan1/ken)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with one-line findings and an optional net summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not apply fixes; use a normal review pass for correctness, security, and performance.]

## Skill Version(s):

1.2.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
