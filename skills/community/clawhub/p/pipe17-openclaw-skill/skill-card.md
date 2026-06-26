## Description: <br>
Uses the Pipe17 Unified API to search and read orders, shipping requests, fulfillments, and inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-shao1](https://clawhub.ai/user/j-shao1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to look up Pipe17 commerce and fulfillment records, inspect inventory by SKU or location, and construct filtered API queries for support and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Pipe17 API key could be exposed through shared terminals, logs, transcripts, or overly broad environment access. <br>
Mitigation: Use a Pipe17 API key scoped to the intended organization and least privilege, preferably read-only where possible, and avoid exposing the key in shared output. <br>
Risk: Returned order, fulfillment, shipping, and inventory records may contain sensitive business data. <br>
Mitigation: Limit queries to the records needed for the task, avoid unnecessary data sharing, and treat API responses as sensitive operational data. <br>


## Reference(s): <br>
- [Pipe17 Unified API Docs](https://apidoc.pipe17.com/#/) <br>
- [ClawHub Skill Page](https://clawhub.ai/j-shao1/pipe17-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided PIPE17_API_KEY; outputs are instructions and command examples for Pipe17 API access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
