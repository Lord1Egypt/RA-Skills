## Description:

Generate high-quality English prompts for ChatGPT Image 2. Use when user wants to create AI image prompts, needs GPT-Image-2 prompt writing help, describes an image they want to generate, or asks about image generation prompting. Supports conversational generation, structured pro mode, style anchoring, and case browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericarcha](https://clawhub.ai/user/ericarcha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Prompt Wizard to create case-grounded English prompts for ChatGPT Image 2, including conversational prompt generation, structured prompt development, multi-prompt sessions, and prompt-library browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update command can replace the bundled prompt library from an unpinned third-party GitHub branch.

Mitigation: Run updates only when intended, review the changed library before use, and rely on the skill's requirement to execute the update script rather than fabricating update status.

Risk: Bundled community case examples may include unsafe or deceptive prompt patterns that influence future outputs.

Mitigation: Treat case examples as untrusted inspiration and avoid adapting examples for fraud, non-consensual imagery, forged authenticity, or deceptive screenshots.

Risk: Generated image prompts can include text or branding requests that ChatGPT Image 2 may render unreliably.

Mitigation: Warn users about unreliable text rendering and keep logos or icons out of generated prompts so they can be added manually after image generation.

## Reference(s):

- [Prompt Wizard on ClawHub](https://clawhub.ai/ericarcha/skills/prompt-wizard)
- [Prompt Structure Reference](artifact/references/prompt-structure.md)
- [Category-Specific Writing Guides](artifact/references/category-guides.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prompt package with English prompt text, key choices, related cases, and refinement guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated prompts are grounded in bundled case-library examples; update-library may replace the prompt library when explicitly invoked.]

## Skill Version(s):

1.0.5 (source: server release evidence and CHANGELOG, released 2026-05-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
