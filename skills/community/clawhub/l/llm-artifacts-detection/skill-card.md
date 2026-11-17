## Description:

Detects common LLM coding agent artifacts in codebases. Identifies test quality issues, dead code, over-abstraction, and verbose LLM style patterns. Use when cleaning up AI-generated code or reviewing for agent-introduced cruft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review AI-generated code for maintainability issues, including weak tests, dead code, over-abstraction, and verbose style patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect source files across a codebase and surface sensitive implementation details in review findings.

Mitigation: Run it only on codebases the agent is authorized to inspect and review findings before sharing them externally.

Risk: Heuristic review findings may be misleading if reported without a current file anchor.

Mitigation: Apply the skill's anchor, title, and deduplication gates; verify each [FILE:LINE] finding against the current file contents before acting.

Risk: Suggested cleanup targets may remove code that has runtime uses not visible to static inspection.

Mitigation: Confirm usage with tests, search, or runtime knowledge before deleting or refactoring flagged code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/llm-artifacts-detection)
- [Test Quality Criteria](references/tests-criteria.md)
- [Dead Code Criteria](references/dead-code-criteria.md)
- [Abstraction Criteria](references/abstraction-criteria.md)
- [Style Criteria](references/style-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown findings anchored as [FILE:LINE] ISSUE_TITLE]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review findings are evidence-bound and deduplicated before final output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
