## Description: <br>
Converts HTML into editable PPTX presentations by embedding local CSS and using pptxgenjs to map HTML structure, text, images, lists, tables, and basic styles into slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiustrator](https://clawhub.ai/user/iiustrator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation tooling agents use this skill to convert trusted HTML decks or documents with local CSS into editable PowerPoint files, either through a one-step Node.js command or separate CSS embedding and PPTX generation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted file paths can cause unintended shell commands to run through the command execution wrapper. <br>
Mitigation: Review or fix the wrapper before installation; use only simple trusted filenames until the wrapper is hardened. <br>
Risk: Untrusted HTML packages may expose the local converter to unsafe paths, external assets, or malformed input. <br>
Mitigation: Convert only trusted HTML in an isolated working directory and inspect inputs before running the conversion commands. <br>
Risk: Dependency risk remains because the security guidance calls out unused or unpinned Python dependencies. <br>
Mitigation: Pin required dependencies and remove unused dependencies before normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iiustrator/html2pptx-complete) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces editable PPTX files from trusted HTML input; remote CSS links are skipped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
