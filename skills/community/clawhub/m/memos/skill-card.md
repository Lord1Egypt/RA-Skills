## Description:

Manage memos through the Memos API by creating, retrieving, deleting, and listing memos with visibility and pagination support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fty4](https://clawhub.ai/user/fty4)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an agent to a configured Memos instance for creating, reading, deleting, and listing memos. It is suited for workflows that need authenticated memo management through the Memos API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured MEMOS_URL or overly broad MEMOS_TOKEN could expose memo data or mutate the wrong Memos instance.

Mitigation: Use a trusted HTTPS Memos URL, provide a narrowly scoped token, and confirm the configured instance before running create, list, delete, or force-delete operations.

Risk: New memos default to PUBLIC visibility and delete operations can remove remote memo content.

Mitigation: Select PRIVATE or PROTECTED visibility for non-public content and verify memo IDs before using delete or force-delete.

## Reference(s):

- [Memos API documentation](https://usememos.com/docs/api)
- [ClawHub Memos skill page](https://clawhub.ai/fty4/skills/memos)
- [Publisher profile](https://clawhub.ai/user/fty4)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration instructions]

**Output Format:** [JSON API responses and errors, with Markdown memo links when referenced in agent output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMOS_URL and MEMOS_TOKEN environment variables; create defaults memo visibility to PUBLIC unless another visibility is supplied.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
