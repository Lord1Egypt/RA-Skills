## Description:

Automates Linear.app workflows in the OpenClaw-managed browser profile using browser actions for triage, issue updates, comments, filtering, bulk state changes, and visual verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hassam-powerhouse](https://clawhub.ai/user/hassam-powerhouse)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate Linear issue triage, issue creation, issue editing, state changes, comments, bulk updates, and visual verification through a logged-in managed browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make changes in a logged-in Linear workspace through the managed browser.

Mitigation: Install only if you are comfortable with that access, and review requested issue targets before confirming changes.

Risk: Bulk triage or state-change requests could affect multiple issues or the wrong issue if target details are ambiguous.

Mitigation: The artifact requires explicit team, issue, state, and comment details, candidate-list confirmation for bulk updates, fresh snapshots, and post-action verification.

Risk: Unauthenticated sessions or MFA prompts can interrupt browser automation.

Mitigation: The workflow routes unauthenticated sessions to Linear login, asks the user to complete authentication, and resumes after dashboard state is visible.

## Reference(s):

- [Linear Browser Workflows](references/workflows.md)
- [Selectors and Fallbacks](references/selectors-and-fallbacks.md)
- [Linear](https://linear.app/)
- [Linear Login](https://linear.app/login)
- [ClawHub Skill Page](https://clawhub.ai/hassam-powerhouse/skills/linear-browser-automation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries with browser-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Linear workspace in the OpenClaw-managed browser profile.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
