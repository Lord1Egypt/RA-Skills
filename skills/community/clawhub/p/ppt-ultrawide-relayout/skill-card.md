## Description: <br>
PPT Ultra-wide Relayout helps agents convert standard PowerPoint decks into wider ultra-wide layouts while preserving editable text, reading order, visual hierarchy, and reference-deck aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[standed](https://clawhub.ai/user/standed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, presentation specialists, and agent developers use this skill to analyze PowerPoint structure and create editable ultra-wide relayout drafts without stretching text. It is suited for adapting standard decks to wider canvases or matching the aspect ratio and visual direction of a reference deck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python helpers process user-provided PowerPoint files and may expose slide text to the agent workflow or logs. <br>
Mitigation: Use the skill only on intended decks and avoid confidential presentations unless that exposure is acceptable. <br>
Risk: Automated relayout can create incorrect slide composition, overflow, or misplaced content. <br>
Mitigation: Save to a new output filename and review the generated PPTX before sharing or presenting it. <br>


## Reference(s): <br>
- [Reference Style Notes](references/reference-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON slide layout analysis, and editable PPTX outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python helpers on user-provided PowerPoint files and writes transformed decks to a chosen output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
