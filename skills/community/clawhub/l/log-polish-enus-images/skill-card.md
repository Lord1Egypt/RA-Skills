## Description:

Polish a technical blog draft into an 1000-1200 word, 4-5 section en-US article, preserve technical terms/code, and generate consistent hero + per-section image prompts when the user asks to polish and translate a blog with images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to turn a draft technical blog into a polished en-US Markdown article with coordinated hero and per-section image prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan describes the implementation as a rough template generator rather than a trustworthy publish-ready editor or actual image generator.

Mitigation: Review the polished article and image prompts before publication, and treat returned image paths as intended filenames unless an image-generation tool actually creates the files.

Risk: The skill reads a configured draft file and writes timestamped Markdown output to the configured output directory.

Mitigation: Install and run it only when those local file reads and writes are acceptable for the selected draft and output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/log-polish-enus-images)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON object with a polished Markdown path, intended image paths, and single-line image prompt strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped output under the configured contentPolished directory and may return intended image filenames when images are not generated.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
