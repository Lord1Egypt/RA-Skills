## Description:

Rewrites AI-sounding academic and serious popular-science prose in English or Chinese while preserving the source's facts and register, and leaves already-natural prose unchanged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, editors, and science communicators use this skill to revise templated serious nonfiction without adding claims, citations, or numbers. It can also report writing signals without rewriting when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rewriting could change a claim, citation, or scholarly qualifier.

Mitigation: Compare the revision with the original and verify facts, citations, and hedging before use.

Risk: Confidential or unpublished drafts may be shared with a separate quality-review agent.

Mitigation: Disable or avoid blind review unless the review agent's data handling is acceptable for the draft.

Risk: The README's unpinned installation command may fetch a different release later.

Mitigation: Install from a pinned, reviewed release source.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vincentjiang06/skills/humanizer-academic)
- [Academic mode guide](artifact/references/academic-pack.md)
- [Popular-science mode guide](artifact/references/popsci-pack.md)
- [Blind review rubric](artifact/references/blind-judge-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Revised prose or unchanged draft; optional change notes or a diagnostic JSON signal report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports academic and popular-science modes in English and Chinese; diagnostic scores do not establish authorship.]

## Skill Version(s):

4.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
