## Description:

Lets an agent search and read Baobiao procurement, company, contract, and project data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts can use the skill to search Baobiao procurement notices and company records, then read project, contract, buyer, and supplier information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an unexplained remote CLI installer that runs directly, and says fallback setup may install software without warning or approval. The fetched script's contents and effects are unknown, and two local references were unresolved during the partial scan.

Mitigation: Do not install until the publisher explains why the installer is needed and provides a verifiable installation method; review the unresolved references and remote script before use.

Risk: The list_company_contacts action can return personal contact details from notices.

Mitigation: Use returned contact information only for lawful business contact, as the skill directs.

## Reference(s):

- [Baobiao API documentation](https://console.woyaobid.com/gateway-admin/share/api-doc)
- [Baobiao homepage](https://www.woyaobid.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text, Structured data]

**Output Format:** [Markdown guidance with shell commands; Baobiao action results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and by the data and permissions available to the connected Baobiao account.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
