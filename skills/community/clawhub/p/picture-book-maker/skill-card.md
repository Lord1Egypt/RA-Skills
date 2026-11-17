## Description:

Picture Book Maker helps agents create illustrated picture books from theme planning and story writing through character design, storyboarding, image generation, metadata preparation, and HTML packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lishuailibertine](https://clawhub.ai/user/lishuailibertine)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, and developers use this skill to guide an agent through planning, writing, illustrating, and packaging children's picture books for education, fables, and emotional learning scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book metadata can cause the packer to read local files or contact arbitrary remote image URLs.

Mitigation: Run the packer only on trusted metadata.json files and trusted image sources; avoid arbitrary remote image URLs.

Risk: Generated book.html files should be treated as active web content.

Mitigation: Review generated HTML before sharing or hosting, and keep it in a controlled environment until path containment, URL restrictions, strict image validation, and HTML escaping are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lishuailibertine/skills/picture-book-maker)
- [Story creation template](references/story-template.md)
- [Picture book page guide](references/page-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON metadata and shell command examples; the packaging script produces an HTML picture book file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated books use metadata.json plus page image assets; the packer can embed local or URL-based images into book.html.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
