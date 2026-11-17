# Where submissions land

## The shared GTM models

Every submission from a work email upserts two rows:

- **`gtm_accounts`**, matched on `website` (the email domain): `name`, `number_of_employees`,
  `billing_country`, `linkedin_url` and `description` from LinkedIn's company data.
- **`gtm_contacts`**, matched on `email`: `first_name`, `last_name`, `name`, `account_id` (the
  `id` of the account row above), `lead_source` `website`, and the columns this skill adds:

| Added column        | What it holds                                              |
| ------------------- | ---------------------------------------------------------- |
| `inbound_status`    | `qualified`, `not_qualified` or `unknown_company`          |
| `inbound_message`   | what they wrote                                            |
| `inbound_page_url`  | the page they submitted from                               |
| `utm_source`        | the visit's `utm_source`                                   |
| `utm_campaign`      | the visit's `utm_campaign`                                 |
| `marketing_consent` | whether they ticked the box to receive product news        |

These are the shared models every pipeline declares under the same slug
(`scripts/native-models.json`). Cargo generates each record's `id`; `account_id` is read back from
the account upsert, never invented. A second submission from the same person updates their row
instead of adding one.

## Query it

```sql
SELECT c.name, c.email, a.name AS company, a.number_of_employees,
       c.custom__inbound_status, c.custom__inbound_page_url
FROM gtm_contacts c
JOIN gtm_accounts a ON a.id = c.account_id
WHERE c.lead_source = 'website'
ORDER BY c._updated_at DESC
```

Check the dataset and column names with `cargo-ai storage column list` against the live models
before relying on this.

## The `crm-backed` variation

When contacts belong in a CRM, the two `model.upsert` calls become the CRM connector's upsert, with
the same fields under the CRM's names. For HubSpot (`upsertRecords`, `mappings` as
`{ propertyName, value }`):

| Shared model column                    | HubSpot property                                    |
| -------------------------------------- | --------------------------------------------------- |
| `gtm_accounts.website` (match)         | company `domain`                                    |
| `gtm_accounts.name`                    | company `name`                                      |
| `gtm_accounts.number_of_employees`     | company `numberofemployees`                         |
| `gtm_contacts.email` (match)           | contact `email`                                     |
| `gtm_contacts.first_name` / `last_name`| contact `firstname` / `lastname`                    |
| `gtm_contacts.lead_source`             | contact `lifecyclestage` `lead`                     |
| added columns                          | contact properties of the same names, created first |

The CRM properties must exist before the first deploy; a missing one fails the run, not the plan.
Keep the Slack post and the answer unchanged.

## Reading a count

- **Only work emails create rows.** A refused personal email writes nothing.
- **`unknown_company` is not a failure.** LinkedIn has no company for some domains; the contact is
  still written and posted, without a qualification.
- **A submission is not a meeting.** `qualified` means the company fits the rules and was shown the
  booking link; whether they booked lives in the scheduling tool.
