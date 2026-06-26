## Description: <br>
Convert a PDF research paper, report, or other document into a multi-slide HTML presentation with a structured outline JSON and summary markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zai-org](https://clawhub.ai/user/zai-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document authors use this skill to turn local or trusted PDF documents into structured HTML slide decks with generated outlines, cropped visuals, and summary markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote PDF download is under-scoped and may fetch untrusted content. <br>
Mitigation: Prefer local PDFs or trusted HTTPS URLs; add URL confirmation, host blocking, size and type limits, and download timeouts before broad use. <br>
Risk: The crop helper can write outside the intended crops folder. <br>
Mitigation: Fix crop filename sanitization and review generated crop paths before using the skill in shared or sensitive workspaces. <br>
Risk: Sensitive documents may be rendered into local page images and reviewed during slide generation. <br>
Mitigation: Avoid sensitive PDFs unless local rendered copies and agent viewing are acceptable under the user's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zai-org/glmv-pdf-to-ppt) <br>
- [GLM-V PDF-to-PPT homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-pdf-to-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML slide files, JSON outline, Markdown summary, cropped image files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an output folder under ppt/<pdf_stem>_<timestamp>/ with slide HTML, outline.json, crops, and summary.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
