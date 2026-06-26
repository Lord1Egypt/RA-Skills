## Description: <br>
Reviews AI short-drama and short-film storyboard prompts against a 10-point checklist covering time of day, subject consistency, scene anchors, lighting, shadows, material consistency, depth, shot choice, shadow direction, and asset annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beermanzz](https://clawhub.ai/user/beermanzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external creators use this skill to review AI image and video storyboard prompts before generation, marking prompts as pass or fail and identifying concrete revisions for visual consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger words such as self-review or checklist may invoke the skill outside AI image or video prompt review. <br>
Mitigation: Confirm the user is reviewing storyboard or generation prompts before applying the checklist. <br>
Risk: Prompt asset annotations may expose sensitive local paths when prompts are sent to external generation tools. <br>
Mitigation: Use non-sensitive asset identifiers or sanitized relative names before sharing prompts with external services. <br>


## Reference(s): <br>
- [Detailed prompt quality checklist](references/checklist-detailed.md) <br>
- [ClawHub skill page](https://clawhub.ai/beermanzz/prompt-quality-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown checklist review with pass/fail findings and revision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only review output; no code, commands, credentials, or privileged actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
