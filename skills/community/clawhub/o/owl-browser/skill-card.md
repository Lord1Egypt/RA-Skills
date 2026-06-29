## Description: <br>
Drive Owl Browser as an agent. Read pages as compact, handle-addressable OwlMark and click/type by handle, not by screenshot or pixel coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibnbd](https://clawhub.ai/user/ibnbd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to control Owl Browser through its HTTP or MCP tooling, observe pages as OwlMark, and click or type using handles during web navigation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A non-local or untrusted Owl Browser endpoint may receive browser actions, observations, page data, and bearer-token authenticated requests. <br>
Mitigation: Use localhost or HTTPS endpoints you control, protect OWL_API_TOKEN, and avoid entering sensitive credentials or private page data unless you trust the server. <br>


## Reference(s): <br>
- [Owl Browser homepage](https://www.owlbrowser.net) <br>
- [ClawHub skill page](https://clawhub.ai/ibnbd/owl-browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OWL_API_ENDPOINT, OWL_API_TOKEN, and curl; observations return OwlMark text and handle tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
