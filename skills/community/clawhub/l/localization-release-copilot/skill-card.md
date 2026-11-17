## Description:

Shadow-mode copilot for localization / translation release operations. Given a source draft and its target-language version(s), it locks terminology, machine-checks numbers and proper nouns, preserves source attributions, flags structure loss, and produces a reviewable diff preview — without rewriting the translation. Designed for editorial long-form ZH↔EN localization; SaaS locale-file features (.po / placeholders / plurals) are flagged as pending until real samples exist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Editorial and localization teams can use this skill to review a finished source draft against one or more translations before publication. It checks long-form ZH↔EN content for terminology, numbers, proper nouns, attributions, and claim-level structure loss, then produces a human-reviewable preview without editing either text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has file-writing capability, so unintended paths could be changed during use.

Mitigation: Review the requested file operations and use host permissions that limit writes to intended review outputs.

Risk: A potential release command could conflict with the user's intended publishing workflow.

Mitigation: Inspect the command and its effects before execution, and keep publication under human control.

Risk: The security inspection was partial because two referenced paths were missing from the bundle.

Mitigation: Check the referenced paths and review any available content before installing or relying on those files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haiyangchenbj/skills/localization-release-copilot)
- [Terminology & Release Checklist](artifact/references/terminology-checklist.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Analysis]

**Output Format:** [JSON extraction and glossary-compliance data, plus Markdown diff and review preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only; does not rewrite the source or target. SaaS locale-file checks are pending real samples.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
