## Description:

Use this skill to read, create, update, and delete OneSignal data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OneSignal messages and manage push notifications in their connected OneSignal account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include a downloaded CLI installer; the installer was not executed or directly inspected.

Mitigation: Review and approve CLI installation separately, including any bundled skill changes, before allowing automatic setup.

Risk: OOMOL mediates access to the connected OneSignal account and billing.

Mitigation: Consider account access and billing when connecting, and keep the required confirmation before sending or canceling messages.

## Reference(s):

- [OneSignal Skill Release](https://clawhub.ai/oomol/skills/oo-onesignal-rest-api)
- [OneSignal API Reference](https://documentation.onesignal.com/reference)
- [OneSignal](https://onesignal.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise natural language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation before execution.]

## Skill Version(s):

1.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
