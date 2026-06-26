## Description: <br>
Project Manager Pro helps agents create, organize, prioritize, decompose, review, and export local task and project data through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users add, update, break down, prioritize, review, and export personal task and project records through an OpenClaw-compatible conversational agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script may install jq through the user's system package manager and create files under ~/.openclaw/workspace/pm-pro. <br>
Mitigation: Review setup.sh before running it, install jq manually if preferred, and run setup only in an environment where creating the local task workspace is acceptable. <br>
Risk: The weekly review script can archive completed tasks and rewrite the active task list. <br>
Mitigation: Back up the pm-pro data directory and review weekly-review.sh behavior before enabling scheduled or automated reviews. <br>
Risk: Task content, exports, and cross-tool notes may contain sensitive personal or work information in plain text. <br>
Mitigation: Avoid storing secrets or highly sensitive details, use disk encryption where appropriate, and handle exported markdown, CSV, and JSON files as sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/project-manager-pro) <br>
- [README.md](artifact/README.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown conversation responses, shell command suggestions, JSON-backed task records, and optional markdown/CSV/JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files under ~/.openclaw/workspace/pm-pro and optional Bash helper scripts for setup, export, and weekly review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/config/settings.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
