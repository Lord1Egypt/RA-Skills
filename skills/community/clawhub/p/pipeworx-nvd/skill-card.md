## Description: <br>
NVD MCP wraps the NIST National Vulnerability Database API with free, no-auth CVE lookup tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to connect an agent to Pipeworx-hosted NVD MCP tools for CVE search, CVE detail lookup, and recent vulnerability review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CVE lookup queries are sent to the Pipeworx MCP gateway. <br>
Mitigation: Use the skill only when Pipeworx is trusted to process those queries. <br>
Risk: The artifact configures npx to run mcp-remote@latest, which can change over time. <br>
Mitigation: Pin mcp-remote to a reviewed package version before production deployment. <br>


## Reference(s): <br>
- [Pipeworx NVD pack homepage](https://pipeworx.io/packs/nvd) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-nvd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON configuration blocks and tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the Pipeworx MCP gateway for NVD vulnerability lookup; no API key is required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
