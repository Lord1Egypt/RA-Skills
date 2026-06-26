## Description: <br>
Lightweight memory consolidation for OpenClaw agents that reviews recent daily memory files, extracts durable knowledge, and merges it into MEMORY.md without imposing a new file architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balukov](https://clawhub.ai/user/balukov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep long-term MEMORY.md current by distilling durable facts, preferences, decisions, and corrections from recent daily memory journals. It is suitable for manual consolidation runs or a simple scheduled job after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory updates may preserve incorrect, stale, or overly broad information if consolidation is run without review. <br>
Mitigation: Run the skill manually first, review diffs to MEMORY.md, and keep edits surgical and conservative. <br>
Risk: Memory summaries may accidentally retain sensitive details from daily journals. <br>
Mitigation: Avoid leaking secrets into reports or memory summaries, and review consolidated entries before unattended scheduling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balukov/memory-sleep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown edits to MEMORY.md, optional Markdown journal note, and a short text run summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally add a concise consolidation marker to daily journal files; journal files should not be deleted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
