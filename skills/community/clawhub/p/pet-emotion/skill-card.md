## Description: <br>
上传猫狗照片后，该技能调用 DashScope 多模态模型识别快乐、悲伤、愤怒、恐惧、放松或警觉情绪，并生成包含置信度、解读和雷达图的 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners and assistants use this skill to analyze a provided cat or dog photo, summarize the likely emotional state, and produce an HTML report with confidence, visualizations, and interaction suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and can fall back to OPENAI_API_KEY when DASHSCOPE_API_KEY is absent. <br>
Mitigation: Use a DashScope-specific DASHSCOPE_API_KEY for this skill and avoid relying on a general-purpose OPENAI_API_KEY. <br>
Risk: Analyzed pet photos are uploaded to DashScope and embedded in the generated HTML report. <br>
Mitigation: Only analyze photos the user intends to upload to DashScope, and treat generated reports as files containing the original image. <br>
Risk: The emotion analysis and suggestions may be wrong or incomplete for signs of pain, fear, aggression, or illness. <br>
Mitigation: Treat results as informal behavior guidance and consult a veterinarian or qualified professional for concerning symptoms. <br>


## Reference(s): <br>
- [宠物情绪解读知识库](references/emotion_guide.md) <br>
- [Project homepage](https://github.com/bettermen/pet-emotion) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/pet-emotion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summary plus generated HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a pet image path and a DashScope API key; generated reports embed the analyzed image.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
