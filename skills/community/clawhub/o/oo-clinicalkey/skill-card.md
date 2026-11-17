## Description:

Search and read ClinicalKey data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

ClinicalKey customers and their agents can check service status, find available COUNTER 5.1 reports or consortium members, and retrieve usage reports through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute downloaded code, and automatic skill synchronization may introduce changes to other agent skills.

Mitigation: Review and approve CLI setup separately, prefer a verified fixed release, and consider disabling automatic synchronization with the publisher-documented OO_SKILLS_SYNC_DISABLED setting.

Risk: Exact installer behavior and server-side credential handling have not been verified.

Mitigation: Review the setup and account connection before use, and avoid relying on undocumented credential-handling assumptions.

## Reference(s):

- [ClinicalKey](https://www.clinicalkey.com/)
- [ClinicalKey COUNTER 5.1 API documentation](https://dev.elsevier.com/sushicop5.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use live connector schemas; responses include data and execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
