## Description: <br>
Markdown 工具箱 helps agents produce portable single-file Markdown with fenced code blocks, GFM tables, heading hierarchy checks, relative links, and basic validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agent users use this skill to generate or clean up portable Markdown documents and validate common formatting rules across GitHub, GitLab, Obsidian, and VS Code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file-writing authority that is broader than its Markdown formatting purpose requires. <br>
Mitigation: Require explicit confirmation before shell commands, npm installs, markdownlint runs, network diagnostics, or file changes outside the requested document. <br>
Risk: Generated Markdown guidance may still need human review for correctness, portability, and project-specific style. <br>
Mitigation: Review generated Markdown before publishing and run project-appropriate Markdown validation when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/markdown-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with fenced code blocks, checklists, tables, and occasional JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focused on single-file Markdown generation and basic validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
