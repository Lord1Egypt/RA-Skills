## Description: <br>
Personal knowledge wiki manager that organizes notes into structured Markdown wiki pages with concept pages, summaries, and cross-references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local Markdown knowledge wiki, add links or documents, summarize sources, create concept pages, answer queries with citations, and run wiki health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently creates, updates, and logs local wiki files. <br>
Mitigation: Review KNOWLEDGE_BASE_DIR before use and run the skill only on knowledge-base directories intended for persistent local storage. <br>
Risk: Sensitive source material added to the wiki will be retained locally in Markdown files and logs. <br>
Mitigation: Avoid ingesting sensitive content unless local retention in the knowledge directory is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown wiki files, textual reports, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local files under KNOWLEDGE_BASE_DIR or the default ~/.openclaw/workspace/knowledge path.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
