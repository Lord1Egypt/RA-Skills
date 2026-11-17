## Description:

Ppt Deck Master helps an agent plan, write, design, generate, QA, and deliver high-quality presentation decks from a short user request, using Nano Banana Pro through Ofox or OpenRouter when image generation is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create client-ready product demos, pitch decks, sales materials, training decks, and reports. The workflow guides an agent through brainstorming, deck specification, content writing, visual design, prompt creation, slide image generation, QA repair, and PPTX assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that API-key handling can send a credential to the wrong external provider.

Mitigation: Use a dedicated low-privilege API key, set only one provider credential at a time, and confirm the selected provider before running generation.

Risk: Presentation prompts and content may be sent to external image-generation providers.

Mitigation: Avoid sensitive or confidential presentation content unless the selected provider is approved for that data.

Risk: The workflow runs local scripts and may install dependencies for PPTX assembly.

Mitigation: Review the script before execution and install dependencies in a virtual environment with pinned versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/ppt-deck-master)
- [Brainstorming template](references/Brainstorming模板.md)
- [Prompt guide](references/Prompt指南.md)
- [QA repair mode](references/QA修复模式.md)
- [Writing principles](references/写作原则.md)
- [Self-review checklist](references/自审清单.md)
- [Visual strategy guide](references/视觉策略.md)
- [Ofox image generation endpoint](https://api.ofox.ai/v1/images/generations)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, JSON slide specifications, shell commands, generated JPG slide files, and optional PPTX/PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OFOX_API_KEY or OPENROUTER_API_KEY for external image generation; python-pptx is used only when assembling PPTX files.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
