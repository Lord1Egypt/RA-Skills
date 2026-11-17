## Description:

Assess OT/ICS security posture across 30 controls in 6 principles: Business Driven, Risk Based, Enterprise Wide, Methodical, OT Security Focused, and OT Security Compliant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and OT teams use this skill to collect answers for OT/ICS controls, call the ToolWeb assessment API, and summarize compliance scores, risk level, gaps, and remediation priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends OT/ICS security posture and compliance information to a third-party paid API.

Mitigation: Use it only when organizational policy permits sharing this class of information with ToolWeb, and avoid entering site names, asset identifiers, network details, secrets, or other sensitive operational data unless approved.

Risk: The release evidence security verdict is suspicious because consent and data-handling disclosure are not clear for sensitive industrial-security assessment data.

Mitigation: Review ToolWeb retention, billing, and data-handling terms before use in real OT, ICS, manufacturing, utility, or critical-infrastructure environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/ot-security-assessment)
- [ToolWeb portal](https://portal.toolweb.in)
- [OT Security Assessment API endpoint](https://portal.toolweb.in/apis/security/ot-security-assessment)
- [ToolWeb platform](https://toolweb.in)
- [RapidAPI publisher profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with summarized scores, findings, remediation guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TOOLWEB_API_KEY; sends user-provided OT/ICS control responses to the ToolWeb API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
