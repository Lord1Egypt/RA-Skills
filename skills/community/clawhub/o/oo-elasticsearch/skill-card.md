## Description:

Elasticsearch (elastic.co). Use this skill for ANY Elasticsearch request — reading, creating, updating, and deleting data. Whenever a task involves Elasticsearch, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect, search, index, update, reindex, and manage Elasticsearch data and clusters through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup runs remote code and may introduce broader agent changes, including synchronized skills.

Mitigation: Review and approve the CLI installation and any skill synchronization separately, and use a verified release before enabling the skill.

Risk: Write and deletion actions can change or remove Elasticsearch data, and a timed-out deletion may continue running.

Mitigation: Confirm the exact payload and effect before writes or deletions, use narrowly scoped credentials, and do not blindly retry a timed-out deletion.

Risk: Elasticsearch access is mediated by OOMOL, which may not suit every data-handling requirement.

Mitigation: Assess whether OOMOL-mediated access is appropriate for the data before connecting Elasticsearch.

## Reference(s):

- [Elasticsearch](https://www.elastic.co/elasticsearch)
- [Elasticsearch API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON request and response data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by Elasticsearch action.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
