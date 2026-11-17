## Description:

TelTel (teltel.io). Use this skill for ANY TelTel request — reading, creating, and updating data. Whenever a task involves TelTel, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and TelTel account users use this skill to check account balances and SMS delivery reports, list reports, and send SMS through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses remote installers that were unavailable for inspection.

Mitigation: Review and install the oo CLI separately before allowing automated setup.

Risk: Startup synchronization can make broader, persistent changes to agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if you do not want those skill changes.

Risk: Sending SMS contacts a recipient and may incur account costs.

Mitigation: Approve the recipient, message contents, and cost before sending.

## Reference(s):

- [TelTel](https://www.teltel.io)
- [TelTel API documentation](https://apidoc.teltel.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON results with concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain account balance, SMS report, or send-result data.]

## Skill Version(s):

1.0.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
