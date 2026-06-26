## Description: <br>
Huo15 Knowledge Base helps an agent ingest documents, URLs, or notes into a local knowledge base, compile them into human-readable Markdown wiki entries, and search or lint the resulting knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to maintain a local, Markdown-based research library for papers, web pages, notes, and optional memory-reference material. It supports document ingestion, LLM-assisted wiki compilation, local grep-style search, indexing, and health-check prompt generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and wiki entries may be included in prompts or sent to the configured LLM provider during compile and health-check workflows. <br>
Mitigation: Use the skill only with documents that are approved for local storage and provider processing, and confirm the provider and credentials in models.json before running LLM-assisted commands. <br>
Risk: Activation scripts create knowledge-base folders and configuration under agent directories, and the all-agents activation script can initialize every detected agent. <br>
Mitigation: Start with one test agent and run the all-agents activation script only when broad initialization is intentional. <br>
Risk: Generated lint or compile outputs may alter wiki content or introduce inaccurate summaries. <br>
Mitigation: Review generated prompts and any resulting Markdown edits before treating the compiled wiki as trusted knowledge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-knowledge-base) <br>
- [Publisher profile](https://clawhub.ai/user/jobzhao15) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, shell command output, generated prompts, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores raw documents, cache files, wiki entries, indexes, and generated prompts in local knowledge-base directories.] <br>

## Skill Version(s): <br>
0.7.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
