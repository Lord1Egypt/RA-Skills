## Description:

A Chinese lesson-preparation framework for NOI/CSP/GESP informatics training that helps agents plan objectives, lesson flow, examples, exercises, code, and optional lecture or PPT materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and agent users use this skill to prepare Chinese informatics competition lessons for middle-school and high-school learners, including learning analysis, lesson design, teaching materials, examples, assignments, and C++ code snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated materials may include Zhiguo Xuetang branding, footer text, contact fields, or named role conventions without clear opt-in.

Mitigation: Review generated lesson materials before use and remove or replace branding, contact fields, and role names unless they are intended for the class.

Risk: The skill can request file edits, self-documentation updates, image-generation API use, or asset downloads.

Mitigation: Require explicit approval before allowing edits, documentation updates, image-generation calls, or downloaded assets.

Risk: Teaching examples, assignments, and C++ snippets may be inaccurate or mismatched to learner level.

Mitigation: Have an educator review lesson objectives, examples, code, and assignments before classroom or OJ use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fslong520/skills/prepkit)
- [Information Olympiad Lesson Preparation Rules](references/备课规则.md)
- [Example Problem Template Rules](references/例题模板规则.md)
- [Analysis Module](modules/01-Analysis分析.md)
- [Design Module](modules/02-Design设计.md)
- [Development Module](modules/03-Development开发.md)
- [Narrative Design Module](modules/叙事设计.md)
- [Lecture PPT Template](assets/讲义ppt模板.md)
- [Zhiguo Xuetang OJ](https://fslong.iok.la/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown lesson materials, Marp-compatible slide Markdown when requested, C++ code snippets, exercise specifications, and planning guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional illustration prompts and asset placement guidance when explicitly requested.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
