## Description:

Create mobile-first newspaper-style brief images from raw content or existing summaries, either by structuring source material first or rendering prepared summary bullets directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eisonme](https://clawhub.ai/user/eisonme)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn articles, chats, notes, meeting minutes, links, or prepared summaries into mobile-readable newspaper-style brief images. The skill guides the agent to extract titles, highlights, sections, and footer notes before rendering the result as HTML and, when available, PNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes user-provided content into local output files, so untrusted input or output paths can create unintended local artifacts.

Mitigation: Use trusted local input and output paths, and review the generated HTML or PNG before sharing.

Risk: PNG export may launch a local browser, including a browser path supplied through NEWSPAPER_BRIEF_BROWSER.

Mitigation: Leave NEWSPAPER_BRIEF_BROWSER unset unless it points to a trusted Edge or Chrome executable.

Risk: Very long content can exceed the practical limits of single-image browser screenshots.

Mitigation: Shorten content for one image or split the brief into multiple outputs when the generated page is unusually long.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eisonme/skills/newspaper-brief)
- [Example input payload](artifact/examples/ai-interface-sample.json)
- [Renderer script](artifact/scripts/render_newspaper.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell commands; generated files are HTML, optional PNG, and optional normalized JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local input JSON into local output files; PNG export may launch a local Edge or Chrome browser and can crop bottom whitespace when Pillow is available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
