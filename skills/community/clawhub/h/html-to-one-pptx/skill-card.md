## Description: <br>
Convert any HTML file or design into a pixel-faithful PowerPoint (.pptx) slide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panhongwei](https://clawhub.ai/user/panhongwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to convert one or more HTML design files into PowerPoint slides while preserving layout, colors, text, shapes, and chart structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads user-provided HTML and creates temporary project files before executing generated local scripts. <br>
Mitigation: Keep work in a dedicated project folder and review generated files before execution, especially when the HTML is untrusted. <br>
Risk: Generated gen.js controls the final PPTX output and may be incorrect if the HTML parsing or chart extraction is incomplete. <br>
Mitigation: Review the generated gen.js and intermediate parse, color, and chart files before running Node to create the presentation. <br>


## Reference(s): <br>
- [PptxGenJS Tutorial](artifact/pptxgenjs.md) <br>
- [ClawHub skill page](https://clawhub.ai/panhongwei/html-to-one-pptx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local Python and Node command snippets, generated JavaScript, intermediate markdown/JSON files, and PPTX file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary parse, color, chart, and generation files before writing one or more .pptx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
