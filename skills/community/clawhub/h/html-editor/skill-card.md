## Description: <br>
Turns a static HTML page into an editable local HTML file with inline text editing, style controls, bilingual UI labels, prompt-based restyling guidance, and clean export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ytisvibecoding](https://clawhub.ai/user/ytisvibecoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to convert static reports, pages, and presentation-style HTML into editable local pages with visual style controls and exportable clean HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When Anthropic or OpenAI API keys are present, the tool can send CSS variable and selector metadata to that provider for semantic labeling. <br>
Mitigation: For private or internal HTML, run without those API key environment variables or block network access before adapting the file. <br>
Risk: The tool modifies local HTML copies and exported pages may not be suitable for sharing without review. <br>
Mitigation: Keep a source copy, avoid bypassing sanity checks unless necessary, and review the generated HTML before publishing or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ytisvibecoding/html-editor) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an editable HTML file from a local static HTML input and can export a cleaned HTML copy after review.] <br>

## Skill Version(s): <br>
1.8.4 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
