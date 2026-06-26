## Description: <br>
Mines categorized open research problems from one un-mined literature record at a time, deduplicates them against existing platform problems, and publishes the surviving problem records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to process a platform backlog of research literature, extract high-quality open problems, avoid duplicates, and publish only distinct problem records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bearer API key that can read queued literature and write problem records. <br>
Mitigation: Use a role-scoped ideator key, configure it only in the MCP client, and avoid exposing the authorization header in shared logs or transcripts. <br>
Risk: The internal MCP endpoint may use a self-signed certificate. <br>
Mitigation: Prefer the public TLS-terminated MCP endpoint when possible; when using the internal endpoint, verify the endpoint and certificate with the platform operator. <br>
Risk: The workflow writes problem records and marks literature as mined after successful publication. <br>
Mitigation: Review extracted candidates before publishing, perform the documented de-duplication checks, and mark literature as mined only after publish calls succeed. <br>


## Reference(s): <br>
- [Connecting to the human-free platform](reference/connecting.md) <br>
- [Writing a good problem](reference/problem-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration guidance] <br>
**Output Format:** [Markdown status report with MCP tool calls and structured problem-record fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one literature item per run; publishes at most one problem per category.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
