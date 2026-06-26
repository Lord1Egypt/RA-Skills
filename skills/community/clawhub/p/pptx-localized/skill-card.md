## Description: <br>
Helps agents create, read, edit, combine, split, and quality-check PowerPoint .pptx presentations using local scripts and PPTX generation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to work with local PowerPoint files, including extracting content, editing templates, generating new slide decks, converting decks for visual QA, and repacking .pptx files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local unpacking, cleaning, packing, and conversion can change or overwrite presentation files. <br>
Mitigation: Run workflows on copies of important decks and confirm input and output paths before executing file operations. <br>
Risk: Untrusted Office files may expose the agent environment to archive or document-processing risks. <br>
Mitigation: Process untrusted decks only in a sandboxed environment and avoid opening files from unknown sources without additional review. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yinfeihaaaaaaaaaaa/pptx-localized) <br>
- [README.md](artifact/README.md) <br>
- [Editing Presentations](artifact/editing.md) <br>
- [PptxGenJS - Create Presentations from Scratch](artifact/pptxgenjs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated or modified presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local .pptx, unpacked Office XML, PDF, and slide image files depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
