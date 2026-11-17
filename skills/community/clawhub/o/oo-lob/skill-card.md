## Description:

Lob (lob.com). Use this skill for ANY Lob request — searching and reading data. Whenever a task involves Lob, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to search Lob data and autocomplete, verify, or standardize US and international postal addresses through an OOMOL-connected Lob account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup relies on remote installers that have not been inspected, and current publisher documentation does not establish which CLI release setup would install.

Mitigation: Review and approve CLI installation separately using a verified release.

Risk: Automatic skill management may make unexpected changes to other agent skills.

Mitigation: Check its behavior; set OO_SKILLS_SYNC_DISABLED=1 to suppress startup synchronization.

Risk: Address data is processed by OOMOL and Lob.

Mitigation: Share only addresses intended for those services to process.

## Reference(s):

- [Lob API Documentation](https://docs.lob.com/)
- [Lob](https://www.lob.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-lob)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON request and response examples with Markdown guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided address data for autocomplete and verification; responses include Lob result data and execution metadata.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
