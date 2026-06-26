## Description: <br>
Searches M-Flow memory for a user query, formats relevant results as wiki entries, and saves them for later knowledge compilation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn M-Flow memory search results into Markdown wiki entries that can be reused in later knowledge compilation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory search results and query-derived content may be persisted into local wiki files. <br>
Mitigation: Use the skill only when persistent storage is acceptable, avoid sensitive queries, and periodically review generated knowledge/wiki/ files. <br>
Risk: The skill depends on the m-flow-memory dependency for search behavior and stored memory access. <br>
Mitigation: Install and trust m-flow-memory in the target environment before use, and review its behavior for the data being queried. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sora-mury/karpathy-query-feedback) <br>
- [Publisher profile](https://clawhub.ai/user/sora-mury) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown wiki tables, JSON result summaries, Python API objects, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes query results to local wiki files under knowledge/wiki/ when entries are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
