## Description: <br>
面向6-12岁儿童的AI家教助手，结合苏格拉底式引导和知识讲解，以数学和科学为主，支持主动出题、个性化难度调节、学习记录和家长报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang1076](https://clawhub.ai/user/lixiang1076) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Parents, guardians, and educators use this skill to run short, child-appropriate math and science tutoring sessions for ages 6-12. It supports guided questioning, adaptive difficulty, local learning records, and parent-facing progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores identifiable learning records about children, including profile details and session history. <br>
Mitigation: Use pseudonyms where possible, keep the local data directory private, and delete old sessions when they are no longer needed. <br>
Risk: Parent reports may expose child learning history if shared without clear consent. <br>
Mitigation: Send reports only to explicitly approved recipients and only when a parent or guardian understands and accepts the data sharing. <br>


## Reference(s): <br>
- [小学数学与科学知识体系（人教版课标对齐）](references/curriculum.md) <br>
- [教学法指南](references/pedagogy.md) <br>
- [出题模板库](references/question-templates.md) <br>
- [ClawHub release page](https://clawhub.ai/lixiang1076/kid-tutor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational tutoring text, Markdown reports, JSON learning records, and local shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores child profile and session data locally under the configured data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
