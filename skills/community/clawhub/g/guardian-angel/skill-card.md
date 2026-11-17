## Description:

Guardian Angel gives AI agents a moral conscience rooted in Thomistic virtue ethics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo3linbeck](https://clawhub.ai/user/leo3linbeck)

### License/Terms of Use:


## Use Case:

External users and agent developers use Guardian Angel to add a virtue-based review layer for agent actions, especially high-stakes, irreversible, deceptive, or approval-sensitive tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin approval flow is not reliable enough to serve as a strong security boundary for sensitive actions.

Mitigation: Require independent human review for shell commands, config changes, file writes, outbound messages, and scheduled actions before deployment.

Risk: An agent could bypass or self-approve sensitive actions if relying only on the current plugin enforcement.

Mitigation: Treat Guardian Angel as advisory defense-in-depth until approval binding and human-confirmation controls are verified in the target runtime.

Risk: Hook ordering cannot be fully verified when the runtime does not expose hook introspection.

Mitigation: Review installed plugins and runtime hook behavior so later hooks cannot override Guardian Angel blocks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leo3linbeck/skills/guardian-angel)
- [Guardian Angel Plugin Specification](PLUGIN-SPEC.md)
- [Default Configuration](config/defaults.json)
- [Moral Credit Scoring Rubric](references/rubric.md)
- [Category-Based System 1 Rubric](references/category-rubric.md)
- [High-Scrutiny Domains](references/domains.md)
- [Prompt Injection Defense Reference](references/prompt-injection-defense.md)
- [Guardian Angel Secondary Rubric: Reversibility & Commitment](references/reversibility-commitment-rubric.md)
- [Affected Parties Rubric](references/affected-parties-rubric.md)
- [Thomistic Framework for Moral Evaluation](references/thomistic-framework.md)
- [Virtue Ethics Reference](references/virtue-ethics.md)
- [Principle of Double Effect](references/double-effect.md)
- [Pattern Triggers Reference](references/pattern-triggers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript plugin code, JSON configuration, and structured block or escalation messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plugin enforcement may block tool calls or require approval through parameter-bound, time-limited nonces.]

## Skill Version(s):

3.1.2 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
