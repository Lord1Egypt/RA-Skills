## Description:

Organizes a Markdown vault by grouping notes into semantic topic folders, moving notes after confirmation, and creating or updating MOC.md indexes without changing note contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanli6](https://clawhub.ai/user/wanli6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and note-taking users use this skill to initialize or incrementally maintain a Markdown vault by classifying notes, moving files, and updating map-of-content indexes after reviewing a proposed change list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe file moves or path handling may behave incorrectly for unusual filenames or untrusted vault contents.

Mitigation: Use the skill only on a backed-up or cleanly committed git repository, inspect every proposed move or write before approval, and avoid paths with spaces, shell metacharacters, leading hyphens, or traversal-like names unless safer path handling is applied.

Risk: Semantic classification can place notes in the wrong topic or create misleading MOC links.

Mitigation: Review the full proposed change list, require explicit confirmation before execution, and route ambiguous notes to misc/ with a pending-organization marker instead of forcing a topic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanli6/skills/organize-vault)
- [Skill homepage from frontmatter](https://github.com/wanli6/OrganizeVault)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, proposed file moves, and MOC.md file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes and performs file moves and MOC.md writes only after user confirmation; relies on git for rollback.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
