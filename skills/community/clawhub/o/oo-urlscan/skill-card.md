## Description:

Use urlscan.io to retrieve scan results, search scans, and submit URLs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search urlscan.io, retrieve completed scan results, and submit URLs for scanning through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes remote software whose automatic skill synchronization settings can affect other installed agents; installer behavior was not verified.

Mitigation: Review the CLI installation source and inspect its skill synchronization settings before allowing setup to run.

Risk: Submitting a URL sends a scan payload through OOMOL and its scan visibility may expose the submitted URL or results.

Mitigation: Confirm the exact URL and intended scan visibility before submitting.

## Reference(s):

- [urlscan.io API documentation](https://urlscan.io/docs/api/)
- [urlscan.io](https://urlscan.io)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON scan results and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports scan retrieval, search, and URL submission.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
