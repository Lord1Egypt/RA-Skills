## Description: <br>
Knowledge Expansion Notetaking (KEN) turns newly shared knowledge, concepts, or methods into sourced, structured deep-note cards and archives them to Get notes, Feishu wiki/docs, and a local file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to expand a newly learned idea into a structured note with source context, concept analysis, boundaries, ambiguity checks, follow-up questions, and an AI-written continuation. It is intended for personal knowledge management workflows that sync generated notes into Get notes, Feishu wiki/docs, and local backup files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically archive user-provided knowledge content to external Get note and Feishu destinations. <br>
Mitigation: Use it only with the intended Feishu workspace and Get note account, avoid sensitive personal or proprietary notes unless external archiving is acceptable, and require explicit confirmation before syncing. <br>
Risk: The workflow grants full Feishu document access to a hardcoded user identifier. <br>
Mitigation: Review and replace the recipient before use, or remove the automatic permission grant and require explicit approval for permission changes. <br>
Risk: The skill depends on sensitive credentials and external workspace permissions for Feishu and Get note operations. <br>
Mitigation: Keep credentials scoped to the minimum required access, store them outside the skill files, and rotate them if workspace membership or intended usage changes. <br>


## Reference(s): <br>
- [Feishu knowledge base configuration](references/feishu-kb-config.md) <br>
- [ClawHub release page](https://clawhub.ai/binhuatochina/knowledge-expansion-notetaking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes with Feishu XML conversion guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates an eight-section deep note, up to 800 Chinese characters for the AI continuation section, and returns archive links plus a core finding and follow-up question.] <br>

## Skill Version(s): <br>
0.4.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
