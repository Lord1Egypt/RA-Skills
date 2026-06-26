## Description: <br>
PPT Layout Matcher analyzes presentation content against a 45-page 16:9 layout library and recommends suitable PowerPoint slide layouts across 10 categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presentation authors, and agents use this skill to analyze slide content, select top PowerPoint layout matches, and create or guide slide generation after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad presentation-related wording and provide layout recommendations when the user only intended a general discussion. <br>
Mitigation: Confirm the user's intent and present top layout recommendations for review before creating slides. <br>
Risk: Optional slide-generation workflows depend on local Python packages such as python-pptx or markitdown. <br>
Mitigation: Install optional dependencies only from trusted package sources and review generated PPTX output before use. <br>


## Reference(s): <br>
- [Layout Templates Reference](references/layout_templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zrxparley/ppt-layout-matcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or text recommendations with optional Python code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes layout names, slide references, match scores, structure descriptions, and recommendation explanations; PPTX generation depends on python-pptx.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
