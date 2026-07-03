## Description: <br>
Harvest every ponytail: shortcut comment into one debt ledger, so deferrals get tracked instead of forgotten. One-shot report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dietrichgebert](https://clawhub.ai/user/dietrichgebert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan a repository for deliberate `ponytail:` shortcut comments and turn them into a grouped debt ledger. It helps teams track ceilings, upgrade triggers, and missing trigger information without changing source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ledger may omit debt markers if a repository uses comment prefixes beyond the documented grep pattern. <br>
Mitigation: Extend the search pattern for the repository's languages before treating the ledger as complete. <br>
Risk: Rows without an upgrade trigger can silently become stale process debt. <br>
Mitigation: Review entries tagged no-trigger and add a concrete revisit trigger before relying on the ledger for planning. <br>
Risk: Persisting the ledger writes a new repository file when explicitly requested. <br>
Mitigation: Review the requested output path and generated markdown before committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dietrichgebert/skills/ponytail-debt) <br>
- [Homepage](https://github.com/DietrichGebert/ponytail) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, files] <br>
**Output Format:** [Markdown ledger with repository file and line references; optionally a persisted markdown file when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports marker totals and tags entries with missing upgrade triggers as no-trigger.] <br>

## Skill Version(s): <br>
4.8.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
