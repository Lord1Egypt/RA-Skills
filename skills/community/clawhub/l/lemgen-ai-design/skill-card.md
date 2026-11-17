## Description:

Search 4,500+ curated AI image and video prompts, enhance prompts, and generate with LemGen from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aithink001](https://clawhub.ai/user/aithink001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and creative agents use this skill to search prompt examples, refine or translate prompts, inspect visual inspiration, and generate LemGen images or videos after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned external MCP server that receives a LemGen API token.

Mitigation: Pin the MCP server to a reviewed commit or release, use a revocable low-scope LemGen token, and run the server with minimal filesystem and network access.

Risk: Image and video generation can consume paid service credits or create long-running jobs.

Mitigation: Require explicit user approval before generation, avoid repeated video retries, and check LemGen generation history before starting another job.

Risk: The LemGen API token could be exposed through chat, logs, screenshots, or shared configuration.

Mitigation: Keep LEMGEN_API_TOKEN out of chat, logs, screenshots, and shared configs; rotate the token if exposure is suspected.

## Reference(s):

- [LemGen AI Design ClawHub page](https://clawhub.ai/aithink001/skills/lemgen-ai-design)
- [Skill-declared MCP repository](https://github.com/aithink001/lemgen-ai-design-mcp)
- [LemGen prompt gallery](https://lemgen.org)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, API calls]

**Output Format:** [Markdown guidance with prompt examples, tool recommendations, and JSON MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation tools require LEMGEN_API_TOKEN and explicit user approval before image or video generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
