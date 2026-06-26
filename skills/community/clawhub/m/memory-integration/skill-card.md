## Description: <br>
Memory Integration syncs OpenClaw memory files into co-occurrence and semantic-vector stores, then supports combined semantic and relationship-based memory search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to synchronize local memory files and improve recall with enhanced search across semantic-vector matches and co-occurrence relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw memory contents and some search-query context may be indexed into local co-occurrence or semantic-vector systems. <br>
Mitigation: Review the connected adapter plugins and their storage, retention, and deletion behavior before using the skill with sensitive memories. <br>
Risk: The integration depends on separate co-occurrence and optional semantic-vector adapters that determine where memory-derived data is stored. <br>
Mitigation: Install only trusted adapter implementations and confirm their configuration before running synchronization. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, and Python adapter usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can emit console summaries and Python dictionaries or lists for sync counts, memory statistics, and ranked search results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
