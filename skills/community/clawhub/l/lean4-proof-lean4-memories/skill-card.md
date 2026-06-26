## Description: <br>
This skill helps agents working on Lean 4 formalization projects maintain persistent memory of successful proof patterns, failed approaches, project conventions, and user preferences across sessions using MCP memory server integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during Lean 4 formalization work to recall project-specific proof strategies, avoid previously failed tactic paths, and keep reusable conventions across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memories can store project paths, theorem names, proof details, and preferences that may be sensitive. <br>
Mitigation: Use the skill only with a trusted MCP memory server, avoid storing secrets or confidential project identifiers, and periodically review or clear stored memories. <br>
Risk: Stored proof memories can become stale as a Lean 4 project evolves. <br>
Mitigation: Review older memories before relying on them, update records when better approaches are found, and remove memories for deleted or changed theorems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/lean4-proof-lean4-memories) <br>
- [memory-patterns.md](references/memory-patterns.md) <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/getting-started/intro) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Lean, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose memory records for proof patterns, failed approaches, project conventions, user preferences, and theorem dependencies.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
