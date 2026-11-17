## Description:

Interactive Architecture Diagram helps agents turn architecture, code, process, knowledge-base, and long-form text requests into structured ContextWeave diagram workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qhyw99](https://clawhub.ai/user/qhyw99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and knowledge workers use this skill to convert complex technical, business, and knowledge content into explicit diagram-generation requests. It is suited for architecture diagrams, dependency maps, business process diagrams, mind maps, and structured information graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram requests may include proprietary systems, code structure, customer workflows, or secrets and are uploaded to a fixed remote service.

Mitigation: Use the skill only where remote processing is approved, and avoid including secrets or sensitive proprietary details in diagram requests.

Risk: The skill may use a bundled shared API key when CONTEXTWEAVE_MCP_API_KEY is not configured.

Mitigation: Configure a user- or organization-owned API key and manage it through the environment.

Risk: Security guidance flags unsafe local file-writing plus path and command-injection issues around returned filenames and the included E2E test.

Mitigation: Avoid running the E2E test or trusting backend-returned filenames until those issues are fixed; review paths before executing generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qhyw99/skills/interactive-architecture-diagram)
- [Skill source](artifact/SKILL.md)
- [ContextWeave example configuration](artifact/cwmcp_config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON responses with diagram session identifiers, generated asset URLs, and locally written ContextWeave code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and uses CONTEXTWEAVE_MCP_API_KEY when configured.]

## Skill Version(s):

0.1.18 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
