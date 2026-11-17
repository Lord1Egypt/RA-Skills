## Description:

Edit AI-assisted drafts without flattening the writer's voice, detect named AI-writing patterns without rewriting, or generate deliberately exaggerated AI copy for satire and before-and-after examples. Use when the user wants writing clearer, more direct, more opinionated, or less AI-sounding; asks whether a draft reads as AI; or explicitly requests intentionally bad AI-style copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwithenoch](https://clawhub.ai/user/aiwithenoch)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, marketers, and other external users use this skill to make drafts clearer and less generic while preserving the writer's voice. It can also audit drafts for named AI-writing patterns or generate intentionally exaggerated AI-style copy for satire, teaching, or before-and-after examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger on broad writing-improvement requests even when the user wants a different editorial style.

Mitigation: Use it when the desired outcome is an opinionated human-sounding edit, AI-pattern audit, or intentionally exaggerated AI-style example; choose or request another writing workflow for a different style.

Risk: AI-pattern detection findings could be mistaken for proof that a person used AI.

Mitigation: Treat findings as checkable writing-pattern evidence only; the skill is designed to avoid scoring drafts or claiming AI authorship.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/aiwithenoch/humantoday/tree/main/skills/humantoday)
- [ClawHub skill page](https://clawhub.ai/aiwithenoch/skills/humantoday)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown text with edited drafts, detection findings, or intentionally labeled example copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For edit requests, returns the full edited draft and a short What changed section; for detect requests, names patterns with quoted lines and short fixes.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
