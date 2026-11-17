## Description:

Search and read MxToolbox DNS, email security, network, monitor, and account usage data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and email or network operators use this skill to inspect DNS, email authentication, blacklist, SMTP and HTTP, ping, monitor, and usage information in MxToolbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded installation scripts without separate approval or verification.

Mitigation: Install the CLI separately from a reviewed, verified release and require approval for setup changes.

Risk: MxToolbox requests may consume paid credits.

Mitigation: Review account usage and billing before running lookups that may incur charges.

## Reference(s):

- [MxToolbox](https://mxtoolbox.com)
- [MxToolbox API documentation](https://knowledgebase.mxtoolbox.com/home/about-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text]

**Output Format:** [Structured MxToolbox response data (JSON) and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected lookup and connected MxToolbox account.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
