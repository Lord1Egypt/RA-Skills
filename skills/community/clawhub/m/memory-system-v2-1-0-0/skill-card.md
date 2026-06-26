## Description: <br>
Fast semantic memory system with JSON indexing, auto-consolidation, and sub-20ms search for capturing learnings, decisions, insights, events, and interactions across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and AI agent operators use this skill to give agents persistent local memory for prior work, decisions, learnings, events, and interaction history. It supports capture, search, recent-memory lookup, statistics, and weekly consolidation through a Bash and jq CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local persistent memory can retain sensitive notes if users choose to store them. <br>
Mitigation: Avoid storing secrets, credentials, health, financial, legal, or highly personal data, and review $HOME/clawd/memory periodically. <br>
Risk: Broad auto-capture or automatic recall can cause stored history to be reused in later sessions. <br>
Mitigation: Enable broad capture or recall rules only when that reuse is intended, and prune local memory files when context should no longer be available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sieyer/memory-system-v2-1-0-0) <br>
- [Memory System v2 design document](docs/memory-system-v2-design.md) <br>
- [Memory System v2 test results](docs/memory-system-v2-test-results.md) <br>
- [jq dependency](https://formulae.brew.sh/formula/jq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash CLI commands and local JSON/Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and writes persistent memory data under $HOME/clawd/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
