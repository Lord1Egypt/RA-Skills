## Description: <br>
Use when the user asks how to operate Maito end to end, connect Maito to an agent, manage a Maito workspace, run newsletter publishing, create social drafts, manage subscribers, inspect attribution, work with sponsors, or use authenticated Maito MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman14](https://clawhub.ai/user/freeman14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External publishers and operators use this skill to manage Maito newsletters, social drafts, subscriber workflows, attribution, and sponsor materials. It guides authenticated Maito changes when tools are connected and returns a Maito-ready handoff when they are not. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing, sending, scheduling, subscriber changes, sponsor outreach, or payments can affect audiences, customer records, or commercial commitments. <br>
Mitigation: Require explicit user approval before these actions and report only changes that succeeded through authenticated Maito tools. <br>
Risk: Maito workflows can involve private subscriber data, analytics, sponsor contracts, credentials, tokens, or private URLs. <br>
Mitigation: Keep sensitive data out of committed files and public content, and summarize only the information needed for review. <br>
Risk: Drafts, sponsor proof, and attribution analysis may contain unsupported claims or inferred explanations. <br>
Mitigation: Separate verified Maito data from inference, preserve source notes, and require human review before publishing or external use. <br>


## Reference(s): <br>
- [Maito MCP Tools Documentation](https://getmaito.com/docs/mcp/tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with structured drafts, summaries, checklists, and handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Maito session or authenticated Maito MCP tools for persistence; otherwise outputs a Maito-ready handoff.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
