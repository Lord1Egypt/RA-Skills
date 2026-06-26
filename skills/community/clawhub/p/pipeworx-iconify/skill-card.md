## Description: <br>
Search 200,000+ open-source icons across 150+ collections - Material Design, Font Awesome, Heroicons, Lucide, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search icon collections, retrieve SVG data, compare icon styles, and configure access to the Pipeworx Iconify MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Icon search terms and requested icon names are sent to gateway.pipeworx.io. <br>
Mitigation: Avoid submitting sensitive project names, confidential feature names, or other private terms as icon queries. <br>
Risk: The optional MCP configuration runs mcp-remote from npm. <br>
Mitigation: Review and approve the npm dependency separately before enabling the MCP configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-iconify) <br>
- [Pipeworx Iconify pack](https://pipeworx.io/packs/iconify) <br>
- [Pipeworx Iconify MCP endpoint](https://gateway.pipeworx.io/iconify/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, icon identifiers, and SVG data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send icon search terms and requested icon names to gateway.pipeworx.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
