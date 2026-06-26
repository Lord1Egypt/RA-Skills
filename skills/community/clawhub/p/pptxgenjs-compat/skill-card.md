## Description: <br>
This skill helps developers create PowerPoint-compatible PPTX files with pptxgenjs by applying safe API patterns, post-processing known pptxgenjs defects, and verifying compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaodongcheng](https://clawhub.ai/user/yaodongcheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when generating or repairing PPTX files with pptxgenjs so the resulting presentations are less likely to trigger PowerPoint repair dialogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled fixer rewrites PPTX packages and can overwrite the input file when no output path is provided. <br>
Mitigation: Run it with a separate output filename or on a backup copy of the presentation. <br>
Risk: The fixer may remove notes-related PPTX parts, which can affect presentations that rely on speaker notes. <br>
Mitigation: Preserve the original file and inspect notes-sensitive presentations after repair. <br>
Risk: Compatibility fixes may not fully prove behavior across all PowerPoint, WPS, and LibreOffice versions. <br>
Mitigation: Open the repaired PPTX in the target presentation software and check for repair dialogs before distribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yaodongcheng/pptxgenjs-compat) <br>
- [pptxgenjs compatibility pitfalls](references/pptxgenjs-pitfalls.md) <br>
- [PptxGenJS Issue #1449 - Needs Repair Errors](https://github.com/gitbrent/PptxGenJS/issues/1449) <br>
- [pptxgenjs needs-repair documentation](https://gitbrent.github.io/PptxGenJS/docs/needs-repair-errors/) <br>
- [OOXML Standard - ECMA-376](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and a Python fixer that rewrites PPTX packages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a repaired PPTX file when the bundled fixer is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
