## Description:

Search Have I Been Pwned for breach and paste exposure data, and retrieve breach and subscription information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to check email addresses for known breach or paste exposures and to review breach details, data classes, and subscription status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a downloaded CLI installer, and the linked CLI documents broader persistent changes to agent skills.

Mitigation: Review and independently verify the installer before use; decide whether managed skill changes are acceptable and consult the CLI's OO_SKILLS_SYNC_DISABLED control.

Risk: Email addresses submitted for lookups are shared through OOMOL with Have I Been Pwned.

Mitigation: Submit only email addresses you intend to share with those services, and limit access to returned exposure details.

## Reference(s):

- [Have I Been Pwned](https://haveibeenpwned.com/)
- [Have I Been Pwned API documentation](https://haveibeenpwned.com/API/v3)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured breach and paste exposure data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can contain sensitive personal information.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
