## Description: <br>
KDP Author Engine helps agents write, edit, format, publish, and market indie books for Amazon KDP and IngramSpark using a structured six-agent workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droteng](https://clawhub.ai/user/droteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and indie-author agents use this skill to plan books, draft and review chapters, prepare KDP or IngramSpark publishing materials, research Amazon keywords, and run launch marketing workflows. It is intended for human-in-the-loop book production with explicit approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated manuscripts, metadata packages, or launch files could overwrite existing work if the output directory is unsafe or reused carelessly. <br>
Mitigation: Configure BOOKS_DIR to a dedicated project directory, keep backups of manuscripts, and review target filenames before allowing file writes or pandoc exports. <br>
Risk: Reader, reviewer, or ARC contact lists may contain personal data. <br>
Mitigation: Collect contacts only with permission, store them securely, use them only for the intended campaign, and delete them when no longer needed. <br>
Risk: Publishing, pricing, keyword, category, or health-related book guidance can become inaccurate or may require current external validation. <br>
Mitigation: Verify market data, platform rules, categories, pricing, medical claims, and legal or tax implications against authoritative current sources before publication. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Humanization Rules](references/humanization-rules.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Genre Playbooks](references/genre-playbooks.md) <br>
- [Chapter Workflow](references/chapter-workflow.md) <br>
- [KDP Publishing and Formatting Reference](references/kdp-publishing.md) <br>
- [Amazon Keyword Research for KDP](references/keyword-research.md) <br>
- [Book Marketing and Launch Strategy](references/book-marketing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/droteng/kdp-author-engine) <br>
- [Project Homepage](https://discord.gg/yGyXDwdHU9) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with templates, checklists, shell commands, and document-generation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local .docx manuscript, metadata, launch plan, and performance report files when used with a configured BOOKS_DIR and pandoc.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
