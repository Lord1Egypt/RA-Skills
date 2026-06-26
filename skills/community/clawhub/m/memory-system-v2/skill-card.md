## Description: <br>
Memory System V2 helps agents capture and search persistent learnings, decisions, insights, events, and interactions using a bash and jq file-backed JSON index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External developers and agent operators use this skill to add a local persistent memory store for agent sessions, including capture, search, recent-memory retrieval, stats, and weekly consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory entries may retain sensitive content in plaintext under $HOME/clawd/memory. <br>
Mitigation: Do not capture secrets, credentials, regulated personal data, or confidential details unless plaintext local storage is acceptable; review and delete old memories periodically. <br>
Risk: Recalled memories may be stale or conflict with current user instructions or verified files. <br>
Mitigation: Treat recalled memories as context, not authority, and prefer current user instructions and verified workspace files when they differ. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kellyclaudeai/memory-system-v2) <br>
- [Memory System V2 design document](docs/memory-system-v2-design.md) <br>
- [Memory System V2 test results](docs/memory-system-v2-test-results.md) <br>
- [Memory System V2 homepage](https://github.com/austenallred/memory-system-v2) <br>
- [jq dependency install metadata](metadata/clawdis) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the CLI writes Markdown logs and JSON indexes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and jq; stores memory files under $HOME/clawd/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
