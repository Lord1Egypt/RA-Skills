## Description: <br>
Helps agents inspect and maintain existing long-term memory stores by reporting memory health issues and offering snapshot-backed index reconciliation for supported formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check and tidy an existing LLM-agent memory store before memory drift, stale notes, dead links, or index drift degrade agent behavior. It supports read-only reports by default and deterministic index reconciliation when explicitly run with a fix option. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-chosen memory directory and can expose sensitive memory content in reports or terminal output. <br>
Mitigation: Run it only on memory directories the user intends to inspect, and review report output before sharing it. <br>
Risk: Using the fix option rewrites the MEMORY.md index for supported auto-memory stores. <br>
Mitigation: Run report and lint first, review the dry-run plan, and use --fix only when the user wants the index rewritten. <br>
Risk: The bundled snapshot is not a full recursive backup of every possible memory-store file. <br>
Mitigation: Keep an independent backup for important memory stores before applying fixes. <br>


## Reference(s): <br>
- [memory-doctor ClawHub release](https://clawhub.ai/casperkwok/memory-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown health reports, terminal output, and snapshot-backed file updates when fixes are requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with no LLM dependency; report and lint are read-only unless the user applies fixes.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
