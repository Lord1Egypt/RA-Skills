## Description: <br>
结构化审校中文论文：从参考论文学习风格，统一结构图谱，执行格式/术语/逻辑/风格融合审查，并将结果回写为 Word 批注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urnotLhh](https://clawhub.ai/user/urnotLhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing-support teams use this skill to review Chinese thesis drafts with structure-aware format, terminology, logic, and style checks. It learns a style profile from user-provided reference papers and writes review results back as Word comments for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target manuscripts and reference-paper excerpts may be sent to the configured LLM provider. <br>
Mitigation: Use an approved provider, explicit skill-specific LLM settings, and a limited API key; only process documents that are permitted for that provider. <br>
Risk: Ambient OpenAI-compatible environment variables or global provider defaults may route document content to an unintended service. <br>
Mitigation: Set the PAPER_STYLE_REVIEW_LLM_* configuration explicitly and avoid relying on generic OPENAI_* defaults. <br>
Risk: The review pipeline can remove prior generated outputs in the selected output directory. <br>
Mitigation: Use an isolated output directory and keep original manuscripts and reference files outside that directory. <br>
Risk: Generated Word comments may contain incorrect, incomplete, or misleading review suggestions. <br>
Mitigation: Treat annotations as review aids and have a human reviewer approve changes before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urnotLhh/paper-style-review) <br>
- [Review configuration example](references/review-config.example.json) <br>
- [Format rule matrix](references/format-rule-matrix.md) <br>
- [Format rules](references/format-rules.json) <br>
- [Style profile extractor](references/style-profile-extractor.md) <br>
- [Style profile schema](references/style-profile.schema.json) <br>
- [AI diff report schema](references/ai-diff-report.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Word document annotations] <br>
**Output Format:** [Markdown guidance with shell commands; runtime outputs include JSON reports, a style profile, structured annotations, and annotated DOCX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided target and reference documents; review generated annotations before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
