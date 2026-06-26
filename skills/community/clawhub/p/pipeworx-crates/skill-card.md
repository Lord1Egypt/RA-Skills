## Description: <br>
Search and retrieve Rust crate metadata, versions, and download statistics from crates.io through the hosted Pipeworx crates MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search public Rust packages, retrieve crate metadata, and inspect published crate versions and download statistics without authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries sent through the hosted Pipeworx gateway may disclose private project names or confidential package research. <br>
Mitigation: Use it for public Rust crate lookups, and avoid sending sensitive private package research unless you trust the Pipeworx service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-crates) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Pipeworx crates MCP endpoint](https://gateway.pipeworx.io/crates/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and MCP server configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public crate names, descriptions, versions, download counts, and related metadata from the crates.io REST API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
