## Description: <br>
Pharaoh provides a codebase knowledge graph and MCP-backed developer workflow skills for querying architecture, dependencies, blast radius, dead code, and test coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xuxdesign](https://clawhub.ai/user/0xuxdesign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Pharaoh to give AI agents repository-aware architecture, dependency, blast-radius, dead-code, and test-coverage context before planning or modifying code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository metadata and docstrings are processed and stored on Pharaoh infrastructure. <br>
Mitigation: Install only for repositories you intend to share with Pharaoh, and use the documented repository deletion or account deletion paths when finished. <br>
Risk: The skill requires read-only GitHub access and OAuth credentials stored at ~/.pharaoh/credentials.json. <br>
Mitigation: Limit the GitHub App to selected repositories, keep the credentials file owner-only, and revoke access or run the documented logout command when access is no longer needed. <br>
Risk: The installer modifies OpenClaw configuration and overwrites existing Pharaoh skill files on reinstall. <br>
Mitigation: Review the install command before running it, preserve any local Pharaoh skill customizations, and remove the MCP entry and installed skills during uninstall. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xuxdesign/pharaoh) <br>
- [Pharaoh documentation](https://pharaoh.so/docs) <br>
- [Pharaoh homepage](https://pharaoh.so) <br>
- [Pharaoh MCP server](https://mcp.pharaoh.so) <br>
- [Pharaoh MCP npm package](https://www.npmjs.com/package/@pharaoh-so/mcp) <br>
- [Pharaoh GitHub App](https://github.com/apps/pharaoh-so) <br>
- [GitHub Device Authorization Grant](https://datatracker.ietf.org/doc/html/rfc8628) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MCP-backed repository context when Pharaoh tools are available.] <br>

## Skill Version(s): <br>
0.3.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
