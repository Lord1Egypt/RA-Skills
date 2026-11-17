## Description:

Looks up IP address and ASN information through ipdata.co, including location, network, and threat data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve location, network, threat, and ASN information for IP addresses through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code without verification or a clear user checkpoint; the remote installer could not be inspected and hosted connector code is not bundled.

Mitigation: Review and install a specific, verified CLI release separately, and check its automatic skill-management behavior.

Risk: Lookup parameters pass through OOMOL to ipdata.co and may consume account credit.

Mitigation: Review lookup inputs and expected account-credit use before running lookups, especially bulk requests.

## Reference(s):

- [ipdata.co](https://ipdata.co)
- [ipdata.co API authentication documentation](https://docs.ipdata.co/reference/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OOMOL ipdata.co connection setup](https://console.oomol.com/connections/ipdata_co)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON and text fields returned by ipdata.co lookup actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields depend on the selected action; bulk_lookup supports up to 100 IP addresses.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
