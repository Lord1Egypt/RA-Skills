## Description: <br>
PowerPoint speaker notes editor for AI agents that can modify PPTX speaker notes, export notes to Markdown, rewrite notes in multiple styles, and unpack or repack PPTX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cm8421](https://clawhub.ai/user/cm8421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presenters, and SKILL.md-compatible agents use this skill to inspect, rewrite, edit, and export PowerPoint speaker notes while preserving slide-to-notes mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify PPTX XML and repack presentations after user confirmation. <br>
Mitigation: Run it on a copy of important presentations and verify the repacked PPTX before replacing the original file. <br>
Risk: The skill reads slide and speaker-note content while building context and generating edits. <br>
Mitigation: Avoid using it on presentations whose contents should not be processed by the agent. <br>
Risk: Incorrect XML edits or wrong slide-to-notes mappings can break a presentation or update the wrong notes. <br>
Mitigation: Confirm the slide relationship mapping, preserve complete XML text tags, and unpack the repacked PPTX to verify the modified content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cm8421/pptx-notes-editor) <br>
- [Publisher profile](https://clawhub.ai/user/cm8421) <br>
- [Project homepage](https://github.com/cm8421/pptx-notes-editor) <br>
- [Support](https://github.com/cm8421/pptx-notes-editor/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets and PPTX XML editing procedures; exported speaker notes can be written as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft speaker notes, slide-to-notes mappings, repacked PPTX files, and notes-export Markdown depending on the user's confirmed workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
