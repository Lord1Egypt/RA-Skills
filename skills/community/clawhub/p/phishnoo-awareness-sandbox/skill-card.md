## Description:

Explore synthetic Phishnoo security-awareness metrics and submit example threat reports through the Phishnoo sandbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangpang83](https://clawhub.ai/user/pangpang83)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to inspect synthetic Phishnoo awareness metrics, campaign and progress data, and example threat reports. They can submit a synthetic example report when the user requests that write.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to the external Phishnoo sandbox service.

Mitigation: Use the named Phishnoo sandbox endpoint and avoid sending real employee records, actual messages, or live customer data.

Risk: The sandbox key could be exposed if handled as ordinary text.

Mitigation: Store PHISHNOO_SANDBOX_KEY in the client's secret settings and send it only as a Bearer authorization value; keep it out of URLs, command arguments, reports, and output.

Risk: Submitting a threat report writes data to the sandbox.

Mitigation: Call report_threat only when the user requests a write, and submit only synthetic example content without credentials or URL query and fragment data.

## Reference(s):

- [Phishnoo](https://phishnoo.com)
- [Phishnoo API documentation](https://api.phishnoo.nl/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Text or Markdown summaries and guidance based on synthetic sandbox data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and metrics are for synthetic sandbox data.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
