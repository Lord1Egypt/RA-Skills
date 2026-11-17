## Description:

VirusTotal (virustotal.com). Use this skill for ANY VirusTotal request — reading, creating, and updating data. Whenever a task involves VirusTotal, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to retrieve and search VirusTotal reports, inspect related objects and community data, and submit files, URLs, or community contributions through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified remote installer, and the external installer and hosted implementation have not been verified.

Mitigation: Review and approve CLI installation separately; use a pinned, verified release and avoid automatic remote script execution.

Risk: File or URL submissions and community contributions send data to VirusTotal or change its state.

Mitigation: Confirm each exact submission or contribution and do not send confidential material without authorization.

## Reference(s):

- [VirusTotal API documentation](https://docs.virustotal.com/reference/authentication)
- [VirusTotal](https://www.virustotal.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON API results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and available actions depend on VirusTotal account permissions; submissions and community contributions can change external state.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
