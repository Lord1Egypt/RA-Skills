## Description: <br>
Professional storyboard design tool for short drama/video production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautyaiclub](https://clawhub.ai/user/beautyaiclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and production teams use this skill to turn a plot outline or script into character designs, relationship planning, and structured storyboard CSVs for short-form video production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story scripts, draft CSVs, generation requests, and metadata may be saved in a local storyboard project workspace. <br>
Mitigation: Choose the output folder deliberately and avoid using confidential scripts unless local drafts and generation metadata are acceptable. <br>
Risk: Actual image and video generation is handed off to a separate myreels-api skill. <br>
Mitigation: Review the separate myreels-api skill before sending approved CSVs or prompts for image or video generation. <br>
Risk: Storyboards and prompts can contain inconsistent character, relationship, or shot details if the source story is ambiguous. <br>
Mitigation: Review and approve character tags, relationship rows, and storyboard CSVs before using them for downstream generation. <br>


## Reference(s): <br>
- [Character Design Reference](references/character-design.md) <br>
- [Recommended Model List](references/models.md) <br>
- [Multilingual Support Reference](references/multilingual.md) <br>
- [Scene Templates for Short Drama](references/scene-templates.md) <br>
- [Storyboard Template & Format Specification](references/storyboard-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown guidance and CSV files for character, relationship, and storyboard planning] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local storyboard project workspaces with draft, approved, export, request, task, metadata, review, and delivery folders when file output is needed.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
