## Description: <br>
Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert common document, data, web, media, archive, and e-book inputs into Markdown for LLM processing or text analysis. It also points users to SkillBoss API Hub for complex document extraction when local markitdown output is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SkillBoss API Hub path sends document or URL content to an external service. <br>
Mitigation: Use that path only for content you are allowed to share with SkillBoss; keep sensitive documents on the local markitdown path unless approved. <br>
Risk: The skill requires a SKILLBOSS_API_KEY for the optional API workflow. <br>
Mitigation: Store the key in the environment and avoid placing it in prompts, files, logs, or shared examples. <br>
Risk: The markitdown plugin option can run third-party extensions. <br>
Mitigation: Enable third-party plugins only when their source and behavior are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/modesty-markdown-converter) <br>
- [SkillBoss Setup Guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API Hub](https://api.skillboss.co/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs preserve document structure such as headings, tables, lists, and links when supported by the converter.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
