## Description: <br>
Turn docs, notes, data, logs, screenshots, and code summaries into polished Marp slide decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuller-stack-dev](https://clawhub.ai/user/fuller-stack-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other knowledge workers use this skill to turn notes, reports, logs, data, screenshots, and technical summaries into concise Marp presentation decks with rendered outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slide decks can persist local copies of sensitive source material. <br>
Mitigation: Review output paths and generated files before sharing, storing, or committing them. <br>
Risk: Rendering depends on the npm-distributed Marp CLI. <br>
Mitigation: Review @marp-team/marp-cli as a third-party CLI dependency before installation or use in controlled environments. <br>
Risk: Dense source material can produce slides with cropped or hidden content if the rendered deck is not checked. <br>
Mitigation: Render-check the requested target format and split crowded slides before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuller-stack-dev/marp-slides) <br>
- [Marp](https://marp.app) <br>
- [Output formats](references/output-formats.md) <br>
- [Slide patterns](references/slide-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Marp Markdown source with rendered HTML, PDF, PPTX, notes text, PNG, or JPEG outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps the editable *.slides.md source when rendering other formats; default rendered output is HTML.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
