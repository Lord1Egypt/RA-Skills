## Description:

Bidirectional mathematical engine for Borges' Library of Babel that locates text, reads pages at coordinates, and scores pages by Shannon entropy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to locate text in a deterministic Borges-style Library of Babel coordinate system, read pages from coordinates, and analyze page entropy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references Python engine and demo files that are not present, so runtime examples may not work from this package alone.

Mitigation: Confirm required source files are available before relying on the skill for execution; treat this package as documentation plus static codex data.

Risk: Optional user-added passages may be stored in local codex data if that documented behavior is implemented.

Mitigation: Review local storage behavior before use and avoid adding sensitive text to persistent codex data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/library-of-babel)
- [Skill documentation](artifact/SKILL.md)
- [Static codex data](artifact/codex.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic text outputs; the artifact includes static codex data, while referenced Python engine and demo files are absent.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
