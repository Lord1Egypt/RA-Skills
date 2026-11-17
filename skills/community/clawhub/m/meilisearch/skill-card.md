## Description:

Deploy and tune Meilisearch with indexing, filtering, and production configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill for concise operational guidance on configuring Meilisearch indexes, search behavior, API keys, backups, and production limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect production key handling could expose privileged Meilisearch access.

Mitigation: Verify master key configuration, use search-only frontend keys, and avoid exposing privileged keys in client-side code.

Risk: Operational guidance may not match a user's deployment constraints for backups, reindexing, or capacity.

Mitigation: Review backup schedules, settings changes, batch sizes, and RAM requirements against the target environment before applying changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plain-text operational checklist; no executable files or tool calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
