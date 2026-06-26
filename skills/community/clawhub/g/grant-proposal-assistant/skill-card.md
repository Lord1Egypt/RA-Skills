## Description: <br>
Grant Proposal Assistant helps draft and review NIH, NSF, and other mainstream grant proposal sections, including specific aims, research strategy, and budget justification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, grant writers, and developers use this skill to generate proposal templates, budget justifications, review checklists, and critique reports for NIH, NSF, and similar funding applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated proposal guidance can be incomplete, incorrect, or out of date for a specific solicitation. <br>
Mitigation: Verify generated sections against the current sponsor instructions and institutional review requirements before submission. <br>
Risk: The local script reads user-supplied input paths in review mode and may process sensitive or unrelated proposal files. <br>
Mitigation: Review only intended proposal files and avoid passing unrelated sensitive documents as input. <br>
Risk: The local script writes to the user-supplied output path and can overwrite existing files. <br>
Mitigation: Use deliberate workspace-scoped output paths and check for existing files before running generation or review commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/grant-proposal-assistant) <br>
- [NIH R01 Grant Proposal Template](references/NIH_R01_template.md) <br>
- [NSF Standard Grant Template](references/NSF_template.md) <br>
- [Budget Templates by Category](references/budget_templates.md) <br>
- [Grant Proposal Review Checklist](references/review_checklist.md) <br>
- [Specific Aims Examples](references/specific_aims_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown templates and review reports, with optional command-line and Python usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated sections or review reports to a user-supplied output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
