## Description: <br>
A lesson-preparation guide for NOI/CSP/GESP informatics training that uses the ADDIE model to help agents produce age-appropriate teaching materials for 14-year-old students. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and teaching-content authors use this skill to plan informatics competition lessons, draft Markdown or Marp materials, create examples and assignments, and review classroom outcomes for iterative improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation and editing of lesson materials, which could overwrite or alter course content if used outside the intended workspace. <br>
Mitigation: Keep use limited to the course workspace and review proposed file changes before applying them. <br>
Risk: The artifact discusses optional image-generation API use and database update workflows. <br>
Mitigation: Explicitly approve any image-generation API call or database update before execution, and keep generated assets in the intended lesson directories. <br>
Risk: The artifact includes self-iteration behavior for maintaining the skill. <br>
Mitigation: Do not let the skill modify its own documents unless the user is intentionally maintaining this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/skills/prepkit) <br>
- [备课规则](artifact/references/备课规则.md) <br>
- [例题模板规则](artifact/references/例题模板规则.md) <br>
- [讲义ppt模板](artifact/assets/讲义ppt模板.md) <br>
- [智国学堂 OJ](https://fslong.iok.la/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown lesson plans, Marp slide drafts, C++ snippets, exercises, classroom notes, and evaluation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, image asset paths, or database update steps only when the user explicitly asks for those workflow outputs.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact metadata says 2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
