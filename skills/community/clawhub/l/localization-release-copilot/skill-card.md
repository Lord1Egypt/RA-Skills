## Description:

Shadow-mode copilot for localization / translation release operations. Given a source draft and its target-language version(s), it locks terminology, machine-checks numbers and proper nouns, preserves source attributions, flags structure loss, and produces a reviewable diff preview — without rewriting the translation. Designed for editorial long-form ZH↔EN localization; SaaS locale-file features (.po / placeholders / plurals) are flagged as pending until real samples exist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Editorial teams and localization reviewers use it before publishing long-form Chinese↔English content to check terminology, numbers, proper nouns, attributions, and claim-level structure. It produces a reviewable diff and checklist while leaving the translation unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis is incomplete: confidence is medium and two local path-like references could not be resolved.

Mitigation: Review the supplied skill files and any unresolved local references before installation.

Risk: The skill has file-writing capability, and a possible release command may not fit every host or workflow.

Mitigation: Check the effects of release actions and grant only the file and host permissions needed for the review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/skills/localization-release-copilot)
- [Terminology and release checklist](artifact/references/terminology-checklist.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [JSON claim extraction and Markdown review diff, glossary checklist, and release gate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only; does not rewrite source or target text.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
