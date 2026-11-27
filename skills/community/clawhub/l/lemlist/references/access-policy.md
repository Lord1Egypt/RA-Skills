# Lemlist access policy

An access policy limits which endpoints Lemlist connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/lemlist#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Lemlist: its 98 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create lemlist --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/activities"},
    {"method": "GET", "path": "api/call-statuses"},
    {"method": "GET", "path": "api/calls/{id}"},
    {"method": "GET", "path": "api/campaigns"},
    {"method": "GET", "path": "api/campaigns/reports"},
    {"method": "GET", "path": "api/campaigns/{id}"},
    {"method": "GET", "path": "api/campaigns/{id}/dynamic-sender-exclusions"},
    {"method": "GET", "path": "api/campaigns/{id}/export/leads"},
    {"method": "GET", "path": "api/campaigns/{id}/export/{id}/status"},
    {"method": "GET", "path": "api/campaigns/{id}/leads"},
    {"method": "GET", "path": "api/campaigns/{id}/schedules"},
    {"method": "GET", "path": "api/campaigns/{id}/senders"},
    {"method": "GET", "path": "api/campaigns/{id}/sequences"},
    {"method": "GET", "path": "api/campaigns/{id}/settings"},
    {"method": "GET", "path": "api/campaigns/{id}/statutes"},
    {"method": "POST", "path": "api/v2/campaigns/stats/batch"},
    {"method": "GET", "path": "api/v2/campaigns/{id}/export/leads"},
    {"method": "GET", "path": "api/v2/campaigns/{id}/stats"},
    {"method": "GET", "path": "api/companies"},
    {"method": "GET", "path": "api/companies/lists"},
    {"method": "GET", "path": "api/companies/{id}"},
    {"method": "GET", "path": "api/companies/{id}/notes"},
    {"method": "GET", "path": "api/contact-sourcing"},
    {"method": "GET", "path": "api/contacts"},
    {"method": "GET", "path": "api/contacts/export"},
    {"method": "GET", "path": "api/contacts/lists"},
    {"method": "GET", "path": "api/contacts/{id}"},
    {"method": "GET", "path": "api/contacts/{id}/notes"},
    {"method": "GET", "path": "api/crm/filters"},
    {"method": "GET", "path": "api/v2/crm/logs"},
    {"method": "POST", "path": "api/database/companies"},
    {"method": "GET", "path": "api/database/filters"},
    {"method": "POST", "path": "api/database/people"},
    {"method": "GET", "path": "api/database/personas"},
    {"method": "GET", "path": "api/database/saved-searches"},
    {"method": "GET", "path": "api/database/saved-searches/{id}"},
    {"method": "GET", "path": "api/deliverability/alerts"},
    {"method": "GET", "path": "api/deliverability/alerts/{id}"},
    {"method": "GET", "path": "api/deliverability/incidents"},
    {"method": "GET", "path": "api/domains-core/mailboxes"},
    {"method": "POST", "path": "api/domains-core/search"},
    {"method": "GET", "path": "api/domains-core/team-domains"},
    {"method": "GET", "path": "api/enrich/{id}"},
    {"method": "GET", "path": "api/v2/enrichments/providers"},
    {"method": "GET", "path": "api/v2/enrichments/waterfalls"},
    {"method": "GET", "path": "api/v2/enrichments/waterfalls/{id}"},
    {"method": "GET", "path": "api/fields"},
    {"method": "GET", "path": "api/hooks"},
    {"method": "GET", "path": "api/inbox"},
    {"method": "GET", "path": "api/inbox/labels"},
    {"method": "GET", "path": "api/inbox/labels/{id}"},
    {"method": "GET", "path": "api/inbox/{id}"},
    {"method": "GET", "path": "api/inbox/{id}/drafts"},
    {"method": "GET", "path": "api/inbox/{id}/drafts/{id}"},
    {"method": "GET", "path": "api/leads"},
    {"method": "GET", "path": "api/leads/{id}"},
    {"method": "GET", "path": "api/message-templates"},
    {"method": "GET", "path": "api/message-templates/tags"},
    {"method": "GET", "path": "api/message-templates/{id}"},
    {"method": "GET", "path": "api/schedules"},
    {"method": "GET", "path": "api/schedules/{id}"},
    {"method": "GET", "path": "api/self-recovery/config"},
    {"method": "GET", "path": "api/self-recovery/history"},
    {"method": "GET", "path": "api/sender-picture/mailboxes"},
    {"method": "GET", "path": "api/senders"},
    {"method": "GET", "path": "api/sequences/{id}/steps/{id}/ab-test"},
    {"method": "GET", "path": "api/sequences/{id}/steps/{id}/branches"},
    {"method": "GET", "path": "api/sequences/{id}/steps/{id}/sender"},
    {"method": "GET", "path": "api/snippets"},
    {"method": "GET", "path": "api/snippets/{id}"},
    {"method": "GET", "path": "api/tasks"},
    {"method": "GET", "path": "api/v2/tasks"},
    {"method": "GET", "path": "api/v2/tasks/filters"},
    {"method": "GET", "path": "api/team"},
    {"method": "GET", "path": "api/team/credits"},
    {"method": "GET", "path": "api/team/crmUsers"},
    {"method": "GET", "path": "api/team/dynamic-sender-exclusions"},
    {"method": "GET", "path": "api/team/senders"},
    {"method": "GET", "path": "api/v2/unsubscribes/contacts/{id}"},
    {"method": "GET", "path": "api/v2/unsubscribes/exports/contacts"},
    {"method": "GET", "path": "api/v2/unsubscribes/exports/variables"},
    {"method": "GET", "path": "api/v2/unsubscribes/variables"},
    {"method": "GET", "path": "api/v2/unsubscribes/variables/{id}"},
    {"method": "GET", "path": "api/user/channels"},
    {"method": "GET", "path": "api/user/sending-settings"},
    {"method": "GET", "path": "api/users/{id}"},
    {"method": "GET", "path": "api/users/{id}/signature"},
    {"method": "GET", "path": "api/views"},
    {"method": "GET", "path": "api/views/fields"},
    {"method": "GET", "path": "api/warmup/errors"},
    {"method": "GET", "path": "api/warmup/{id}/settings"},
    {"method": "GET", "path": "api/watchlist"},
    {"method": "GET", "path": "api/watchlist/filter-values"},
    {"method": "GET", "path": "api/watchlist/filters"},
    {"method": "GET", "path": "api/watchlist/history"},
    {"method": "GET", "path": "api/watchlist/library"},
    {"method": "GET", "path": "api/watchlist/linkedin-profile-views/members"},
    {"method": "GET", "path": "api/watchlist/signals"}
  ],
  "deny": []
}
```

## Endpoints

The Lemlist endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/activities | read | activities | Retrieves the history of all campaign activities and steps performed (optionally filtered by activity type and campaign). |
| DELETE | api/activities/{id}/recording-transcript | write | activities | Deletes the call recording and transcript associated with an activity. |
| GET | api/call-statuses | read | call-statuses | Lists the team's call statuses (dispositions), the keys a logged call takes as callStatus. |
| POST | api/calls | write | calls | Logs a call made outside lemlist, from an external dialer, with its status, note, recording and transcript. |
| GET | api/calls/{id} | read | calls | Reads a call of the team back, by its id or, for a call logged through the API, by the externalId you sent. |
| PATCH | api/calls/{id} | write | calls | Completes a call logged through the API with its status, note, duration, recording or transcript. |
| GET | api/campaigns | read | campaigns | Retrieves a paginated list of all campaigns in your team. |
| POST | api/campaigns | write | campaigns | Creates a new campaign with auto-generated sequence and schedule. |
| GET | api/campaigns/reports | read | campaigns | Retrieves aggregated reports and statistics for one or multiple campaigns. |
| GET | api/campaigns/{id} | read | campaigns | Retrieves detailed information about a specific campaign by ID. |
| PATCH | api/campaigns/{id} | write | campaigns | Updates the settings and configuration of an existing campaign. |
| POST | api/campaigns/{id}/abm-leads | write | campaigns | Adds People Database people to an ABM campaign. |
| POST | api/campaigns/{id}/archive | write | campaigns | Archives a campaign. |
| POST | api/campaigns/{id}/duplicate | write | campaigns | Duplicates an existing campaign with all its sequences, schedules, and templates. |
| GET | api/campaigns/{id}/dynamic-sender-exclusions | read | campaigns | Returns the senders that the leads of a campaign cannot select. |
| PUT | api/campaigns/{id}/dynamic-sender-exclusions | write | campaigns | Replaces the senders that the leads of a campaign cannot select. |
| GET | api/campaigns/{id}/export/leads | read | campaigns | Exports leads from a campaign with flexible filtering and format options. |
| GET | api/campaigns/{id}/export/start | write | campaigns | Initiates an asynchronous export of campaign statistics to a CSV file. Kept out of read: starts an export job. |
| PUT | api/campaigns/{id}/export/{id}/email/{id} | write | campaigns | Configures email notification delivery when a campaign export completes. |
| GET | api/campaigns/{id}/export/{id}/status | read | campaigns | Checks the status of an asynchronous campaign export. |
| GET | api/campaigns/{id}/leads | read | campaigns | Retrieves leads from a specific campaign, optionally filtered by state. |
| POST | api/campaigns/{id}/leads | write | campaigns | Creates a new lead and adds it to a specific campaign. |
| POST | api/campaigns/{id}/leads/import | write | campaigns | Links a campaign to a filter of your connected CRM and imports its records as leads, now and as the filter picks up new ones. |
| PATCH | api/campaigns/{id}/leads/{id} | write | campaigns | Updates an existing lead's information in a specific campaign. |
| DELETE | api/campaigns/{id}/leads/{id} | write | campaigns | Removes a lead from a campaign or unsubscribes it permanently. |
| POST | api/campaigns/{id}/leads/{id}/interested | write | campaigns | Marks a lead as interested in a specific campaign. |
| POST | api/campaigns/{id}/leads/{id}/notinterested | write | campaigns | Marks a lead as not interested in a specific campaign. |
| PUT | api/campaigns/{id}/leads/{id}/steps/{id}/personalization | write | campaigns | Personalizes the message of one campaign step for a single lead. |
| DELETE | api/campaigns/{id}/leads/{id}/steps/{id}/personalization | write | campaigns | Removes a lead's personalization of one campaign step. |
| POST | api/campaigns/{id}/leads/{id}/steps/{id}/skip | write | campaigns | Skips one step of a running campaign for a single lead. |
| POST | api/campaigns/{id}/pause | write | campaigns | Pauses a running campaign without affecting scheduled leads. |
| GET | api/campaigns/{id}/schedules | read | campaigns | Retrieves all schedules associated with a specific campaign. |
| POST | api/campaigns/{id}/schedules/{id} | write | campaigns | Associates a schedule with a campaign. |
| GET | api/campaigns/{id}/senders | read | campaigns | Returns the sender pool of a campaign, as the campaign editor shows it. |
| POST | api/campaigns/{id}/senders | write | campaigns | Adds senders, or channels of senders, to the sender pool of a campaign. |
| PUT | api/campaigns/{id}/senders | write | campaigns | Replaces the sender pool of a campaign. |
| PATCH | api/campaigns/{id}/senders/{id} | write | campaigns | Enables or disables channels of one sender, or changes the alias of a mailbox. |
| DELETE | api/campaigns/{id}/senders/{id} | write | campaigns | Removes one sender from the sender pool of a campaign. |
| GET | api/campaigns/{id}/sequences | read | campaigns | Retrieves all sequences and their steps for a specific campaign. |
| GET | api/campaigns/{id}/settings | read | campaigns | Returns all the settings of a campaign. |
| PATCH | api/campaigns/{id}/settings | write | campaigns | Changes the settings of a campaign, then returns all its settings. |
| POST | api/campaigns/{id}/start | write | campaigns | Resumes a paused campaign. |
| GET | api/campaigns/{id}/statutes | read | campaigns | Retrieves validation statutes for a campaign, including errors that block launching and warnings about daily limits, DNS issues, etc. |
| POST | api/campaigns/{id}/steps/{id}/skip | write | campaigns | Skips one step of a running campaign for every lead. |
| POST | api/campaigns/{id}/steps/{id}/skip-for-leads | write | campaigns | Skips one step of a running campaign for a list of leads. |
| POST | api/campaigns/{id}/triggers/watch-lists | write | campaigns | Links a Signal Agent to a campaign as its signal trigger. |
| DELETE | api/campaigns/{id}/triggers/watch-lists/{id} | write | campaigns | Detaches a Signal Agent from a campaign's signal triggers. |
| POST | api/campaigns/{id}/unarchive | write | campaigns | Restores an archived campaign. |
| POST | api/v2/campaigns/stats/batch | read | campaigns | Retrieves performance statistics for multiple campaigns in a single request. |
| GET | api/v2/campaigns/{id}/export/leads | read | campaigns | Exports leads from a campaign with flexible filtering and format options. |
| GET | api/v2/campaigns/{id}/stats | read | campaigns | Retrieves performance statistics for a specific campaign. |
| GET | api/companies | read | companies | Retrieves companies from your CRM. |
| POST | api/companies | write | companies | Creates a new company or updates an existing one based on domain or LinkedIn URL. |
| POST | api/companies/crm/create | write | companies | Pushes companies to your connected CRM, linking each one to the CRM record found and creating it there when none matches. |
| POST | api/companies/crm/search-and-connect | write | companies | Searches your connected CRM for companies and links each one to the CRM record found, without creating any CRM record. |
| GET | api/companies/lists | read | companies | Retrieves all company lists for the team, with optional name filtering. |
| POST | api/companies/lists | write | companies | Creates a new static company list. |
| POST | api/companies/lists/{id}/entities | write | companies | Add companies to a static company list, or remove them with ?action=remove. |
| POST | api/companies/merge | write | companies | Merges up to 10 lemlist companies into one survivor, moving everything attached to the deleted companies onto it. |
| GET | api/companies/{id} | read | companies | Retrieves one company by its lemlist id (`cpn_xxx`), as a bare object. |
| DELETE | api/companies/{id} | write | companies | Deletes a lemlist company. |
| POST | api/companies/{id}/engage | write | companies | Opens the account-based (ABM) campaign of a company. |
| GET | api/companies/{id}/notes | read | companies | Retrieves all notes associated with a specific company. |
| POST | api/companies/{id}/notes | write | companies | Creates a new note attached to a specific company. |
| GET | api/contact-sourcing | read | contact-sourcing | Reads a contact-sourcing run by ID, or the latest run of an account. |
| POST | api/contact-sourcing | write | contact-sourcing | Starts an AI contact-sourcing run for one or more accounts. |
| POST | api/contact-sourcing/contacts | write | contact-sourcing | Turns one contact-sourcing recommendation into a lemlist contact. |
| GET | api/contacts | read | contacts | Retrieves contacts from your CRM. |
| POST | api/contacts | write | contacts | Creates a new contact or updates an existing one based on email or LinkedIn URL. |
| POST | api/contacts/crm/create | write | contacts | Pushes contacts to your connected CRM, linking each one to the CRM record found and creating it there when none matches. |
| POST | api/contacts/crm/search-and-connect | write | contacts | Searches your connected CRM for contacts and links each one to the CRM record found, without creating any CRM record. |
| GET | api/contacts/export | read | contacts | Exports contacts or companies from a CRM list as a CSV file. |
| GET | api/contacts/lists | read | contacts | Retrieves all contact lists for the team, with optional name filtering. |
| POST | api/contacts/lists | write | contacts | Creates a new static contact list. |
| POST | api/contacts/lists/{id}/entities | write | contacts | Add contacts to a static contact list, or remove them with ?action=remove. |
| POST | api/contacts/merge | write | contacts | Merges up to 10 lemlist contacts into one survivor, moving everything attached to the deleted contacts onto it. |
| GET | api/contacts/{id} | read | contacts | Retrieves a specific contact by their ID or email address. |
| DELETE | api/contacts/{id} | write | contacts | Deletes a lemlist contact by id or email. |
| GET | api/contacts/{id}/notes | read | contacts | Retrieves the notes attached to a specific contact, resolved by its ID or email address. |
| POST | api/contacts/{id}/notes | write | contacts | Writes a note on a specific contact, as a note written in the lemlist app, pushed to your connected CRM. |
| GET | api/crm/filters | read | crm | Retrieves the filters of your team's connected CRM that leads can be imported from. |
| GET | api/v2/crm/logs | read | crm | Retrieves the CRM sync history of your team, a contact or a company. |
| POST | api/database/companies | read | database | Searches the companies database using filters, keywords, and pagination. |
| GET | api/database/companies/export | write | database | Exports the companies matching a search as a CSV file. Kept out of read: starts a companies export that can consume credits. |
| GET | api/database/filters | read | database | Retrieves available filters for searching the people and companies database. |
| POST | api/database/people | read | database | Searches the people database using filters, keywords, and pagination. |
| GET | api/database/people/export | write | database | Exports the People Database leads matching a search as a CSV file. Kept out of read: starts a People Database export that can consume credits. |
| POST | api/database/people/linkedin-post-engagement | write | database | Finds the people who commented on or reacted to a LinkedIn post and returns them as People Database rows. |
| GET | api/database/personas | read | database | Retrieves the People Database personas saved by your team. |
| POST | api/database/personas | write | database | Creates a People Database persona for your team. |
| DELETE | api/database/personas/{id} | write | database | Deletes a People Database persona. |
| GET | api/database/saved-searches | read | database | Retrieves the People Database saved searches of your team. |
| POST | api/database/saved-searches | write | database | Creates a People Database saved search for your team. |
| GET | api/database/saved-searches/{id} | read | database | Retrieves one People Database saved search of your team. |
| PATCH | api/database/saved-searches/{id} | write | database | Renames a People Database saved search and/or replaces its filters. |
| DELETE | api/database/saved-searches/{id} | write | database | Deletes a People Database saved search. |
| GET | api/deliverability/alerts | read | deliverability | Lists all deliverability alert configurations for your team. |
| POST | api/deliverability/alerts | write | deliverability | Creates a new deliverability alert that monitors a warm-up or outreach metric and notifies you through the configured channels when the threshold is breached. |
| GET | api/deliverability/alerts/{id} | read | deliverability | Retrieves a single deliverability alert configuration by its ID. |
| PATCH | api/deliverability/alerts/{id} | write | deliverability | Updates a deliverability alert's threshold, evaluation window, notification channels, scope filter, or enabled state. |
| DELETE | api/deliverability/alerts/{id} | write | deliverability | Permanently deletes a deliverability alert configuration. |
| GET | api/deliverability/incidents | read | deliverability | Lists your team's deliverability incidents, newest first, active and resolved. |
| GET | api/domains-core/mailboxes | read | domains-core | Lists the mailboxes bought on the team's lemlist domains. |
| PATCH | api/domains-core/mailboxes/{id} | write | domains-core | Assigns a mailbox bought through lemlist to another team member. |
| POST | api/domains-core/purchase | write | domains-core | Orders a domain, or a transfer of a domain you own elsewhere, and bills the team. |
| POST | api/domains-core/search | read | domains-core | Checks whether a domain can be bought through lemlist, with its price and the providers that can register it. |
| GET | api/domains-core/team-domains | read | domains-core | Lists the team's domains bought or being transferred through lemlist. |
| POST | api/domains-core/{id}/mailboxes | write | domains-core | Orders mailboxes on one of the team's domains and bills the team. |
| POST | api/enrich | write | enrich | Enriches data by finding emails, phone numbers, or LinkedIn information from various inputs. |
| GET | api/enrich/{id} | read | enrich | Retrieves the state and results of an enrichment. |
| POST | api/v2/enrichments/bulk | write | enrichments | Performs batch enrichment for up to 500 entities to find emails, phone numbers, or LinkedIn data. |
| GET | api/v2/enrichments/providers | read | enrichments | Lists the enrichment providers your team can place in a waterfall, for one enrichment type. |
| PUT | api/v2/enrichments/providers/{id}/connection | write | enrichments | Saves your own API key for an external enrichment provider, connecting it for your waterfalls. |
| DELETE | api/v2/enrichments/providers/{id}/connection | write | enrichments | Removes the API key of an external enrichment provider; lemlist stops calling it on your account. |
| GET | api/v2/enrichments/waterfalls | read | enrichments | Lists your team's enrichment waterfalls — the default waterfall of each type, plus every custom waterfall. |
| GET | api/v2/enrichments/waterfalls/{id} | read | enrichments | Returns one enrichment waterfall of your team, default or custom. |
| PATCH | api/v2/enrichments/waterfalls/{id} | write | enrichments | Updates the name or provider order of an enrichment waterfall. |
| PUT | api/v2/enrichments/waterfalls/{id}/reset | write | enrichments | Hands a default enrichment waterfall back to lemlist, restoring its random provider order. |
| GET | api/fields | read | fields | Lists all available fields for contacts and companies. |
| POST | api/fields | write | fields | Creates a custom field on contacts or companies, or updates the one of that name, under the rules of the lemlist app. |
| DELETE | api/fields/{id}/{id} | write | fields | Deletes a custom field on contacts or companies, as the app does, with the same permission and the same campaign guard. |
| GET | api/hooks | read | hooks | Retrieves all webhooks configured for your team. |
| POST | api/hooks | write | hooks | Creates a webhook that receives real-time POST callbacks for selected events. |
| DELETE | api/hooks/{id} | write | hooks | Deletes a specific webhook. |
| GET | api/inbox | read | inbox | Retrieves all inbox conversations for your team. |
| POST | api/inbox/conversations/labels/{id} | write | inbox | Attaches one or more labels to one or more conversations. |
| DELETE | api/inbox/conversations/labels/{id} | write | inbox | Removes one or more labels from one conversation. |
| POST | api/inbox/email | write | inbox | Sends an email to a contact through the lemlist inbox. |
| GET | api/inbox/labels | read | inbox | List all labels available to your team. |
| POST | api/inbox/labels | write | inbox | Creates a new label available to the team. |
| GET | api/inbox/labels/{id} | read | inbox | Get info of a specific label. |
| POST | api/inbox/linkedin | write | inbox | Sends a LinkedIn message to a contact through the lemlist inbox. |
| POST | api/inbox/sms | write | inbox | Sends an SMS message to a contact through the lemlist inbox. |
| POST | api/inbox/whatsapp | write | inbox | Sends a WhatsApp message to a contact through the lemlist inbox. |
| GET | api/inbox/{id} | read | inbox | Retrieves all messages exchanged with a specific contact. |
| GET | api/inbox/{id}/drafts | read | inbox | Lists all non-deleted drafts for a specific contact. |
| POST | api/inbox/{id}/drafts | write | inbox | Creates a new draft for a specific contact. |
| GET | api/inbox/{id}/drafts/{id} | read | inbox | Retrieves a single draft with its full content, including attachments. |
| PATCH | api/inbox/{id}/drafts/{id} | write | inbox | Partially updates an existing draft. |
| DELETE | api/inbox/{id}/drafts/{id} | write | inbox | Soft-deletes a draft by setting its deletedAt timestamp. |
| GET | api/leads | read | leads | Retrieves a lead using their email address or lead ID. |
| POST | api/leads/audio | write | leads | Uploads an audio file for voice message steps in campaign sequences. |
| POST | api/leads/interested/{id} | write | leads | Marks a lead as interested across all campaigns. |
| POST | api/leads/notinterested/{id} | write | leads | Marks a lead as not interested across all campaigns. |
| POST | api/leads/pause/{id} | write | leads | Pauses a lead's activity in all campaigns or a specific campaign. |
| POST | api/leads/review/{id} | write | leads | Manually launches (reviews) a single lead in its campaign. |
| POST | api/leads/start/{id} | write | leads | Resumes a paused lead in all campaigns or a specific campaign. |
| GET | api/leads/{id} | read | leads | Retrieves a specific lead by their email address. |
| POST | api/leads/{id}/enrich | write | leads | Enriches an existing lead in lemlist with additional data. |
| POST | api/leads/{id}/variables | write | leads | Adds new custom variables to a lead. |
| PATCH | api/leads/{id}/variables | write | leads | Updates the values of custom variables on a lead. |
| DELETE | api/leads/{id}/variables | write | leads | Erases the values of custom variables on a lead. |
| GET | api/message-templates | read | message-templates | Lists the team's library message templates, newest first. |
| GET | api/message-templates/tags | read | message-templates | Lists the distinct tags of the team's library message templates, alphabetically. |
| GET | api/message-templates/{id} | read | message-templates | Returns one library message template with its body. |
| GET | api/schedules | read | schedules | Retrieves all schedules for your team. |
| POST | api/schedules | write | schedules | Creates a new schedule with customizable timing and timezone settings. |
| GET | api/schedules/{id} | read | schedules | Retrieves details of a specific schedule. |
| PATCH | api/schedules/{id} | write | schedules | Updates an existing schedule's parameters. |
| DELETE | api/schedules/{id} | write | schedules | Deletes a specific schedule. |
| GET | api/self-recovery/config | read | self-recovery | Retrieves your team's self-recovery configuration — whether it is enabled, which signals are monitored, which actions are authorized, and how often the recovery digest is sent. |
| PATCH | api/self-recovery/config | write | self-recovery | Updates your team's self-recovery configuration. |
| GET | api/self-recovery/history | read | self-recovery | Lists your team's self-recovery incident history, most recent first. |
| GET | api/sender-picture/mailboxes | read | sender-picture | Lists the mailboxes a user bought through lemlist in your team, with whether their lemlist profile picture has been pushed to each one. |
| POST | api/sender-picture/sync | write | sender-picture | Queues a push of a user's lemlist profile picture onto the mailboxes they bought through lemlist. |
| GET | api/senders | read | senders | Lists the team members who can send, with their channels and the health of each channel. |
| POST | api/sequences/{id}/steps | write | sequences | Creates a step or condition within a campaign sequence. |
| PATCH | api/sequences/{id}/steps/{id} | write | sequences | Updates an existing step within a sequence. |
| DELETE | api/sequences/{id}/steps/{id} | write | sequences | Deletes a specific step from a sequence. |
| GET | api/sequences/{id}/steps/{id}/ab-test | read | sequences | Returns variant B (subject, content, config) of the A/B test on a step. |
| POST | api/sequences/{id}/steps/{id}/ab-test | write | sequences | Creates variant B of an A/B test on a step, prefilled from variant A. |
| PATCH | api/sequences/{id}/steps/{id}/ab-test | write | sequences | Edits variant B content and config of the A/B test on a step. |
| DELETE | api/sequences/{id}/steps/{id}/ab-test | write | sequences | Deletes a variant of the A/B test and ends the test. |
| POST | api/sequences/{id}/steps/{id}/ab-test/winner | write | sequences | Selects the winning A/B test variant, applied to all remaining leads. |
| GET | api/sequences/{id}/steps/{id}/branches | read | sequences | Lists the branches of a condition step, in execution order. |
| POST | api/sequences/{id}/steps/{id}/branches | write | sequences | Adds a branch to a condition step and returns it. |
| PATCH | api/sequences/{id}/steps/{id}/branches | write | sequences | Rewrites the execution priority of a condition step's branches. |
| PATCH | api/sequences/{id}/steps/{id}/branches/{id} | write | sequences | Renames a branch and/or changes what it tests. |
| DELETE | api/sequences/{id}/steps/{id}/branches/{id} | write | sequences | Removes a branch and the sub-tree behind it. |
| GET | api/sequences/{id}/steps/{id}/sender | read | sequences | Returns the forced sender of a step. |
| PUT | api/sequences/{id}/steps/{id}/sender | write | sequences | Forces a team member, and one of their accounts, as the sender of a step. |
| DELETE | api/sequences/{id}/steps/{id}/sender | write | sequences | Removes the forced sender of a step. |
| GET | api/snippets | read | snippets | Lists the team's snippets by name. |
| GET | api/snippets/{id} | read | snippets | Returns one snippet with its content. |
| GET | api/tasks | read | tasks | Retrieves all pending tasks assigned to your team members. |
| POST | api/tasks | write | tasks | Create a manual task (opportunity) associated with a contact/company or lead. |
| PATCH | api/tasks | write | tasks | Modifies aspects of an existing task including assignment, scheduling, and status. |
| POST | api/tasks/ignore | write | tasks | Marks one or more tasks as ignored. |
| GET | api/v2/tasks | read | tasks | Searches your team's tasks with the filters of the Tasks page, and returns every status. |
| GET | api/v2/tasks/filters | read | tasks | Lists every field you can use in the advancedFilters tree of Search Tasks. |
| GET | api/team | read | team | Retrieves information about your team. |
| GET | api/team/credits | read | team | Retrieves the remaining credits balance for your team's account. |
| GET | api/team/crmUsers | read | team | Retrieves the team members whose CRM account is connected to lemlist. |
| GET | api/team/dynamic-sender-exclusions | read | team | Returns the senders that the dynamic sender strategies of the team cannot select. |
| PUT | api/team/dynamic-sender-exclusions | write | team | Replaces the senders that the dynamic sender strategies of the team cannot select. |
| GET | api/team/senders | read | team | Retrieves a list of all team members and their associated campaigns. |
| GET | api/v2/unsubscribes/contacts/{id} | read | unsubscribes | Checks whether a contact is unsubscribed (do-not-contact). |
| POST | api/v2/unsubscribes/contacts/{id} | write | unsubscribes | Marks a contact as unsubscribed (do-not-contact). |
| DELETE | api/v2/unsubscribes/contacts/{id} | write | unsubscribes | Re-subscribes a contact, removing the do-not-contact flag. |
| GET | api/v2/unsubscribes/exports/contacts | read | unsubscribes | Exports all contacts with their subscription status as CSV (default) or JSON. |
| GET | api/v2/unsubscribes/exports/variables | read | unsubscribes | Exports all unsubscribed variables as CSV (default) or JSON. |
| GET | api/v2/unsubscribes/variables | read | unsubscribes | Retrieves a paginated list of all unsubscribed variables (emails, domains, LinkedIn URLs, phone numbers). |
| POST | api/v2/unsubscribes/variables | write | unsubscribes | Unsubscribes up to 10,000 variables in a single request. |
| GET | api/v2/unsubscribes/variables/{id} | read | unsubscribes | Retrieves a specific unsubscribed variable by its value. |
| POST | api/v2/unsubscribes/variables/{id} | write | unsubscribes | Unsubscribes a single variable. |
| DELETE | api/v2/unsubscribes/variables/{id} | write | unsubscribes | Re-subscribes a variable, removing it from the unsubscribe list. |
| GET | api/user/channels | read | user | Retrieves the connected channels (email, LinkedIn, WhatsApp) and their availability for the authenticated user. |
| POST | api/user/email-accounts | write | user | Connects a new SMTP/IMAP email account to your team. |
| DELETE | api/user/email-accounts/{id} | write | user | Disconnects an email account from your team. |
| POST | api/user/email-accounts/{id}/test | write | user | Tests the SMTP and IMAP connection of an email account. |
| GET | api/user/sending-settings | read | user | Retrieves the daily email limit of your email accounts, or of every team member's with `scope=team`. |
| PATCH | api/user/sending-settings | write | user | Sets the daily email limit of up to 100 team email accounts in one call. |
| GET | api/users/{id} | read | users | Retrieves all information for a specific user by their ID. |
| PATCH | api/users/{id}/linkedin-limits | write | users | Updates the daily LinkedIn limits (invitations, messages, profile visits, InMails, endorsements and more) and the invite ramp-up of a team member. |
| GET | api/users/{id}/signature | read | users | Retrieves the HTML and plain-text email signatures of a team member. |
| PATCH | api/users/{id}/signature | write | users | Updates the HTML and plain-text email signatures of a team member. |
| GET | api/views | read | views | Lists the views of the Contacts, Companies or Tasks list, as the API key's user sees them. |
| POST | api/views | write | views | Creates a view on the Contacts, Companies or Tasks list and pins it on the API key user's tabs. |
| GET | api/views/fields | read | views | Lists the fields a view of that list can filter on, with their operators and accepted values. |
| PUT | api/views/tabs | write | views | Sets which views show as the API key user's tabs on a list, and in which order. |
| PATCH | api/views/{id} | write | views | Renames a view, changes its icon or visibility, or replaces its filters. |
| DELETE | api/views/{id} | write | views | Deletes a view for everyone who sees it. |
| POST | api/views/{id}/duplicate | write | views | Copies a view, default views included, into a private view pinned on the API key user's tabs. |
| GET | api/warmup/errors | read | warmup | Lists the mailboxes kept out of warmup, with the cause and the fix for each one. |
| POST | api/warmup/{id}/pause | write | warmup | Pauses warmup for a specific user mailbox. |
| GET | api/warmup/{id}/settings | read | warmup | Retrieves the warmup settings for a specific user mailbox. |
| PATCH | api/warmup/{id}/settings | write | warmup | Updates the warmup settings for a specific user mailbox. |
| POST | api/warmup/{id}/start | write | warmup | Starts warmup for a specific user mailbox. |
| GET | api/watchlist | read | watchlist | Retrieves your Signal Agents (watch lists) with pagination and optional filtering by signal type and status. |
| POST | api/watchlist | write | watchlist | Creates a new Signal Agent (watch list). |
| PATCH | api/watchlist | write | watchlist | Updates an existing Signal Agent (watch list). |
| DELETE | api/watchlist | write | watchlist | Deletes a Signal Agent (watch list). |
| POST | api/watchlist/crm-lists | write | watchlist | Monitors the companies or contacts of one or several CRM lists with a Signal Agent. |
| GET | api/watchlist/filter-values | read | watchlist | Autocompletes allowed values for a Signal Agent filter (job titles, industries, locations, company sizes, and more). |
| GET | api/watchlist/filters | read | watchlist | Lists, per signal type, the filters you can set on a Signal Agent. |
| GET | api/watchlist/history | read | watchlist | Retrieves the configuration history of a Signal Agent — each past config version with its active period and stats. |
| GET | api/watchlist/library | read | watchlist | Lists the signal types available to your team, each with a title and description. |
| GET | api/watchlist/linkedin-profile-views/members | read | watchlist | Lists the team members whose LinkedIn profile views a Signal Agent can track, the ids the linkedinProfileViewsUserIds filter accepts. |
| GET | api/watchlist/signals | read | watchlist | Retrieves paginated signals detected by your Signal Agents with filtering and sorting capabilities. |
| PUT | api/watchlist/signals | write | watchlist | Marks one or several signals as handled or ignored. |
| POST | api/watchlist/{id}/external-signals | write | watchlist | Pushes a contact- or company-level external signal into a Signal Agent. |
