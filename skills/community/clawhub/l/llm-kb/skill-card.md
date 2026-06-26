## Description: <br>
Create and maintain LLM-powered personal knowledge bases that ingest sources, answer questions, and maintain an Obsidian-compatible vault over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to create persistent Markdown wiki vaults, ingest URLs, files, or pasted text, query organized content, and generate saved summaries, comparisons, guides, and analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent local vault and stores raw source copies under raw/inbox/. <br>
Mitigation: Choose the vault location deliberately and avoid adding secrets or sensitive documents unless retaining raw local copies is intended. <br>
Risk: The skill can ingest URLs, local files, and pasted text into the knowledge base. <br>
Mitigation: Approve sources before ingestion and review generated source cards, concept pages, and entity pages for accuracy. <br>
Risk: Generated wiki content may contain uncertain or outdated claims. <br>
Mitigation: Keep important claims tied to source pages, mark uncertainty explicitly, and use the LINT operation to find stale, missing, or broken content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/llm-kb) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown wiki pages, JSON configuration snippets, shell command guidance, and concise status reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains a local Obsidian-compatible vault with raw source captures, source cards, concept pages, entity pages, outputs, and an activity log.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
