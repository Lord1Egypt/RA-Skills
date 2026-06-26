## Description: <br>
Figma Design Integration helps agents read Figma design assets, inspect components and styles, export design artifacts, generate frontend code, and coordinate design-to-code workflows through REST API and MCP access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyqthu](https://clawhub.ai/user/chenyqthu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to inspect Figma files, map design systems to implementation work, extract design tokens or screenshots, and generate React, Vue, or HTML from selected frames. Teams with appropriate Figma permissions can also use MCP workflows to create or modify Figma content after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authenticated access to private Figma files and design assets. <br>
Mitigation: Use a least-privilege Figma token, limit use to approved files, and avoid sensitive or unreleased designs unless explicitly authorized. <br>
Risk: MCP workflows described by the skill can create or modify Figma content when the account has edit permission. <br>
Mitigation: Require explicit user confirmation before write or create actions, inspect the target file first, and verify changes incrementally. <br>
Risk: Bundled Omada asset links may expose private organizational design context. <br>
Mitigation: Treat asset registry links and derived outputs as potentially confidential and avoid sharing them outside approved teams. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenyqthu/openclaw-figma) <br>
- [Figma MCP server](https://mcp.figma.com/mcp) <br>
- [Agent operation guide](references/guide-for-agents.md) <br>
- [Human workflow guide](references/guide-for-humans.md) <br>
- [Omada asset registry](references/omada-assets.md) <br>
- [WEB component library](https://www.figma.com/design/gzLJeRunJYuB02zQKTOkva) <br>
- [APP component library](https://www.figma.com/design/beYqvBsrUqRoq6GNfvOAuN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API command examples, and generated frontend code or design-token outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Figma REST API responses, exported image file paths, MCP tool guidance, or generated UI implementation snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
