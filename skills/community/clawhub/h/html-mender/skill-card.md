## Description:

HTML Mender turns local or saved HTML deck pages into browser-editable copies for visual text, image, and layout fixes, then exports clean HTML patches back to the source baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaoyupku](https://clawhub.ai/user/wuhaoyupku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to make small visual edits to local or saved HTML presentations without regenerating the entire page. It helps an agent prepare an editable HTML copy, guide browser-based edits, and preserve the clean source-oriented export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill on live or authenticated webpages is outside its intended local-file scope.

Mitigation: Use it only with local or saved HTML files that the user chooses; ask for a saved local HTML copy for live or authenticated content.

Risk: Generated editable or exported HTML can lose styling or media references if separated from relative assets.

Mitigation: Keep editable and exported HTML next to the original asset folders when the source uses relative CSS, images, or other files.

Risk: Unsaved browser edits can be lost because local draft saving is disabled.

Mitigation: Use the editor download action to save the clean HTML result before refreshing or closing the page.

## Reference(s):

- [HTML Mender ClawHub Listing](https://clawhub.ai/wuhaoyupku/skills/html-mender)
- [HTML Mender Homepage](https://github.com/wuhaoyupku/html-mender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; the generated editable HTML should stay next to the original HTML assets.]

## Skill Version(s):

0.1.17 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
