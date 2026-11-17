## Description:

Make Html guides agents to produce polished, self-contained HTML artifacts for substantial human-facing deliverables instead of defaulting to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuller-stack-dev](https://clawhub.ai/user/fuller-stack-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, reviewers, and operators use this skill when an agent response should become a readable, navigable, shareable HTML artifact such as a report, plan, review, dashboard, diagram, deck, prototype, or editor. It is intended for substantial deliverables where layout, visual hierarchy, validation, interactivity, or publishing support improves comprehension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted sharing can expose sensitive content because a secret Gist is unlisted rather than private.

Mitigation: Before using the opt-in Pagedrop/Gist publishing workflow, review the generated HTML for secrets, private data, source excerpts, embedded metadata, and hidden content.

Risk: The skill changes the agent's default posture toward HTML for substantial deliverables.

Mitigation: Install it only when polished HTML should be the normal output for larger work, and honor explicit requests for Markdown, JSON, plain text, code-only snippets, or brief chat replies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuller-stack-dev/skills/make-html)
- [Make HTML Skill Source](artifact/SKILL.md)
- [Recognition](artifact/references/recognition.md)
- [Artifact Patterns](artifact/references/artifact-patterns.md)
- [Interaction Patterns](artifact/references/interaction-patterns.md)
- [Visual Quality](artifact/references/visual-quality.md)
- [Validation](artifact/references/validation.md)
- [Sharing HTML Artifacts](artifact/references/sharing.md)
- [Pagedrop](https://pagedrop.ai)
- [Pagedrop GitHub Repository](https://github.com/Martian-Engineering/pagedrop)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [Self-contained HTML files, or a fenced HTML document when file creation is unavailable; optional shell commands are used for validation and opt-in publishing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should work offline by default, include inline CSS and JavaScript when needed, remain responsive on narrow screens, and publish through Pagedrop/Gist only after explicit user request or confirmation.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
