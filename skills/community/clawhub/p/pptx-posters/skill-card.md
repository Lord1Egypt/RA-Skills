## Description: <br>
Generate PowerPoint presentations and academic posters from paper abstracts or full paper content, with automatic layout optimization and citation formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic authors use this skill to turn existing paper content into structured slide-deck or poster outlines, layout recommendations, and manual refinement guidance. It is intended for presentation planning from supplied content, not for writing original research, fabricating figures, or producing submission-ready manuscripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional generated-code path can overwrite an existing *_generator.py file when the chosen output name conflicts with an existing file. <br>
Mitigation: Use a unique output filename or check for an existing generated helper file before enabling generated-code output. <br>
Risk: PDF parsing and direct PPTX creation are limited; the artifact primarily produces outlines and optional helper code. <br>
Mitigation: Validate PDF text extraction before relying on the output, and review or run the generated helper code separately when a real PPTX file is needed. <br>
Risk: Citation formatting, figure placeholders, and academic content structure can be incomplete or misleading if not reviewed. <br>
Mitigation: Manually verify citations, replace placeholders with real figures, and confirm the final slide or poster content against the source paper before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/pptx-posters) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with structured sections, plain-text outlines, and optional Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can provide layout recommendations, design notes, manual checks, and optional generated python-pptx helper code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
