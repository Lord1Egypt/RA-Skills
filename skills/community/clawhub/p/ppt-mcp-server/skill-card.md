## Description:

Generates professional PowerPoint presentations by executing AI-produced python-pptx code through an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janson1983](https://clawhub.ai/user/janson1983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create PowerPoint decks from prompts, outlines, or source content. The skill guides the agent to produce python-pptx code, execute it, and return generated presentation files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad Python code execution to generate PowerPoint files.

Mitigation: Install only in a tightly sandboxed environment with no secrets, restricted workspace access, and preferably no network access.

Risk: Generated presentation requests are executed as code.

Mitigation: Review or confirm generated code before running it and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janson1983/skills/ppt-mcp-server)
- [Artifact-declared repository](https://github.com/janson1983/ppt-master-mcp)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, Python code, MCP tool responses, and generated .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated presentation files are written to the MCP server output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
