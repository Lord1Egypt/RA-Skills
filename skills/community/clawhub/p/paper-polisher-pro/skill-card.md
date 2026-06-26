## Description: <br>
Paper Polisher helps agents detect AI-writing traces, produce academic quality reports, check terminology, and guide bilingual paper polishing while preserving data, citations, and technical terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[docsor1212](https://clawhub.ai/user/docsor1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic-writing teams use this skill to run local checks for AI-writing signals, terminology issues, similarity, and paper-quality metrics before revising bilingual manuscripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to reduce AI-detection signals in academic writing, which may enable authorship misrepresentation or policy violations. <br>
Mitigation: Use only for legitimate editing, transparency, and quality review; follow institutional authorship, disclosure, and academic integrity rules. <br>
Risk: User-provided manuscripts may contain confidential or restricted research content. <br>
Mitigation: Process only manuscripts the user is authorized to handle and avoid sharing confidential content outside approved environments. <br>
Risk: Detection scores and polishing suggestions may be inaccurate or incomplete. <br>
Mitigation: Treat outputs as review aids and require human review before changing or submitting academic work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/docsor1212/paper-polisher-pro) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SKILL_ZH.md](artifact/SKILL_ZH.md) <br>
- [AI patterns, English](artifact/references/ai_patterns_en.json) <br>
- [AI patterns, Chinese](artifact/references/ai_patterns_zh.json) <br>
- [Chinese sentence patterns](artifact/references/sentence_patterns_zh.json) <br>
- [General synonyms](artifact/references/synonyms_general.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and optional JSON reports from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on local user-provided manuscript files; reports AI-risk scores, pattern matches, terminology issues, similarity metrics, and quality summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
