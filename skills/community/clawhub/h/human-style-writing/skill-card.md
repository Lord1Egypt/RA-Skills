## Description:

Routes daily chat and social media writing requests into platform-specific recipes that produce natural Chinese, English, or mixed-language messages, posts, captions, comments, and threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unicorn82](https://clawhub.ai/user/unicorn82)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft or rewrite casual DMs, texts, and social posts so they sound more natural while staying within user-provided facts and platform conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs could be used to impersonate a person or create misleading social content.

Mitigation: Use the skill transparently, keep authorship and intent truthful, and avoid fake experiences or claims.

Risk: The skill is scoped to daily chat and social media, not formal legal, compliance, academic, business, or press writing.

Mitigation: Route formal-domain requests to an appropriate domain-specific skill, or ask the user to choose an on-scope DM/text or social platform.

Risk: Humanization can make added details feel factual even when they were not supplied.

Mitigation: Only add concrete anchors from user-provided facts; ask a short clarification or leave a placeholder when details are missing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unicorn82/skills/human-style-writing)
- [Scenario Router](references/scenario-router.md)
- [Prompt Recipes](references/prompt-recipes.md)
- [Registers & Differences](references/registers.md)
- [AI Tells](references/ai-tells.md)
- [Phrase Blacklist](references/phrase-blacklist.md)
- [Human-likeness QA Checklist](references/human-checklist.md)
- [Few-shot Pack](references/fewshot-pack.md)
- [Language Extension](references/language-extension.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown, depending on whether the response includes variants or change notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional bullets describing what changed; does not produce code, shell commands, configuration, or files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
