## Description: <br>
Compresses verbose markdown memory logs into structured summaries that preserve key events, lessons, decisions, and todos without external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LingLin6](https://clawhub.ai/user/LingLin6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents with markdown-based memory systems use this skill to compress daily memory logs into curated summaries before appending them to long-term memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script reads selected memory log files and may process sensitive memory content. <br>
Mitigation: Run it only on intended markdown logs, avoid broad or sensitive paths, and review generated summaries before appending them to long-term memory. <br>
Risk: The compressed summary is a best-effort reduction and may omit nuance from the original log. <br>
Mitigation: Compare the summary against the source log for important decisions, lessons, and todos before treating it as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LingLin6/memory-compress) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a selected markdown log and writes a compressed summary file; default output is /tmp/compressed-memory.md.] <br>

## Skill Version(s): <br>
1.2.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
