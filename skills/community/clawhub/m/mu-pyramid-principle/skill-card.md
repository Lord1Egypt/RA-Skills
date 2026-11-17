## Description:

A Chinese-first Pyramid Principle coaching skill that diagnoses draft logic, checks MECE structure, selects SCQA openings, and rebuilds text into conclusion-first Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Employees, writers, and business users use this skill to diagnose the structure of reports, proposals, emails, speeches, and meeting notes, then reorganize them into a clearer pyramid argument. It also supports guided coaching for users who have scattered ideas but no finished draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad phrases such as requests to organize thoughts may trigger the skill while working with sensitive drafts.

Mitigation: Invoke the skill explicitly for sensitive material and review the agent context before sharing confidential text.

Risk: The skill can produce logic diagnoses and rewrites that may overstate certainty if source evidence is weak.

Mitigation: Review cited original text, severity labels, and proposed rewrites before using them in business-facing materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-pyramid-principle)
- [Logic diagnosis standards](references/logic-diagnosis.md)
- [Pyramid construction templates](references/pyramid-patterns.md)
- [Logic framework toolkit](references/logic-frameworks.md)
- [Project README](README.md)
- [Landing page](https://muippt.github.io/mu-pyramid-principle/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown with a logic diagnosis report, pyramid tree, SCQA preamble, and polished rewrite.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; supports English input and output when requested.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter and README report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
