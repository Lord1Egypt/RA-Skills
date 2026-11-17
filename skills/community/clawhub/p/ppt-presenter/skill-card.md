## Description:

Creates reveal.js HTML presentations with planned slide content, AI-generated whiteboard illustrations, presenter view, and complete word-for-word speaker scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewislulu](https://clawhub.ai/user/lewislulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external presenters, and developers use this skill to turn topics, notes, or Markdown into polished HTML slide decks with structured sections, generated visuals, and readable presenter scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled image-generation helper can write generated image files outside the requested output folder when slide names are path-like.

Mitigation: Use only trusted prompts JSON files and keep slide names to simple filenames containing letters, numbers, dashes, and underscores.

Risk: Image prompts are sent to Google's API, and generated presentations load JavaScript, CSS, and fonts from external CDNs.

Mitigation: Avoid sensitive prompt content, use a restricted Gemini API key, and review or modify the presentation template when external network loading is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lewislulu/skills/ppt-presenter)
- [Google Generative Language API generateContent endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent)
- [reveal.js 5.1.0 CSS CDN](https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, HTML presentation code, JSON image prompts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated presentations use reveal.js presenter notes; optional slide images are produced through a Gemini API helper script.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
