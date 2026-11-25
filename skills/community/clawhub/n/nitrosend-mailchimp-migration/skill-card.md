## Description:

Migrate from Mailchimp to Nitrosend by bringing audiences, members, merge fields, and consent statuses across, then rebuilding the campaigns and customer journeys still needed as Nitrosend emails and flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

External teams moving email marketing from Mailchimp to Nitrosend use this skill to preserve opt-outs and suppression status, connect the accounts, and identify which campaigns and customer journeys to rebuild.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opt-outs, bounced addresses, or spam complaints could be missed and receive email if suppression records are not carried over before sending.

Mitigation: Import the relevant suppression files before connecting, spot-check blocking status, and repeat the process for new Mailchimp suppressions before each send while both services are in use.

Risk: Mailchimp account credentials could be exposed if requested or shared in chat.

Mitigation: Have the user connect Mailchimp through Nitrosend's OAuth flow and do not request credentials in chat.

## Reference(s):

- [Nitrosend Mailchimp integration guide](https://docs.nitrosend.com/integrations/mailchimp)
- [Nitrosend migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)
- [ClawHub skill page](https://clawhub.ai/nitrosend/skills/nitrosend-mailchimp-migration)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown migration steps with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent-preserving import checks and pre-send guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
