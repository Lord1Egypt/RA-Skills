## Description:

Use when the user talks with memes, stickers, reaction images, or wants a more natural image-meme chat style. Also use when deciding whether to interpret an inbound image as a meme vs perform literal image analysis, and when selecting or organizing a meme library for lightweight visual replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ave-nue](https://clawhub.ai/user/ave-nue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Meme Master to interpret meme, sticker, and reaction-image exchanges by social meaning, choose restrained context-aware meme replies, and maintain a small opt-in meme library when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved or passively collected meme libraries may include private, identifying, sensitive, or context-bound images.

Mitigation: Require explicit opt-in before saving or passive collection, save only reusable non-sensitive memes, and periodically review or delete <workspace>/memes/ and meme-index.md.

Risk: Meme replies can feel dismissive in serious, urgent, technical, or vulnerable conversations.

Mitigation: Use text-only responses in serious or ambiguous contexts, avoid mocking memes for sensitive personal topics, and never let meme use replace substantive help.

Risk: A casual meme interpretation could be inappropriate when the user needs OCR, exact visual details, or image troubleshooting.

Mitigation: Switch to explicit image analysis when requested or when the task depends on precise visual details, and distinguish certainty from uncertainty.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ave-nue/skills/meme-master)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Natural-language chat responses and Markdown guidance for optional meme library and meme-index maintenance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend workspace meme library organization only when meme saving is allowed by user or operator policy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
