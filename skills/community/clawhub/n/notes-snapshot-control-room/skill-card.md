## Description: <br>
Helps agents connect Apple Notes Snapshot to local hosts by proving notesctl preflight state, wiring notesctl mcp, and keeping AI Diagnose, Local Web API, MCP, and attach proof boundaries distinct. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and local-agent users use this skill to guide Apple Notes Snapshot setup, local proof checks, host MCP configuration, and troubleshooting without overstating hosted-service or universal attach claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can direct a local agent to run an external Apple Notes tool. <br>
Mitigation: Review the referenced notesctl repository and require the agent to show exact commands before execution. <br>
Risk: The install/load path can create a recurring local backup job. <br>
Mitigation: Allow the install/load step only after confirming the user wants a recurring backup job and understands how to disable or remove it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/notes-snapshot-control-room) <br>
- [Install And Attach](references/install-and-attach.md) <br>
- [Usage And Proof](references/usage-and-proof.md) <br>
- [Apple Notes Snapshot landing page](https://xiaojiou176-open.github.io/apple-notes-snapshot/) <br>
- [Apple Notes Snapshot quickstart](https://xiaojiou176-open.github.io/apple-notes-snapshot/quickstart/) <br>
- [Apple Notes Snapshot proof page](https://xiaojiou176-open.github.io/apple-notes-snapshot/proof/) <br>
- [Apple Notes Snapshot MCP guide](https://xiaojiou176-open.github.io/apple-notes-snapshot/mcp/) <br>
- [Apple Notes Snapshot for agents](https://xiaojiou176-open.github.io/apple-notes-snapshot/for-agents/) <br>
- [Public skills pack docs](https://xiaojiou176-open.github.io/apple-notes-snapshot/for-agents/public-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local preflight steps, MCP host wiring guidance, capability-boundary explanations, and troubleshooting recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
