## Description: <br>
MILKEE Swiss Accounting integrates with MILKEE accounting for Swiss businesses to manage projects, customers, time tracking, tasks, products, daily time summaries, and fuzzy project matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers with MILKEE accounts use this skill to let an agent run accounting and time-tracking workflows, including listing and updating projects, customers, tasks, products, and time entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MILKEE API token and company ID that can grant access to business accounting data. <br>
Mitigation: Install only from a trusted publisher, use a dedicated or least-privileged token if MILKEE supports it, keep credentials out of git, logs, screenshots, and shell history, and rotate any exposed token. <br>
Risk: Documentation includes realistic API-token examples that users could copy or accidentally expose. <br>
Mitigation: Replace all example values with real secrets only in private environment variables or local configuration, and never commit copied examples as active credentials. <br>
Risk: Create, update, and time-logging commands can change MILKEE account records. <br>
Mitigation: Review project, customer, task, product, and time-entry actions before allowing an agent to execute them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xenofex7/milkee) <br>
- [MILKEE API documentation](https://apidocs.milkee.ch/api) <br>
- [MILKEE authentication documentation](https://apidocs.milkee.ch/api/authentifizierung.html) <br>
- [MILKEE API v2 Endpoints Reference](references/api-endpoints.md) <br>
- [MILKEE Configuration Guide](references/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Plain text CLI output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MILKEE_API_TOKEN and MILKEE_COMPANY_ID environment variables; timer state may be stored in ~/.milkee_timer.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md author/version line) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
