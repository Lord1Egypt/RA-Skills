## Description: <br>
Structures and archives notes, reports, and knowledge documents into topic folders, maintains a searchable index, and prompts for missing context during reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chentx1243](https://clawhub.ai/user/chentx1243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn pasted text or local Markdown/text files into a persistent structured knowledge base with summaries, facts, code snippets, resources, and an index for later retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist, reorganize, copy, and index local content, which may expose sensitive files if broad or high-sensitivity folders are selected. <br>
Mitigation: Point it only at narrow, low-sensitivity folders and avoid archiving secrets, credentials, private keys, internal server details, regulated data, or sensitive configuration files. <br>
Risk: The workflow moves processed source files and refreshes the index, which can make recovery harder if the output is not reviewed. <br>
Mitigation: Keep backups and regularly review generated meta.md, process.md, code.md, resource files, and index.json. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chentx1243/maple-structured-storage) <br>
- [File writing rules](references/file-rules.md) <br>
- [Reflection workflow](references/reflection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown files, JSON index data, copied resource files, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .knowledge-config.json, move processed source files into a done folder, refresh index.json, and update topic files under the configured storage path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
