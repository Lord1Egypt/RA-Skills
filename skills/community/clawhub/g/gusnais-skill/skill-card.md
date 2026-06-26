## Description: <br>
Gusnais Skill helps agents configure OAuth access to gusnais.com and perform permission-aware read and write operations across Gusnais/Homeland API domains including press, notes, jobs, site content, topics, users, replies, likes, photos, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GYURYONGKIM](https://clawhub.ai/user/GYURYONGKIM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to connect to Gusnais with CLIENT_ID and CLIENT_SECRET, exchange and refresh OAuth tokens, normalize API errors, and run permission-aware read, write, publish, update, and delete operations for supported community plugin domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth client credentials and grants account-level Gusnais API access. <br>
Mitigation: Use a dedicated OAuth client where possible, provide CLIENT_ID and CLIENT_SECRET through environment variables or a secret manager, and avoid sharing credentials in prompts, logs, or repositories. <br>
Risk: Refreshable OAuth tokens can be persisted in a local JSON token store for long-lived automation. <br>
Mitigation: Keep TOKEN_STORE_PATH outside source repositories and synced folders, restrict file access, and rotate or revoke tokens when access is no longer needed. <br>
Risk: The API client can perform write, delete, publish, and update actions on Gusnais resources. <br>
Mitigation: Review every mutating action before execution, use the least-privileged account that can complete the task, and rely on server abilities and status codes as the final authorization boundary. <br>
Risk: Some plugin API routes may be unavailable on a deployment. <br>
Mitigation: Treat unmounted plugin routes as resource_unavailable and avoid repeated retries against endpoints that return 404. <br>


## Reference(s): <br>
- [Gusnais API Endpoint Mapping](references/endpoints.md) <br>
- [Permission Parity Rules](references/permission-parity.md) <br>
- [Gusnais](https://gusnais.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/GYURYONGKIM/gusnais-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown guidance with Python helper scripts and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local OAuth token store JSON when TOKEN_STORE_PATH is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
