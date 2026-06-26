## Description: <br>
Generates professional PowerPoint presentations from Markdown, including themed layouts, lists, quotes, code blocks, tables, chart conversion, and automatic closing slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agilight](https://clawhub.ai/user/agilight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to turn structured Markdown or presentation prompts into PowerPoint decks for reports, business summaries, technical briefings, and similar slide-based communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a local Node.js helper and dependency can execute code on the user's machine. <br>
Mitigation: Install and run the skill only in environments where local Node.js execution and the pptxgenjs dependency are acceptable. <br>
Risk: User-selected input and output paths could read unintended Markdown files or overwrite an unexpected PPTX path. <br>
Mitigation: Choose input Markdown files and output destinations deliberately before running the helper. <br>


## Reference(s): <br>
- [AI PPT Generator on ClawHub](https://clawhub.ai/agilight/ppt-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PPTX file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Node.js helper with pptxgenjs to create PPTX files from user-selected Markdown input and output paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
