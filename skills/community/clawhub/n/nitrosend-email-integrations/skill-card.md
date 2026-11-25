## Description:

Connect tools that trigger emails and update contacts: Shopify, HubSpot, Attio, Mailchimp, and ActiveCampaign connect natively in the Nitrosend app, while other apps and backends can send contacts and events through the REST API or Events API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to connect email triggers and contact updates across Nitrosend's native integrations or other apps using its REST API and Events API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contacts synced from HubSpot or Attio may arrive subscribed unless the CRM marks them opted out, which can lead to sending email without consent.

Mitigation: Bring opt-outs across before connecting a source and confirm consent before sending to a synced audience.

Risk: Recording an event can start live flows.

Mitigation: Use a test contact and record a test event only after the user confirms.

## Reference(s):

- [Nitrosend Shopify integration guide](https://docs.nitrosend.com/integrations/shopify)
- [Nitrosend Events API guide](https://docs.nitrosend.com/integrations/events-api)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include integration setup guidance, event payload guidance, and test-event steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
