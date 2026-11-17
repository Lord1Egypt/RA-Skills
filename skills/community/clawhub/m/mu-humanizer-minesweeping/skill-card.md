## Description:

AI味消除剂+书面禁忌扫雷：通过场景锚定、风格校准、证据守恒改写、独立保真审计与书面禁忌扫雷，帮助写出准确、自然、得体的文字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, marketers, and communications teams use this skill to polish Chinese, English, or mixed-language natural-language text while preserving facts, numbers, scope, qualifiers, and attribution. It can also scan Chinese written-language risk expressions and flag high-sensitivity wording for human review instead of automatic replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat writing-risk findings as legal, policy, or final publication approval.

Mitigation: Present findings as editing guidance and require human review for legal, policy, high-sensitivity, or final-publication decisions.

Risk: Private company, team, or personal rules could be exposed if stored inside the repository without exclusion.

Mitigation: Keep private rules outside the public package or add a .gitignore entry for rules/ before use.

Risk: Rule-based scanning can miss uncoded risks or produce false positives, especially outside the covered Chinese written-risk mapping.

Mitigation: Use the scan as a prompt for editorial review and route English written-risk or high-sensitivity content to qualified human reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-humanizer-minesweeping)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Chinese AI expression patterns](references/zh-patterns.md)
- [English AI expression patterns](references/en-patterns.md)
- [AI argument tic patterns](references/ai-tics.md)
- [Thresholds and preservation rules](references/thresholds.md)
- [Edit policy and review gates](references/edit-policy.md)
- [Fidelity audit rules](references/fidelity-audit.md)
- [Written-taboo risk rules](references/written-taboo-rules.md)
- [Custom rules template](references/custom-rules-template.yaml)
- [Third-party reference notice](THIRD_PARTY_NOTICES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style report with revised text, per-item diffs, benefit notes, anchor sources, fidelity audit results, untreated signals, and written-risk findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not write back to source files; callers must confirm before applying edits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
