## Description: <br>
Local file knowledge base with LLM-powered indexing and Q&A that scans .txt, .md, .pdf, .docx, .xlsx, and .csv files, extracts summaries, tags, and tables of contents, and answers questions by retrieving relevant files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[congshengwu](https://clawhub.ai/user/congshengwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to create a local index of documents in a chosen directory and ask questions over the indexed content with file citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected folder's documents are read for indexing and Q&A, and generated summaries may be retained in .kb-meta.json. <br>
Mitigation: Point the skill at a narrow folder whose contents are appropriate to index; avoid broad home, secrets, cloud-sync, or confidential work folders unless intentional, and review or delete .kb-meta.json when no longer needed. <br>
Risk: Answers may be incomplete when the index is stale or a relevant file cannot be read. <br>
Mitigation: Run the indexing workflow after document changes and verify important answers against the cited source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/congshengwu/personal-kb-lite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown responses, JSON metadata files, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .kb-config.json and .kb-meta.json for the selected knowledge base directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
