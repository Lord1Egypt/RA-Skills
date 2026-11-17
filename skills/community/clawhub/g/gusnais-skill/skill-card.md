## Description:

Gusnais Skill helps agents connect to the Gusnais API with OAuth credentials, discover platform settings, preserve web permission behavior, and perform read/write operations for press, note, jobs, and site domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyuryongkim](https://clawhub.ai/user/gyuryongkim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to connect to Gusnais with OAuth credentials, discover API settings, and perform read or write operations for community content, press posts, notes, jobs, and site entries while preserving server permission behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable OAuth credentials and can persist tokens in a local plaintext JSON store.

Mitigation: Use a private token-store path outside shared directories, restrict file permissions, and rotate or revoke tokens if the file may have been exposed.

Risk: The skill can perform content-changing actions such as create, update, publish, and delete operations.

Mitigation: Review intended actions before execution and treat delete, publish, and update operations as potentially public or irreversible.

Risk: Some plugin API routes may be unavailable on a deployment.

Mitigation: Treat 404 responses from plugin routes as resource_unavailable and avoid repeated retries against unmounted endpoints.

## Reference(s):

- [Gusnais API Endpoint Mapping](references/endpoints.md)
- [Permission Parity Rules](references/permission-parity.md)
- [Gusnais](https://gusnais.com)
- [ClawHub Skill Page](https://clawhub.ai/gyuryongkim/skills/gusnais-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python helper scripts, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API actions normalize status, reason, data, capability, and request details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
