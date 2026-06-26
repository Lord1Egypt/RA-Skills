## Description: <br>
Converts HTML slide decks, especially frontend-slides output, into editable PowerPoint (PPTX) files while preserving slide structure, text, lists, images, and basic styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to convert local HTML presentation files into editable PPTX decks, including batch-style workflows where generated HTML slides need to become PowerPoint files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation describes prompt-generation and virtual-environment behavior that is not supported by the reviewed converter entry point. <br>
Mitigation: Use the local Python converter on explicitly chosen HTML files and verify the available entry point before automating workflows. <br>
Risk: Dependency hygiene issues may cause behavior to change across environments. <br>
Mitigation: Pin and review dependencies before shared or production use, then test conversion results with representative slide decks. <br>
Risk: The converter parses local HTML and writes PPTX files, so unexpected input can produce incomplete or inaccurate slides. <br>
Mitigation: Run it on trusted or reviewed HTML inputs and inspect generated PPTX files before distributing them. <br>


## Reference(s): <br>
- [ClawHub release page for html2pptx](https://clawhub.ai/liberalchang/html2pptx) <br>
- [Publisher profile: liberalchang](https://clawhub.ai/user/liberalchang) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PPTX files with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against explicit input HTML files and writes a PPTX output path.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
