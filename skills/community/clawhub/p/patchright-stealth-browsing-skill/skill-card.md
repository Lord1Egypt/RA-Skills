## Description: <br>
Perform stealth browser automation to bypass bot detection (Cloudflare, Akamai, Datadome) using Patchright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized automation operators use this skill to guide an agent through browser workflows on protected sites using Patchright MCP tools. It covers navigation, form interaction, session reuse, screenshots, proxy settings, and challenge handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for stealth browser automation against anti-bot protections. <br>
Mitigation: Use it only for legitimate, authorized testing or automation on sites you control or are permitted to assess. <br>
Risk: Saved cookies, browser profiles, screenshots, and videos can contain credentials or personal data. <br>
Mitigation: Handle these artifacts as sensitive data, restrict access, and remove them when they are no longer needed. <br>
Risk: The required patchright-mcp server is private and is not fully represented by the packaged skill files. <br>
Mitigation: Review and trust the patchright-mcp server separately before enabling this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyber-bye/patchright-stealth-browsing-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cyber-bye) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with tool names, JSON-like action parameters, and inline shell or configuration references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and an installed, configured, running patchright-mcp server with the referenced MCP tools.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
