## Description: <br>
Family health management suite: health records, diet tracking, weight management, wearable sync. Local SQLite storage by default; optional cloud features require explicit setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juneyaooo](https://clawhub.ai/user/juneyaooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and families use this skill in OpenClaw to record health data, manage family health profiles, track diet and weight, sync wearable data, and prepare summaries for medical visits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and processes sensitive medical records, attachments, backups, reports, and wearable configuration data. <br>
Mitigation: Use a dedicated, isolated health workspace and treat generated databases, attachments, exports, and backups as sensitive medical data. <br>
Risk: Shared or group-bot deployments can expose one user's health data to another user if owner_id isolation is not enforced. <br>
Mitigation: Avoid shared deployments unless owner_id is enforced fail-closed and each user has a separate data scope. <br>
Risk: Optional external services can transmit health records, images, text fragments, food queries, or wearable data outside the local machine. <br>
Mitigation: Enable DDInter, vision or LLM providers, embeddings, USDA, backend APIs, and wearable sync only after confirming what data leaves the machine and trusting the configured endpoint. <br>
Risk: Credential and token handling is involved for optional API keys and wearable integrations. <br>
Mitigation: Enter passwords and API keys only through local terminal setup flows, never in chat, and keep generated token stores private. <br>
Risk: Attachment or file-serving features may expose private health files if bound publicly. <br>
Mitigation: Keep attachment serving local or access-controlled and do not bind it to public interfaces. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/juneyaooo/mediwise-health-suite) <br>
- [Project homepage](https://github.com/JuneYaooo/mediwise-health-suite) <br>
- [Cycle, Attachments, and Multi-Tenancy](mediwise-health-tracker/references/cycle-attachments-multitenancy.md) <br>
- [Drug Safety and Briefing](mediwise-health-tracker/references/drug-briefing.md) <br>
- [Intake, Query, and Vision](mediwise-health-tracker/references/intake-query-vision.md) <br>
- [Visit Preparation Summary](mediwise-health-tracker/references/visit-prep.md) <br>
- [Health Management Overview](docs/HEALTH-MANAGEMENT-OVERVIEW.md) <br>
- [Installation Guide](docs/INSTALLATION.md) <br>
- [Agent Setup Guide](docs/AGENT_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional shell commands, generated reports, exported files, and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite records, reports, backups, attachments, and wearable sync artifacts in the configured health workspace] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
