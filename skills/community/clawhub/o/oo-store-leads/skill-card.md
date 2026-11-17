## Description:

Search and read Store Leads data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search Store Leads and retrieve details about ecommerce apps, domains, and technologies through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs a remote CLI installer that was not audited.

Mitigation: Prefer a separately verified oo CLI installation and review the installer before using fallback setup.

Risk: Setup may install or synchronize other agent skills without explaining those broader changes.

Mitigation: Review and explicitly control any installation or synchronization of other agent skills.

Risk: The connected Store Leads account determines what data the skill can access.

Mitigation: Connect only the Store Leads access you intend OOMOL to use.

## Reference(s):

- [Store Leads](https://storeleads.app)
- [Store Leads API documentation](https://storeleads.app/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Data, JSON]

**Output Format:** [Structured Store Leads results returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records depend on the selected search or lookup action.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
