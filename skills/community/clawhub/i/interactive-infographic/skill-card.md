## Description:

Interactive Infographic helps agents turn complex text, knowledge, business processes, mind maps, and architecture descriptions into structured ContextWeave infographic generation requests and rendered visual assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qhyw99](https://clawhub.ai/user/qhyw99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and knowledge workers use this skill to convert dense requirements, system relationships, process flows, and long-form content into structured infographic requests and generated visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local input file contents and drawing requests to a third-party ContextWeave backend.

Mitigation: Use it only with content that may be sent to that service, and avoid passing sensitive or symlinked files as input.

Risk: The security guidance flags path-safety and credential-management issues, including reliance on an embedded anonymous credential when no API key is set.

Mitigation: Set your own CONTEXTWEAVE_MCP_API_KEY before use, keep input files inside the active workspace, and review paths before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qhyw99/skills/interactive-infographic)
- [ContextWeave Default Backend](https://pptx.chenxitech.site)
- [ContextWeave Example API URL](https://api.contextweave.site)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Single JSON object with generation status, session_id, asset URLs or file paths, and error details when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; reads CONTEXTWEAVE_MCP_API_KEY when set; sends requested drawing content to the ContextWeave backend.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
