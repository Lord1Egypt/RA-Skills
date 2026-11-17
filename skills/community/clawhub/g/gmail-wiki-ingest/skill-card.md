## Description:

Triage recent Gmail threads against a user's personal wiki and submit verdicts for server-managed ingestion, review, or discard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users triage recent Gmail correspondence into their personal wiki, with review cards for items requiring approval and a digest of each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Gmail metadata daily and may read full correspondence from up to 12 threads per run.

Mitigation: Enable Gmail ingest only if this access is wanted, and confirm the Google permission is read-only.

Risk: Incorrect verdicts could surface irrelevant correspondence for review or lead to unwanted wiki entries for previously trusted senders.

Mitigation: Review candidate cards and digest results; discard unwanted items and disable Gmail ingest in HiJavis when no longer needed.

## Reference(s):

- [Judgment rubric](rubric.md)
- [Tool contract](references/tool-contract.md)
- [Banding and sender trust](references/banding-and-trust.md)
- [Trigger contract](references/trigger-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Thread verdicts and a Markdown chat digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most 12 full email threads read per run; the server controls wiki writes.]

## Skill Version(s):

0.5.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
