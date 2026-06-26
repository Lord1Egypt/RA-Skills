## Description: <br>
Granola MCP integration with managed authentication for searching meeting content, retrieving summaries and action items, listing meetings, and accessing transcripts via Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to query their connected Granola meeting notes, retrieve meeting metadata and summaries, find action items, and review transcripts when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized Granola meeting titles, attendees, notes, summaries, private notes, queries, and possible transcripts are routed through Maton. <br>
Mitigation: Install only when the user trusts Maton to broker Granola access, and revoke the Maton connection when it is no longer needed. <br>
Risk: The skill requires a sensitive MATON_API_KEY credential. <br>
Mitigation: Store the key in the MATON_API_KEY environment variable, avoid printing it in shared logs, and rotate or revoke it if exposed. <br>
Risk: Requests can target the wrong Granola account when multiple connections exist. <br>
Mitigation: Set the Maton-Connection header to the intended connection ID when more than one connection is available. <br>


## Reference(s): <br>
- [ClawHub Granola Skill](https://clawhub.ai/byungkyu/granola-api) <br>
- [Maton](https://maton.ai) <br>
- [Granola MCP Documentation](https://docs.granola.ai/help-center/sharing/integrations/mcp) <br>
- [Granola Help Center](https://docs.granola.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-shaped API responses and Python or JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an active Granola MCP connection; responses may include cited meeting-note links, XML-like meeting data, summaries, private notes, and transcripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
