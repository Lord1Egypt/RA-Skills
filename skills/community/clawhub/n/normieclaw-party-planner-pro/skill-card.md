## Description: <br>
Organize party and event details from setup and guest lists to menus, timelines, budgets, vendors, and day-of logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People planning parties, gatherings, and events use this skill to structure event details, manage guests and dietary needs, track budgets, generate menus and timelines, coordinate vendors, and prepare day-of logistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store party details, guest contact information, dietary and allergy notes, venue addresses, vendor details, and budget data as local plaintext files. <br>
Mitigation: Install only where local plaintext storage is acceptable, restrict file access, avoid sharing reports until reviewed for private information, and consider device or disk encryption for sensitive guest lists. <br>
Risk: Setup and reporting scripts modify local skill data and generate exports. <br>
Mitigation: Review scripts before running setup, verify paths before uninstalling or deleting data, and inspect exported Markdown or report files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-party-planner-pro) <br>
- [README.md](README.md) <br>
- [SECURITY.md](SECURITY.md) <br>
- [CODEX-SECURITY-AUDIT.md](CODEX-SECURITY-AUDIT.md) <br>
- [dashboard-kit/manifest.json](dashboard-kit/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance with Markdown summaries, JSON event files, shell commands, and optional generated reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local event-planning data such as guest lists, budgets, menus, task timelines, vendor records, and reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
