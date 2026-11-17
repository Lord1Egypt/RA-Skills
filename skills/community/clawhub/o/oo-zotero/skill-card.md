## Description:

Zotero (zotero.org). Use this skill for ANY Zotero request — reading, creating, updating, and deleting data. Whenever a task involves Zotero, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and read their Zotero libraries and, when requested, create, update, or delete library items and collections. It asks for confirmation before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup can execute downloaded software without separate approval.

Mitigation: Review the CLI installation, verify the downloaded release, and review or disable automatic skill synchronization before first use.

Risk: Connecting Zotero authorizes OOMOL to access the connected Zotero account.

Mitigation: Connect the intended account and confirm write or destructive actions against the exact payload and target.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [Zotero Web API documentation](https://www.zotero.org/support/dev/web_api/v3/basics)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured Zotero data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, or delete Zotero library data; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
