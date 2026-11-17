## Description:

面向6-12岁儿童的AI家教助手，结合苏格拉底式引导和知识讲解，以数学和科学为主，支持AI主动出题、个性化难度调节、错误引导、学习记录和家长报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang1076](https://clawhub.ai/user/lixiang1076)

### License/Terms of Use:

MIT

## Use Case:

External users and families can use this skill to guide 6-12 year old children through short math and science tutoring sessions with Socratic prompting, adaptive difficulty, local learning records, and parent-facing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a child's profile and learning history in local plaintext files.

Mitigation: Get parent consent before use, avoid real full names, and keep the data/kid-tutor/ directory access-controlled.

Risk: The documented shell echo pattern for logging session JSON can mishandle user-provided content.

Mitigation: Use a file-based session JSON workflow or a non-shell stdin invocation instead of echoing JSON through the shell.

Risk: Parent reports may include child learning data and are described as shareable through Feishu.

Mitigation: Review report contents and obtain a separate confirmation before sending reports outside the local environment.

## Reference(s):

- [Curriculum](references/curriculum.md)
- [Pedagogy](references/pedagogy.md)
- [Question Templates](references/question-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/lixiang1076/skills/kid-tutor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational tutoring guidance, inline shell commands, local JSON learning records, and Markdown parent reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local profile and session files under data/kid-tutor/ when the helper scripts are run.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
