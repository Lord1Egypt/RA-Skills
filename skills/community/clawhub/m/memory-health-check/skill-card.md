## Description: <br>
Performs a 6-dimension OpenClaw memory health check for integrity, freshness, bloat, orphans, duplicates, and coverage, with optional repair recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw agents use this skill to inspect local memory stores, identify data quality and maintenance issues, generate health reports, and decide whether cleanup is appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional repair commands can delete local memory files. <br>
Mitigation: Run diagnostics first, use --dry-run before repair, and back up memory before deleting orphaned entries. <br>
Risk: The release advertises crypto and purchase-related capability tags, but the reviewed security guidance does not justify granting those authorities. <br>
Mitigation: Do not grant purchase or crypto authority for this skill unless a separate reviewed workflow requires it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chongjie-ran/memory-health-check) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [DESIGN.md](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Console text plus JSON and Markdown-style diagnostic reports with actionable repair guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inspects local OpenClaw memory paths and can optionally remove local cleanup targets when repair commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
