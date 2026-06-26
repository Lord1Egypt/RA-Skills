## Description: <br>
English Visual Vocabulary helps learners build English vocabulary with image-based word cards, study plans, root and affix analysis, pronunciation notes, and Ebbinghaus-style review schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bxwzan](https://clawhub.ai/user/bxwzan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, educators, and study assistants use this skill to create visual English vocabulary cards, personalized study plans, and spaced-review schedules for vocabulary learning, exam preparation, and daily practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image search or generation can send requested words or topics to external services, depending on the host agent's available tools. <br>
Mitigation: Use explicit prompts, avoid sensitive study terms when using external image tools, and review host-agent tool permissions before deployment. <br>
Risk: The skill may create local study files such as vocabulary cards, learning plans, or review logs. <br>
Mitigation: Run it in an appropriate workspace and review generated files before sharing or reusing them. <br>
Risk: Vocabulary definitions, etymology, or root analysis can be incomplete or inaccurate. <br>
Mitigation: Review learner-facing word data against trusted dictionary or etymology references before relying on it for instruction or assessment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bxwzan/learn-english-with-images) <br>
- [Common English Roots and Affixes](artifact/references/common_roots.md) <br>
- [Ebbinghaus Review Schedule](artifact/references/ebbinghaus_schedule.md) <br>
- [Beginner Vocabulary List](artifact/references/vocabulary_lists/beginner.json) <br>
- [Intermediate Vocabulary List](artifact/references/vocabulary_lists/intermediate.json) <br>
- [Advanced Vocabulary List](artifact/references/vocabulary_lists/advanced.json) <br>
- [Oxford Learner's Dictionaries](https://www.oxfordlearnersdictionaries.com/) <br>
- [Etymonline](https://www.etymonline.com/) <br>
- [Anki](https://apps.ankiweb.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown learning plans and vocabulary cards, with optional JSON study data and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local card, plan, and learning-log files when scripts are used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
