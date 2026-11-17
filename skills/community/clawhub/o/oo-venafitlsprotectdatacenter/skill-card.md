## Description:

Use the oo CLI to search and read Venafi TLS Protect Datacenter certificate and policy data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and certificate administrators use this skill to check effective certificate policies and retrieve or list certificates in a connected Venafi TLS Protect Datacenter account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded software whose installer and backend effects have not been fully verified.

Mitigation: Review and approve CLI installation separately before setup, and use a verified release.

Risk: Credentials and certificate data are handled through the OOMOL-connected account.

Mitigation: Use a read-only Venafi connection and assess whether OOMOL is an appropriate party to handle the credentials and certificate data.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CyberArk Certificate Manager Self-Hosted product information](https://www.cyberark.com/resources/product-datasheets/cyberark-certificate-manager-self-hosted)
- [Venafi Web SDK REST API reference](https://docs.venafi.com/Docs/current/TopNav/Content/SDK/WebSDK/cco-sdk-REST-API-reference.php)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only certificate and policy data; available fields depend on the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
