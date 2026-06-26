## Description: <br>
Design UIs in Pencil (.pen files) and generate production-ready code from them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caopipeline](https://clawhub.ai/user/caopipeline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product teams use this skill to create or edit Pencil UI design files, generate PPT-style design boards, and convert Pencil designs into React, Tailwind CSS, and shadcn/ui code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write .pen files or edit Pencil documents through MCP. <br>
Mitigation: Use it in workspaces where Pencil file generation or MCP editing is expected, and review generated design files before relying on them. <br>
Risk: The skill defaults user-facing UI text in generated .pen files to Simplified Chinese unless the user specifies another language. <br>
Mitigation: State the desired UI language explicitly for English, bilingual, or multilingual projects. <br>
Risk: The activation scope covers broad UI prototyping and design-to-code requests. <br>
Mitigation: Narrow activation or invoke the skill explicitly when you do not want it used for general frontend design work. <br>
Risk: Generated Pencil, PPT, or code outputs can still contain layout or conversion mistakes. <br>
Mitigation: Run the skill's layout integrity and screenshot QA checks before accepting final design or code output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caopipeline/pencil-design-skill) <br>
- [Publisher profile](https://clawhub.ai/user/caopipeline) <br>
- [Pencil format reference](references/pen-format.md) <br>
- [Layout integrity reference](references/layout-integrity.md) <br>
- [Design token reference](references/design-tokens.md) <br>
- [Design-to-code workflow](references/codegen-workflow.md) <br>
- [MCP tool quick reference](mcp/mcp-tools.md) <br>
- [Screenshot QA reference](mcp/screenshot-qa.md) <br>
- [Style picker reference](styles/style-picker.md) <br>
- [getdesign.md style source](https://getdesign.md/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON .pen files, generated code, and tool or shell commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify Pencil .pen files directly, or use Pencil MCP tools when connected.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
