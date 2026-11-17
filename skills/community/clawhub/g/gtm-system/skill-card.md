## Description:

Manage go-to-market activities including contacts, opportunities, pipeline stages, reminders, and signal crawling through a command-line workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Founder-led GTM teams and agents use this skill to track contacts, opportunities, follow-ups, daily actions, and public market signals. It supports natural-language requests by mapping common GTM questions to local CLI commands and summarizing the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an embedded Exa API key.

Mitigation: Remove the embedded key, rotate any exposed credential, and require users to provide credentials explicitly through their own environment.

Risk: The security evidence reports under-disclosed production CRM access through HubSpot sync.

Mitigation: Gate HubSpot sync behind explicit configuration and user confirmation, and document the CRM data accessed before installation.

Risk: The local SQLite database can contain sensitive CRM and contact data.

Mitigation: Treat the database as sensitive, restrict filesystem access, and avoid sharing exports or digests that include private contact details.

Risk: Signal crawling can contact third-party API destinations.

Mitigation: Document enabled destinations and credentials, and let users disable crawlers they do not want to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/gtm-system)
- [Chapter GTM repository evaluated by artifact](https://github.com/chapter-gtm/chapter)
- [F5Bot](https://f5bot.com/)
- [Apollo.io](https://www.apollo.io/)
- [Exa API destination](https://api.exa.ai/search)
- [HubSpot CRM API destination](https://api.hubapi.com/crm/v3/objects/contacts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text output, Markdown digests, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local CRM/contact records, pipeline state, reminders, and crawled public signal summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
