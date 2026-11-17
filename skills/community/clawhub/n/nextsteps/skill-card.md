## Description:

NextSteps appends context-aware follow-up suggestions after agent responses, surfaces unfinished tasks from local memory, and adapts suggestion count, categories, and format from user feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindulasai](https://clawhub.ai/user/cindulasai)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to keep conversations moving by adding specific, actionable next-step suggestions after responses. It is useful for recurring project work where unfinished topics, format preferences, and suggestion categories should carry across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically append suggestions to most agent responses, which may interfere with workflows that require a strict response format.

Mitigation: Review the preference settings before use and disable suggestions for conversations or environments where output shape must remain fixed.

Risk: The skill keeps persistent local memory about selections, ignored suggestions, inferred preferences, and backlog topics.

Mitigation: Avoid enabling persistence in contexts with private cross-channel information, and review the .nextsteps files periodically for sensitive or unwanted entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cindulasai/skills/nextsteps)
- [Category Taxonomy](artifact/references/CATEGORIES.md)
- [Anti-Pattern Rules](artifact/references/ANTI-PATTERNS.md)
- [Cold-Start Bootstrap Protocol](artifact/references/COLD-START.md)
- [User Customization Protocol](artifact/references/CUSTOMIZATION.md)
- [Security Rules](artifact/references/SECURITY.md)
- [Self-Improvement Engine](artifact/references/SELF-IMPROVE.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or compact text suggestions appended to agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt suggestion count, categories, and format based on user preferences; may maintain local .nextsteps preference, history, and backlog files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
