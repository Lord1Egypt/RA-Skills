## Description: <br>
Adds slides to an existing PPTX by cloning a selected slide template and replacing text while preserving the deck's original styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to add content, section, or cover slides to an existing PowerPoint deck while keeping the original visual style. It is intended for extending existing presentations rather than creating new decks from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-provided PPTX and writes a new PPTX to the requested output path. <br>
Mitigation: Run it only on presentations intended for processing and choose a separate output filename when the original deck should be preserved. <br>
Risk: Inserted content can overflow, be truncated, or leave blank areas when the selected template slide does not match the supplied content structure. <br>
Mitigation: Select a template slide with enough matching text regions and review the generated deck before sharing or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/pptx-add-slides) <br>
- [Publisher profile](https://clawhub.ai/user/tuobadaidai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [PPTX output files plus Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes a new PPTX to the user-selected output path and accepts slide content as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
