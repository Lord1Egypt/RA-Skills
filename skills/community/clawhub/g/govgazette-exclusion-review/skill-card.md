## Description:

Check GovGazette for a possible federal exclusion, debarment, or suspension match and review the supporting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, compliance, and contracting teams can use this skill to check supplied identities against federal exclusion, debarment, or suspension records and review supporting sources. It helps explain possible matches and the limits of the available evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Names and identifiers supplied for a lookup are sent to GovGazette.

Mitigation: Submit only information you are authorized to share and keep confidential material out of queries.

Risk: A possible match or incomplete record could be mistaken for a conclusive exclusion finding.

Mitigation: Verify official records and supporting sources, preserve freshness warnings, and explain identity uncertainty before relying on a result.

## Reference(s):

- [GovGazette exclusion records](https://govgazette.com)
- [GovGazette MCP connection](https://govgazette.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary of identity evidence, record status, dates, restriction type, agency, official links, and uncertainty]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves freshness warnings and limits conclusions to possible matches; a no-match result does not establish eligibility.]

## Skill Version(s):

1.3.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
