## Description:

Auto-apply JD.com (京东) price protection on all eligible orders by connecting to Chrome through OpenClaw Browser Relay CDP, opening the JD price protection page, clicking visible "申请价保" buttons, and reporting refund results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwangyy](https://clawhub.ai/user/danielwangyy)

### License/Terms of Use:


## Use Case:

External users and shopping automation agents use this skill to check logged-in JD.com orders for eligible price-protection refunds and submit matching price-protection requests. It is intended for agents that can run the included Node.js script against a user's connected Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in JD.com browser session and submits all visible price-protection requests automatically.

Mitigation: Run it manually first and review the JSON output before enabling scheduled or silent operation.

Risk: Scheduled use can perform unattended account actions through the local browser relay.

Mitigation: Use scheduled mode only when the user is comfortable with unattended JD.com account actions and local relay-token access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielwangyy/skills/jd-price-protect)
- [JD.com price protection portal](https://pcsitepp-fm.jd.com/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON results from the Node.js automation script, with optional agent-facing notification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports totals, clicked request count, pages checked, successful refunds with amounts, and failed requests with reasons.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
