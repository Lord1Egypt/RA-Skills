## Description: <br>
全球海岛选岛助手通过分步询问人数、预算、出发地、飞行时长和偏好，为中文用户推荐合适海岛，并可在流程完成后使用可选 FlyAI/飞猪查询商品链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amokay](https://clawhub.ai/user/amokay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Chinese-speaking travelers and travel planners use this skill to narrow island destinations by group size, budget, departure city, acceptable flight time, travel dates, trip length, and activity preferences. It supports itinerary-oriented recommendations and can optionally add real travel product links after the recommendation flow is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad beach-vacation wording may activate the skill when the user only wants general travel conversation. <br>
Mitigation: Confirm the user wants island selection and continue with one question at a time before collecting detailed preferences. <br>
Risk: The optional FlyAI/Fliggy lookup sends destination, trip length, and activity search terms to an external travel service. <br>
Mitigation: Use the lookup only after the five-step flow when product links are needed, and proceed with recommendations only if the component is unavailable or untrusted. <br>


## Reference(s): <br>
- [全球海岛数据库](references/island-database.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown travel recommendations with optional inline command-backed product lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are produced after a five-step question flow; optional product links require a trusted local flyai-cli installation.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
