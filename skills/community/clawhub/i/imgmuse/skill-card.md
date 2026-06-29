## Description: <br>
通用型图像Prompt生成器。输入主题描述，AI自主分析主体特征、决定艺术风格、推荐配色构图，输出结构化Prompt。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, educators, and developers use this skill to turn a topic or visual goal into structured image-generation prompts, including Markdown, JSON, plain-text, and English prompt variants for image tools. It is especially oriented toward Chinese-language visual design and educational infographic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper is Chinese-oriented and may default to Chinese wording or Chinese visual-design assumptions. <br>
Mitigation: Ask explicitly for the desired output language, target image tool, audience, and style constraints. <br>
Risk: The skill can write or edit files when an agent is allowed to use those tools. <br>
Mitigation: Confirm whether files should be written before using write-capable agent tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/imgmuse) <br>
- [Publisher profile](https://clawhub.ai/user/fslong520) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/reference.md](artifact/reference.md) <br>
- [artifact/examples.md](artifact/examples.md) <br>
- [artifact/知识可视化专家.md](artifact/知识可视化专家.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured Markdown with optional JSON, plain-text, and English prompt variants] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aspect-ratio guidance, negative prompts, style notes, composition details, and follow-up questions when the user's brief is incomplete.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
