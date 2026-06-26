## Description: <br>
Connect to Civic MCP for 100+ integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[civictechuser](https://clawhub.ai/user/civictechuser) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to discover and call Civic MCP tools for connected services such as email, databases, storage, and other integrations from an OpenClaw workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad token-backed access to connected services. <br>
Mitigation: Use a least-privilege Civic profile, verify CIVIC_URL before use, and protect and rotate CIVIC_TOKEN. <br>
Risk: Tool calls may send messages, modify files, write or delete records, run SQL, or change connected services. <br>
Mitigation: Inspect tool schemas and require explicit user approval before any operation that changes data or external services. <br>
Risk: Some tools require OAuth authorization flows before execution can continue. <br>
Mitigation: Show the authorization URL to the user and continue only after the user completes the expected authorization step. <br>


## Reference(s): <br>
- [Civic documentation](https://docs.civic.com) <br>
- [Civic Nexus](https://nexus.civic.com) <br>
- [ClawHub release page](https://clawhub.ai/civictechuser/openclaw-civic-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline JSON and bash examples; Civic tool calls may return plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CIVIC_URL and CIVIC_TOKEN, plus mcporter or npx/tsx for execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
