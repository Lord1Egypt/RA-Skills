## Description: <br>
OpenClaw Visual turns OpenClaw messages, PhoenixClaw journals, and chat summaries into locally rendered shareable images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goforu](https://clawhub.ai/user/goforu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to convert text, journals, and chat summaries into polished visual cards for sharing in chat and social workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local PhoenixClaw journals or OpenClaw session history and convert private content into shareable images. <br>
Mitigation: Provide exact text when possible, confirm file paths and date ranges before scanning local records, and review generated images before sharing. <br>
Risk: Rendering untrusted HTML or remote image URLs can expose the renderer to unsafe or unexpected content. <br>
Mitigation: Avoid untrusted HTML and image URLs unless rendering is sandboxed, and prefer known local templates with trusted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goforu/openclaw-visual) <br>
- [Template design reference](references/templates.md) <br>
- [Content parsing reference](references/content-parsing.md) <br>
- [Local rendering setup](references/rendering-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON content examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files through HTML/CSS templates and returns render metadata as JSON when the bundled script is run.] <br>

## Skill Version(s): <br>
0.0.1 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
