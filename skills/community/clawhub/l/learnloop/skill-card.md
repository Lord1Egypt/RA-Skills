## Description: <br>
Continuous learning protocol for Claude that captures corrections, errors, and user preferences into native auto-memory so the next session remembers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use Learnloop to preserve high-value corrections, preferences, project facts, and reference pointers across sessions. It helps agents decide when to save a memory, classify it, update the MEMORY.md index, and verify recalled facts before acting on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist preferences, corrections, and project context into future sessions, including sensitive information if saved carelessly. <br>
Mitigation: Do not save secrets, credentials, regulated data, sensitive personal details, or confidential business context unless retention is intentional; periodically review, edit, or delete saved memories. <br>
Risk: Outdated or incorrect memories can influence later agent behavior. <br>
Mitigation: Verify file paths, commands, symbols, and repo state before acting on recalled memories, and update or delete stale entries. <br>


## Reference(s): <br>
- [Learnloop ClawHub page](https://clawhub.ai/skills/learnloop) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown memory entries and concise status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Claude Code memory files and updates the MEMORY.md index when a memory is saved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
