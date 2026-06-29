## Description: <br>
Matches PowerPoint slide styling by analyzing an existing deck's palette, fonts, layout, rhythm, and validation rules, then guiding python-pptx edits for new or replacement pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and presentation authors use this skill to inspect an existing PowerPoint deck and generate or replace slides that follow the source deck's colors, typography, layout formulas, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a whole-deck residual keyword replacement step that could alter unrelated business content. <br>
Mitigation: Run it only on copies of PPT files, specify the exact pages to modify, and allow global residual keyword replacement only after reviewing the replacement list. <br>
Risk: Generated or modified slides may drift from the intended source deck style or layout constraints. <br>
Mitigation: Use the extracted palette, font tiers, layout formulas, and validate_layout checks before delivering the modified deck. <br>


## Reference(s): <br>
- [Design Patterns Reference](references/design-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/ppt-style-matcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create or modify PPTX files using python-pptx and validation checks.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
