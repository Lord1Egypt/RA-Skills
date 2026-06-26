## Description: <br>
Use when researching, scoring, planning allocations, or generating trade plans for public markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Rally to research public-market candidates, score investment signals, create constrained long-only allocation plans, derive trade plans, and generate portfolio reports. It is intended for governed portfolio planning with risk checks, not for hype-driven speculation, margin trading, or personal budget planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rally can create scheduled jobs, including a daily self-update that may replace reviewed skill files from GitHub. <br>
Mitigation: Review or disable the rally:update cron job before use, and require review of updates before relying on changed skill behavior. <br>
Risk: Trade execution exists as a command path and could affect brokerage accounts if intentionally enabled. <br>
Mitigation: Keep execution disabled unless brokerage integration is deliberately configured and reviewed; treat generated trade plans as proposals until approved. <br>
Risk: Rally stores portfolio state, decisions, trade plans, and journals as local financial records. <br>
Mitigation: Protect the Rally data and journal directories with appropriate local access controls and retention practices. <br>


## Reference(s): <br>
- [Rally ClawHub Skill Page](https://clawhub.ai/indigokarasu/ocas-rally) <br>
- [README](artifact/README.md) <br>
- [Rally Data Model](artifact/references/data-model.md) <br>
- [Journal](artifact/references/journal.md) <br>
- [Rally Operating Model](artifact/references/operating-model.md) <br>
- [Rally Research and Scoring](artifact/references/research-and-scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON/JSONL planning records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local portfolio state, research events, signals, decisions, allocation plans, trade plans, reports, and journals under the configured Rally data and journal directories.] <br>

## Skill Version(s): <br>
3.0.1 (source: server evidence release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
