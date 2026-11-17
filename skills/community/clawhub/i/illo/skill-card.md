## Description:

illo helps an agent turn concepts, articles, and prompts into original editorial illustrations, explainer diagrams, mini-comics, mascot cutouts, and comparison galleries using bundled character, style, palette, and backend guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, and developers use illo to generate mascot-led editorial artwork for articles, posts, decks, social media, explainers, and transparent compositing assets. The skill guides the agent through routing, prompt construction, backend selection, quality checks, and delivery of generated image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts, reference images, and related image data may be sent to the selected image backend.

Mitigation: Install and use the skill only when that backend data flow is acceptable for the content being illustrated.

Risk: OpenRouter use requires local credential configuration and can create paid image-generation charges.

Mitigation: Have the user run key setup directly, keep API keys out of chat, and require explicit approval before any paid fallback.

Risk: Community character packs can affect prompts and generated outputs.

Mitigation: Review community packs before installing or updating them, and prefer managed or pinned installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmchow/skills/illo)
- [illo homepage](https://illo-skill.com)
- [README](README.md)
- [Backends and transports](references/backends.md)
- [Models](references/models.md)
- [Composition](references/composition.md)
- [Prompt recipe](references/prompt-recipe.md)
- [Quality bar](references/quality-bar.md)
- [Character builder](references/character-builder.md)
- [Community character packs](references/pack-sharing.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated image file paths or attachments, JSONL manifest records, and optional HTML galleries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images may use subscription CLI transports or OpenRouter, and comparison galleries can include model, cost, dimensions, labels, and prompts.]

## Skill Version(s):

0.37.0 (source: frontmatter and server release changelog, released 2026-09-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
