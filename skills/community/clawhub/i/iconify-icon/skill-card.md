## Description: <br>
Provides access to Iconify icon collections for browsing icon sets, searching icons, and retrieving framework usage examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to browse Iconify icon sets, search for matching icons, and retrieve icon data with framework examples. The skill requires a Xiaobenyang API key and sends icon queries through Xiaobenyang's MCP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and persists a third-party Xiaobenyang API key in a local .env file. <br>
Mitigation: Use a dedicated key, avoid shared or sensitive workspaces, and remove or rotate the key when the skill is no longer needed. <br>
Risk: Icon lookup requests are routed through Xiaobenyang's MCP API rather than directly to Iconify. <br>
Mitigation: Avoid submitting confidential project names or sensitive search terms, and review the third-party service before use in restricted environments. <br>
Risk: Security evidence notes unrelated Gaokao and school-service remnants that make the skill's true scope unclear. <br>
Mitigation: Review the artifact source and test in an isolated workspace before trusting it with credentials or sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/iconify-icon) <br>
- [Xiaobenyang API key site](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Guidance] <br>
**Output Format:** [Structured API results rendered as concise text or Markdown, with framework code examples when returned by icon data lookups.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Xiaobenyang API key before tool calls can succeed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
