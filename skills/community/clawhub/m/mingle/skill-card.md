## Description: <br>
Agent-powered professional networking inside your chat for finding collaborators, co-founders, freelancers, and experts through double opt-in introductions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoess](https://clawhub.ai/user/aeoess) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Mingle to let an assistant search a shared professional network, draft networking cards, surface relevant matches, and coordinate double opt-in introductions after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an assistant to Mingle's remote professional-networking service. <br>
Mitigation: Install and enable it only when that connection is intended, and review the remote service use before approving cards or introductions. <br>
Risk: Published cards or intro messages may disclose sensitive professional context if the user approves overly specific details. <br>
Mitigation: Review every draft and intro before approval, omit confidential details, and generalize company names, financial details, credentials, and personal contact information. <br>
Risk: Networking cards can become stale while remaining discoverable. <br>
Mitigation: Remove or update stale cards when the user no longer wants to be discoverable for that topic. <br>


## Reference(s): <br>
- [Mingle on ClawHub](https://clawhub.ai/aeoess/mingle) <br>
- [Mingle MCP npm package](https://www.npmjs.com/package/mingle-mcp) <br>
- [Mingle landing page](https://aeoess.com/mingle.html) <br>
- [Mingle API endpoint](https://api.aeoess.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; agent responses may include match summaries and intro drafts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and connects to the Mingle remote networking service when its MCP tools are used.] <br>

## Skill Version(s): <br>
2.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
