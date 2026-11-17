## Description:

Operator Humanizer helps agents detect AI-writing patterns, score statistical signals, and revise drafts into more human-sounding prose for posts, articles, emails, marketing copy, newsletters, scripts, and similar text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevjade](https://clawhub.ai/user/kevjade)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and writing teams use this skill to review drafts for AI-like vocabulary, structure, and rhythm, then produce rewrites or suggestions that sound less robotic. It supports content review and revision across common written formats while requiring human review for authorship, consent, and disclosure-sensitive contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used for detector-evasive humanization or policy evasion.

Mitigation: Use it for legitimate editing and quality review, not to bypass disclosure, authorship, or platform rules.

Risk: The skill includes guidance for writing like a specific person, which can enable impersonation.

Mitigation: Use specific-person voice adaptation only with consent and clear disclosure; do not use it to impersonate real people.

Risk: The skill references hidden Unicode spacing in examples.

Mitigation: Inspect generated output for hidden Unicode characters before publishing or submitting it.

Risk: AI-detection scores and claims are heuristic and may be wrong.

Mitigation: Treat scores as rough style signals and require human editorial review before relying on them.

## Reference(s):

- [The 24 AI Writing Patterns](references/patterns.md)
- [Phrases to Remove](references/phrases.md)
- [Structural Patterns to Avoid](references/structures.md)
- [AI Vocabulary Database](references/vocabulary.md)
- [Statistical Signals of AI Writing](references/statistical-signals.md)
- [Personality Injection Guide](references/personality-injection.md)
- [Humanization Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown prose with optional JSON analysis from the local CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-likelihood scores, pattern flags, and humanization suggestions; scores are heuristic.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
