## Description:

Build high-quality presentation decks from scratch, covering brainstorming, content writing, visual design, AI image generation, iterative QA, and final delivery with OpenRouter and Nano Banana Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and presentation authors use this skill to turn a topic or source material into a structured presentation workflow, including spec, content, design, image prompts, QA, and final deck assembly. It is suitable for product demos, pitch decks, training materials, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide prompts and deck content may be sent to third-party image APIs such as Ofox or OpenRouter.

Mitigation: Use only approved providers, review their data handling, and avoid confidential, regulated, customer, financial, or unreleased business material unless explicitly approved.

Risk: The artifact claims no external SaaS dependency while its generation path uses external image API endpoints.

Mitigation: Disclose the external provider dependency before use and require users to configure API credentials only after accepting that dependency.

Risk: Generated slide images can contain altered text, unreadable Chinese, prompt leakage, incorrect numbers, or inconsistent styling.

Mitigation: Run the documented per-slide QA process, rerun only affected slides, and use the HTML plus Playwright fallback when text rendering remains unreliable.

Risk: Local execution requires Python dependencies and API credentials.

Mitigation: Run in a virtual environment, pin dependencies before installing python-pptx, and keep API keys in environment variables rather than embedding them in slide files.

## Reference(s):

- [Prompt Writing Guide for Nano Banana Pro](artifact/references/prompt-writing-guide.md)
- [QA Fix Patterns](artifact/references/qa-fix-patterns.md)
- [Spec Review Checklist](artifact/references/spec-review-checklist.md)
- [Writing Principles](artifact/references/writing-principles.md)
- [Example slides JSON](artifact/scripts/slides.example.json)
- [ClawHub skill page](https://clawhub.ai/dizhu/skills/ppt-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON slide configuration, shell commands, and optional generated PPTX/PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate slide JPG files and assemble them into a PPTX when configured with approved image API credentials.]

## Skill Version(s):

1.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
