## Description: <br>
Build and maintain a structured local knowledge base. Classify incoming content, save it as reusable Markdown, organize inbox items, and keep the knowledge base consistent over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaochuanchao](https://clawhub.ai/user/Shaochuanchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to initialize and maintain a local Markdown knowledge base, classify incoming notes or documents by purpose, and keep reusable entries organized over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and reorganize local Markdown files, so large organization tasks may place content in unexpected paths or categories. <br>
Mitigation: Use a dedicated workspace or knowledge/ directory and review generated paths before large reorganizations. <br>
Risk: Stored knowledge entries may preserve sensitive content or reusable prompts from untrusted sources. <br>
Mitigation: Avoid saving secrets, preserve source attribution, and review stored prompt or instruction entries before reuse. <br>


## Reference(s): <br>
- [Classification Rules](artifact/docs/classification-rules.md) <br>
- [Naming Rules](artifact/docs/naming-rules.md) <br>
- [Default Entry Template](artifact/templates/default-entry.md) <br>
- [Project Entry Template](artifact/templates/project-entry.md) <br>
- [Research Entry Template](artifact/templates/research-entry.md) <br>
- [Reference Entry Template](artifact/templates/reference-entry.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Configuration] <br>
**Output Format:** [Structured Markdown entries, local file paths, folder plans, and concise organization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local files inside a dedicated knowledge/ directory when the agent has workspace file access.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
