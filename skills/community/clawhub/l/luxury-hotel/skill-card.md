## Description: <br>
Discovers premium 5-star hotels and luxury resorts through flyai CLI searches, with booking links and real-time pricing when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agents use this skill to collect destination and date parameters, run flyai hotel searches, and present top-rated luxury hotel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party flyai CLI and may install it globally before answering travel requests. <br>
Mitigation: Review and install a trusted flyai CLI version before use; do not allow automatic global installs unless approved. <br>
Risk: Travel queries and command activity may be sent to the flyai service and saved locally in an execution log. <br>
Mitigation: Use only when sharing travel-search details with the provider is acceptable, and disable or delete `.flyai-execution-log.json` when those details are sensitive. <br>


## Reference(s): <br>
- [Luxury Hotel ClawHub page](https://clawhub.ai/dingtom336-gif/luxury-hotel) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Luxury hotel playbooks](references/playbooks.md) <br>
- [Hotel-search fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with hotel comparison tables, booking links, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the data source; may append execution logs when file-system writes are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
