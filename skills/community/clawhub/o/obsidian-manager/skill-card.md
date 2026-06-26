## Description: <br>
Obsidian Manager helps agents create, search, link, and organize local Obsidian research notes through the integrated knowledge entry point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent operators use this skill to manage local Obsidian-based research notes, including note creation, full-text search, and knowledge-link workflows. The artifact documents this release as a compatibility layer that forwards users toward the unified knowledge skill entry point. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads from and writes to a local Obsidian research vault, so a misconfigured vault path can expose or alter unintended Markdown collections. <br>
Mitigation: Before use, verify that the research vault path points only to notes the agent is allowed to read and modify. <br>
Risk: Note titles and direction values are used to form local file paths, which can be brittle if values contain absolute paths or path traversal segments. <br>
Mitigation: Avoid note titles or direction values containing path traversal such as ../ or absolute paths, and review generated file paths before overwriting existing notes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jirboy/obsidian-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown notes, text search results, and optional JSON search output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and searches local Markdown files under a configured research vault path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
