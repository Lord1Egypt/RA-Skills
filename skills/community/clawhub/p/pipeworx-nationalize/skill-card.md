## Description: <br>
Nationalize MCP provides nationality prediction from a first name through nationalize.io, with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Pipeworx-hosted MCP server for predicting likely nationalities from first names, either one at a time or in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Names submitted for nationality prediction may be sent to Pipeworx's gateway and the underlying prediction service. <br>
Mitigation: Avoid submitting sensitive, regulated, or bulk personal data unless that external processing is acceptable for the use case. <br>


## Reference(s): <br>
- [Pipeworx Nationalize Pack](https://pipeworx.io/packs/nationalize) <br>
- [Pipeworx](https://pipeworx.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Markdown with JSON configuration and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote Pipeworx MCP gateway; no API key is declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
