## Description:

Operate Rapid URL Indexer through an OOMOL-connected account to read, create, and update indexing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit URLs for indexing and inspect project progress, reports, and credit balance through their connected Rapid URL Indexer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs downloaded CLI code that has not been verified, and automatic skill synchronization may change agent skills without disclosing the full scope of those changes.

Mitigation: Review and install a verified CLI release, and check its automatic skill synchronization settings before use.

Risk: Submitted URLs pass through OOMOL, and confirmed indexing submissions can spend credits.

Mitigation: Connect only the intended account and review the URLs and associated credit costs before confirming a submission.

## Reference(s):

- [Rapid URL Indexer homepage](https://rapidurlindexer.com/)
- [Rapid URL Indexer API documentation](https://rapidurlindexer.com/indexing-api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Indexing status and reports are returned as action results; indexing can take up to 14 days.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
