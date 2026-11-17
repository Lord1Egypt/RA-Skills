## Description:

Model Context Protocol bridge that lets AI agents search, read, create, update, move, comment on, and upload content in an Outline workspace over SSE transport.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuellie](https://clawhub.ai/user/samuellie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Outline can give an agent controlled access to workspace documents, collections, comments, and user directory data. The skill is suited for documentation search, document drafting, updates, collaboration workflows, and media upload assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload helper can read any file that the OpenClaw process can read and send it to an agent-supplied URL.

Mitigation: Run the skill with least-privileged filesystem access, restrict readable paths, review agent upload requests, and avoid enabling upload or bulk-sync workflows unless local file upload is required.

Risk: A broad Outline API key can expose or modify workspace documents, collections, comments, and user data.

Mitigation: Use a minimally scoped Outline API key tied to the intended workspace permissions and rotate it if logs or behavior indicate unexpected access.

Risk: An untrusted OUTLINE_URL could redirect authenticated requests or uploads away from the intended Outline origin.

Mitigation: Configure only a trusted HTTPS Outline MCP endpoint and use URL allowlisting before routine deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuellie/skills/outline-app-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/samuellie)
- [Outline](https://www.getoutline.com/)
- [Model Context Protocol SDK package](https://registry.npmjs.org/@modelcontextprotocol/sdk/-/sdk-1.27.1.tgz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API responses]

**Output Format:** [Markdown guidance, shell commands, and JSON responses from Outline and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OUTLINE_API_KEY, OUTLINE_URL, Node.js, and npm; file upload paths can read local files available to the OpenClaw process.]

## Skill Version(s):

1.3.4 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
