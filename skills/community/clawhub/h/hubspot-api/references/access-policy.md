# HubSpot access policy

An access policy limits which endpoints HubSpot connections may call through Maton. HubSpot doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/hubspot#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for HubSpot: its 197 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create hubspot --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "crm/v3/objects/contacts"},
    {"method": "GET", "path": "crm/v3/objects/contacts/{id}"},
    {"method": "POST", "path": "crm/v3/objects/contacts/search"},
    {"method": "POST", "path": "crm/v3/objects/contacts/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/companies"},
    {"method": "GET", "path": "crm/v3/objects/companies/{id}"},
    {"method": "POST", "path": "crm/v3/objects/companies/search"},
    {"method": "POST", "path": "crm/v3/objects/companies/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/deals"},
    {"method": "GET", "path": "crm/v3/objects/deals/{id}"},
    {"method": "POST", "path": "crm/v3/objects/deals/search"},
    {"method": "POST", "path": "crm/v3/objects/deals/batch/read"},
    {"method": "POST", "path": "crm/v3/objects/deals/splits/batch/read"},
    {"method": "POST", "path": "crm/objects/{id}/deals/splits/batch/read"},
    {"method": "POST", "path": "deal-splits/{id}/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/tickets"},
    {"method": "GET", "path": "crm/v3/objects/tickets/{id}"},
    {"method": "POST", "path": "crm/v3/objects/tickets/search"},
    {"method": "POST", "path": "crm/v3/objects/tickets/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/leads"},
    {"method": "GET", "path": "crm/v3/objects/leads/{id}"},
    {"method": "POST", "path": "crm/v3/objects/leads/search"},
    {"method": "POST", "path": "crm/v3/objects/leads/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/notes"},
    {"method": "GET", "path": "crm/v3/objects/notes/{id}"},
    {"method": "POST", "path": "crm/v3/objects/notes/search"},
    {"method": "POST", "path": "crm/v3/objects/notes/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/calls"},
    {"method": "GET", "path": "crm/v3/objects/calls/{id}"},
    {"method": "POST", "path": "crm/v3/objects/calls/search"},
    {"method": "POST", "path": "crm/v3/objects/calls/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/emails"},
    {"method": "GET", "path": "crm/v3/objects/emails/{id}"},
    {"method": "POST", "path": "crm/v3/objects/emails/search"},
    {"method": "POST", "path": "crm/v3/objects/emails/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/meetings"},
    {"method": "GET", "path": "crm/v3/objects/meetings/{id}"},
    {"method": "POST", "path": "crm/v3/objects/meetings/search"},
    {"method": "POST", "path": "crm/v3/objects/meetings/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/tasks"},
    {"method": "GET", "path": "crm/v3/objects/tasks/{id}"},
    {"method": "POST", "path": "crm/v3/objects/tasks/search"},
    {"method": "POST", "path": "crm/v3/objects/tasks/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/users"},
    {"method": "GET", "path": "crm/v3/objects/users/{id}"},
    {"method": "POST", "path": "crm/v3/objects/users/search"},
    {"method": "POST", "path": "crm/v3/objects/users/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/{id}"},
    {"method": "GET", "path": "crm/v3/objects/{id}/{id}"},
    {"method": "POST", "path": "crm/v3/objects/{id}/search"},
    {"method": "POST", "path": "crm/v3/objects/{id}/batch/read"},
    {"method": "GET", "path": "crm/objects/{id}/{id}"},
    {"method": "GET", "path": "crm/objects/{id}/{id}/{id}"},
    {"method": "POST", "path": "crm/objects/{id}/{id}/search"},
    {"method": "POST", "path": "crm/objects/{id}/{id}/batch/read"},
    {"method": "GET", "path": "crm/v3/objects/{id}/{id}/associations/{id}"},
    {"method": "GET", "path": "crm/objects/{id}/{id}/{id}/associations/{id}"},
    {"method": "GET", "path": "crm/v4/objects/{id}/{id}/associations/{id}"},
    {"method": "GET", "path": "crm/v3/associations/{id}/{id}/types"},
    {"method": "POST", "path": "crm/v3/associations/{id}/{id}/batch/read"},
    {"method": "POST", "path": "crm/v4/associations/{id}/{id}/batch/read"},
    {"method": "GET", "path": "crm/v4/associations/{id}/{id}/labels"},
    {"method": "POST", "path": "crm/associations/{id}/{id}/{id}/batch/read"},
    {"method": "GET", "path": "crm/associations/{id}/{id}/{id}/labels"},
    {"method": "GET", "path": "crm/associations/{id}/definitions/configurations/all"},
    {"method": "GET", "path": "crm/associations/{id}/definitions/configurations/{id}/{id}"},
    {"method": "GET", "path": "crm/v3/properties/{id}"},
    {"method": "GET", "path": "crm/v3/properties/{id}/{id}"},
    {"method": "POST", "path": "crm/v3/properties/{id}/batch/read"},
    {"method": "GET", "path": "crm/properties/{id}/{id}"},
    {"method": "GET", "path": "crm/properties/{id}/{id}/{id}"},
    {"method": "POST", "path": "crm/properties/{id}/{id}/batch/read"},
    {"method": "GET", "path": "crm/v3/properties/{id}/groups"},
    {"method": "GET", "path": "crm/v3/properties/{id}/groups/{id}"},
    {"method": "GET", "path": "crm/properties/{id}/{id}/groups"},
    {"method": "GET", "path": "crm/properties/{id}/{id}/groups/{id}"},
    {"method": "GET", "path": "crm/v3/property-validations/{id}"},
    {"method": "GET", "path": "crm/v3/property-validations/{id}/{id}"},
    {"method": "GET", "path": "crm/v3/property-validations/{id}/{id}/rule-type/{id}"},
    {"method": "GET", "path": "crm/property-validations/{id}/{id}"},
    {"method": "GET", "path": "crm/property-validations/{id}/{id}/{id}"},
    {"method": "GET", "path": "crm/property-validations/{id}/{id}/{id}/rule-type/{id}"},
    {"method": "GET", "path": "crm/v3/schemas"},
    {"method": "GET", "path": "crm/v3/schemas/{id}"},
    {"method": "GET", "path": "crm-object-schemas/{id}/schemas"},
    {"method": "GET", "path": "crm-object-schemas/{id}/schemas/{id}"},
    {"method": "POST", "path": "crm-object-schemas/{id}/schemas/batch/read"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}/{id}"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}/{id}/audit"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}/{id}/stages"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}/{id}/stages/{id}"},
    {"method": "GET", "path": "crm/v3/pipelines/{id}/{id}/stages/{id}/audit"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}/{id}"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}/{id}/audit"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}/{id}/stages"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}/{id}/stages/{id}"},
    {"method": "GET", "path": "crm/pipelines/{id}/{id}/{id}/stages/{id}/audit"},
    {"method": "GET", "path": "crm/v3/owners"},
    {"method": "GET", "path": "crm/v3/owners/{id}"},
    {"method": "GET", "path": "crm/owners/{id}"},
    {"method": "GET", "path": "crm/owners/{id}/{id}"},
    {"method": "GET", "path": "crm/v3/lists"},
    {"method": "GET", "path": "crm/v3/lists/{id}"},
    {"method": "GET", "path": "crm/v3/lists/object-type-id/{id}/name/{id}"},
    {"method": "POST", "path": "crm/v3/lists/search"},
    {"method": "GET", "path": "crm/v3/lists/idmapping"},
    {"method": "POST", "path": "crm/v3/lists/idmapping"},
    {"method": "GET", "path": "crm/v3/lists/{id}/memberships"},
    {"method": "GET", "path": "crm/v3/lists/{id}/memberships/join-order"},
    {"method": "GET", "path": "crm/v3/lists/records/{id}/{id}/memberships"},
    {"method": "POST", "path": "crm/v3/lists/records/memberships/batch/read"},
    {"method": "GET", "path": "crm/v3/lists/{id}/schedule-conversion"},
    {"method": "GET", "path": "crm/v3/lists/{id}/size-and-edits-history/between"},
    {"method": "GET", "path": "crm/v3/lists/folders"},
    {"method": "GET", "path": "crm/lists/{id}"},
    {"method": "GET", "path": "crm/lists/{id}/{id}"},
    {"method": "GET", "path": "crm/lists/{id}/object-type-id/{id}/name/{id}"},
    {"method": "POST", "path": "crm/lists/{id}/search"},
    {"method": "GET", "path": "crm/lists/{id}/idmapping"},
    {"method": "POST", "path": "crm/lists/{id}/idmapping"},
    {"method": "GET", "path": "crm/lists/{id}/{id}/memberships"},
    {"method": "GET", "path": "crm/lists/{id}/{id}/memberships/join-order"},
    {"method": "GET", "path": "crm/lists/{id}/records/{id}/{id}/memberships"},
    {"method": "POST", "path": "crm/lists/{id}/records/memberships/batch/read"},
    {"method": "GET", "path": "crm/lists/{id}/{id}/schedule-conversion"},
    {"method": "GET", "path": "crm/lists/{id}/{id}/size-and-edits-history/between"},
    {"method": "GET", "path": "crm/lists/{id}/folders"},
    {"method": "POST", "path": "crm/lists/{id}/all"},
    {"method": "GET", "path": "crm/v3/imports"},
    {"method": "GET", "path": "crm/v3/imports/{id}"},
    {"method": "GET", "path": "crm/v3/imports/{id}/errors"},
    {"method": "GET", "path": "crm/imports/{id}"},
    {"method": "GET", "path": "crm/imports/{id}/{id}"},
    {"method": "GET", "path": "crm/imports/{id}/{id}/errors"},
    {"method": "GET", "path": "crm/v3/exports/export/{id}"},
    {"method": "GET", "path": "crm/v3/exports/export/async/tasks/{id}/status"},
    {"method": "GET", "path": "crm/exports/{id}/export/{id}"},
    {"method": "GET", "path": "crm/exports/{id}/export/async/tasks/{id}/status"},
    {"method": "GET", "path": "crm/v3/limits/records"},
    {"method": "GET", "path": "crm/v3/limits/custom-object-types"},
    {"method": "GET", "path": "crm/v3/limits/custom-properties"},
    {"method": "GET", "path": "crm/v3/limits/calculated-properties"},
    {"method": "GET", "path": "crm/v3/limits/pipelines"},
    {"method": "GET", "path": "crm/v3/limits/associations/labels"},
    {"method": "GET", "path": "crm/v3/limits/associations/records/from"},
    {"method": "GET", "path": "crm/v3/limits/associations/records/{id}/to"},
    {"method": "GET", "path": "crm/v3/limits/associations/records/{id}/{id}"},
    {"method": "GET", "path": "crm/limits/{id}/records"},
    {"method": "GET", "path": "crm/limits/{id}/custom-object-types"},
    {"method": "GET", "path": "crm/limits/{id}/custom-properties"},
    {"method": "GET", "path": "crm/limits/{id}/calculated-properties"},
    {"method": "GET", "path": "crm/limits/{id}/pipelines"},
    {"method": "GET", "path": "crm/limits/{id}/associations/labels"},
    {"method": "GET", "path": "crm/limits/{id}/associations/records/from"},
    {"method": "GET", "path": "crm/limits/{id}/associations/records/{id}/to"},
    {"method": "GET", "path": "crm/limits/{id}/associations/records/{id}/{id}"},
    {"method": "GET", "path": "account-info/{id}/details"},
    {"method": "GET", "path": "account-info/{id}/api-usage/daily"},
    {"method": "GET", "path": "account-info/{id}/api-usage/daily/private-apps"},
    {"method": "GET", "path": "account-info/{id}/api-usage/daily/privately-distributed"},
    {"method": "GET", "path": "account-info/{id}/activity/audit-logs"},
    {"method": "GET", "path": "account-info/{id}/activity/login"},
    {"method": "GET", "path": "account-info/{id}/activity/security"},
    {"method": "GET", "path": "business-units/v3/business-units/user/{id}"},
    {"method": "GET", "path": "business-units/public/{id}/business-units/user/{id}"},
    {"method": "GET", "path": "tax-rates/{id}/tax-rates"},
    {"method": "GET", "path": "tax-rates/{id}/tax-rates/{id}"},
    {"method": "GET", "path": "settings/v3/users"},
    {"method": "GET", "path": "settings/v3/users/{id}"},
    {"method": "GET", "path": "settings/v3/users/roles"},
    {"method": "GET", "path": "settings/v3/users/teams"},
    {"method": "GET", "path": "settings/users/{id}"},
    {"method": "GET", "path": "settings/users/{id}/{id}"},
    {"method": "GET", "path": "settings/users/{id}/roles"},
    {"method": "GET", "path": "settings/users/{id}/teams"},
    {"method": "GET", "path": "settings/users/{id}/seats"},
    {"method": "GET", "path": "settings/teams/{id}"},
    {"method": "GET", "path": "settings/teams/{id}/{id}"},
    {"method": "GET", "path": "settings/teams/{id}/{id}/members"},
    {"method": "GET", "path": "settings/v3/currencies/codes"},
    {"method": "GET", "path": "settings/v3/currencies/company-currency"},
    {"method": "GET", "path": "settings/v3/currencies/exchange-rates"},
    {"method": "GET", "path": "settings/v3/currencies/exchange-rates/current"},
    {"method": "GET", "path": "settings/v3/currencies/exchange-rates/{id}"},
    {"method": "POST", "path": "settings/v3/currencies/exchange-rates/batch/read"},
    {"method": "GET", "path": "settings/v3/currencies/central-fx-rates/information"},
    {"method": "GET", "path": "settings/v3/currencies/central-fx-rates/unsupported-currencies"},
    {"method": "GET", "path": "settings/currencies/{id}/codes"},
    {"method": "GET", "path": "settings/currencies/{id}/company-currency"},
    {"method": "GET", "path": "settings/currencies/{id}/exchange-rates"},
    {"method": "GET", "path": "settings/currencies/{id}/exchange-rates/current"},
    {"method": "GET", "path": "settings/currencies/{id}/exchange-rates/{id}"},
    {"method": "POST", "path": "settings/currencies/{id}/exchange-rates/batch/read"},
    {"method": "GET", "path": "settings/currencies/{id}/central-fx-rates/information"},
    {"method": "GET", "path": "settings/currencies/{id}/central-fx-rates/unsupported-currencies"}
  ],
  "deny": []
}
```

## Endpoints

The HubSpot endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | crm/v3/objects/contacts | read | contacts | List contacts. |
| GET | crm/v3/objects/contacts/{id} | read | contacts | Get a contact by ID. |
| POST | crm/v3/objects/contacts/search | read | contacts | Search contacts with filters; POST only carries the query. |
| POST | crm/v3/objects/contacts/batch/read | read | contacts | Read a batch of contacts by ID; POST only carries the ID list. |
| POST | crm/v3/objects/contacts | write | contacts | Create a contact. |
| PATCH | crm/v3/objects/contacts/{id} | write | contacts | Update a contact. |
| DELETE | crm/v3/objects/contacts/{id} | write | contacts | Archive a contact. |
| POST | crm/v3/objects/contacts/batch/create | write | contacts | Create a batch of contacts. |
| POST | crm/v3/objects/contacts/batch/update | write | contacts | Update a batch of contacts. |
| POST | crm/v3/objects/contacts/batch/upsert | write | contacts | Create or update a batch of contacts by unique property. |
| POST | crm/v3/objects/contacts/batch/archive | write | contacts | Archive a batch of contacts. |
| POST | crm/v3/objects/contacts/merge | write | contacts | Merge two contacts into one. |
| POST | crm/v3/objects/contacts/gdpr-delete | write | contacts | Permanently delete a contact and its data for GDPR. |
| GET | crm/v3/objects/companies | read | companies | List companies. |
| GET | crm/v3/objects/companies/{id} | read | companies | Get a company by ID. |
| POST | crm/v3/objects/companies/search | read | companies | Search companies with filters; POST only carries the query. |
| POST | crm/v3/objects/companies/batch/read | read | companies | Read a batch of companies by ID; POST only carries the ID list. |
| POST | crm/v3/objects/companies | write | companies | Create a company. |
| PATCH | crm/v3/objects/companies/{id} | write | companies | Update a company. |
| DELETE | crm/v3/objects/companies/{id} | write | companies | Archive a company. |
| POST | crm/v3/objects/companies/batch/create | write | companies | Create a batch of companies. |
| POST | crm/v3/objects/companies/batch/update | write | companies | Update a batch of companies. |
| POST | crm/v3/objects/companies/batch/upsert | write | companies | Create or update a batch of companies by unique property. |
| POST | crm/v3/objects/companies/batch/archive | write | companies | Archive a batch of companies. |
| POST | crm/v3/objects/companies/merge | write | companies | Merge two companies into one. |
| GET | crm/v3/objects/deals | read | deals | List deals. |
| GET | crm/v3/objects/deals/{id} | read | deals | Get a deal by ID. |
| POST | crm/v3/objects/deals/search | read | deals | Search deals with filters; POST only carries the query. |
| POST | crm/v3/objects/deals/batch/read | read | deals | Read a batch of deals by ID; POST only carries the ID list. |
| POST | crm/v3/objects/deals | write | deals | Create a deal. |
| PATCH | crm/v3/objects/deals/{id} | write | deals | Update a deal. |
| DELETE | crm/v3/objects/deals/{id} | write | deals | Archive a deal. |
| POST | crm/v3/objects/deals/batch/create | write | deals | Create a batch of deals. |
| POST | crm/v3/objects/deals/batch/update | write | deals | Update a batch of deals. |
| POST | crm/v3/objects/deals/batch/upsert | write | deals | Create or update a batch of deals by unique property. |
| POST | crm/v3/objects/deals/batch/archive | write | deals | Archive a batch of deals. |
| POST | crm/v3/objects/deals/merge | write | deals | Merge two deals into one. |
| POST | crm/v3/objects/deals/splits/batch/read | read | deals | Read deal splits for a batch of deals; POST only carries the deal IDs. |
| POST | crm/v3/objects/deals/splits/batch/upsert | write | deals | Create or replace deal splits for a batch of deals. |
| POST | crm/objects/{id}/deals/splits/batch/read | read | deals | Read deal splits for a batch of deals; POST only carries the deal IDs (date-versioned path). |
| POST | crm/objects/{id}/deals/splits/batch/upsert | write | deals | Create or replace deal splits for a batch of deals (date-versioned path). |
| POST | deal-splits/{id}/batch/read | read | deals | Read deal splits for a batch of deals; POST only carries the deal IDs (date-versioned path). |
| POST | deal-splits/{id}/batch/upsert | write | deals | Create or replace deal splits for a batch of deals (date-versioned path). |
| GET | crm/v3/objects/tickets | read | tickets | List tickets. |
| GET | crm/v3/objects/tickets/{id} | read | tickets | Get a ticket by ID. |
| POST | crm/v3/objects/tickets/search | read | tickets | Search tickets with filters; POST only carries the query. |
| POST | crm/v3/objects/tickets/batch/read | read | tickets | Read a batch of tickets by ID; POST only carries the ID list. |
| POST | crm/v3/objects/tickets | write | tickets | Create a ticket. |
| PATCH | crm/v3/objects/tickets/{id} | write | tickets | Update a ticket. |
| DELETE | crm/v3/objects/tickets/{id} | write | tickets | Archive a ticket. |
| POST | crm/v3/objects/tickets/batch/create | write | tickets | Create a batch of tickets. |
| POST | crm/v3/objects/tickets/batch/update | write | tickets | Update a batch of tickets. |
| POST | crm/v3/objects/tickets/batch/upsert | write | tickets | Create or update a batch of tickets by unique property. |
| POST | crm/v3/objects/tickets/batch/archive | write | tickets | Archive a batch of tickets. |
| POST | crm/v3/objects/tickets/merge | write | tickets | Merge two tickets into one. |
| GET | crm/v3/objects/leads | read | leads | List leads. |
| GET | crm/v3/objects/leads/{id} | read | leads | Get a lead by ID. |
| POST | crm/v3/objects/leads/search | read | leads | Search leads with filters; POST only carries the query. |
| POST | crm/v3/objects/leads/batch/read | read | leads | Read a batch of leads by ID; POST only carries the ID list. |
| POST | crm/v3/objects/leads | write | leads | Create a lead. |
| PATCH | crm/v3/objects/leads/{id} | write | leads | Update a lead. |
| DELETE | crm/v3/objects/leads/{id} | write | leads | Archive a lead. |
| POST | crm/v3/objects/leads/batch/create | write | leads | Create a batch of leads. |
| POST | crm/v3/objects/leads/batch/update | write | leads | Update a batch of leads. |
| POST | crm/v3/objects/leads/batch/upsert | write | leads | Create or update a batch of leads by unique property. |
| POST | crm/v3/objects/leads/batch/archive | write | leads | Archive a batch of leads. |
| GET | crm/v3/objects/notes | read | notes | List notes. |
| GET | crm/v3/objects/notes/{id} | read | notes | Get a note by ID. |
| POST | crm/v3/objects/notes/search | read | notes | Search notes with filters; POST only carries the query. |
| POST | crm/v3/objects/notes/batch/read | read | notes | Read a batch of notes by ID; POST only carries the ID list. |
| POST | crm/v3/objects/notes | write | notes | Create a note. |
| PATCH | crm/v3/objects/notes/{id} | write | notes | Update a note. |
| DELETE | crm/v3/objects/notes/{id} | write | notes | Archive a note. |
| POST | crm/v3/objects/notes/batch/create | write | notes | Create a batch of notes. |
| POST | crm/v3/objects/notes/batch/update | write | notes | Update a batch of notes. |
| POST | crm/v3/objects/notes/batch/upsert | write | notes | Create or update a batch of notes by unique property. |
| POST | crm/v3/objects/notes/batch/archive | write | notes | Archive a batch of notes. |
| GET | crm/v3/objects/calls | read | calls | List logged calls. |
| GET | crm/v3/objects/calls/{id} | read | calls | Get a logged call by ID. |
| POST | crm/v3/objects/calls/search | read | calls | Search logged calls with filters; POST only carries the query. |
| POST | crm/v3/objects/calls/batch/read | read | calls | Read a batch of logged calls by ID; POST only carries the ID list. |
| POST | crm/v3/objects/calls | write | calls | Create a logged call. |
| PATCH | crm/v3/objects/calls/{id} | write | calls | Update a logged call. |
| DELETE | crm/v3/objects/calls/{id} | write | calls | Archive a logged call. |
| POST | crm/v3/objects/calls/batch/create | write | calls | Create a batch of logged calls. |
| POST | crm/v3/objects/calls/batch/update | write | calls | Update a batch of logged calls. |
| POST | crm/v3/objects/calls/batch/upsert | write | calls | Create or update a batch of logged calls by unique property. |
| POST | crm/v3/objects/calls/batch/archive | write | calls | Archive a batch of logged calls. |
| GET | crm/v3/objects/emails | read | emails | List logged email engagements. |
| GET | crm/v3/objects/emails/{id} | read | emails | Get a logged email engagement by ID. |
| POST | crm/v3/objects/emails/search | read | emails | Search logged email engagements with filters; POST only carries the query. |
| POST | crm/v3/objects/emails/batch/read | read | emails | Read a batch of logged email engagements by ID; POST only carries the ID list. |
| POST | crm/v3/objects/emails | write | emails | Create a logged email engagement. |
| PATCH | crm/v3/objects/emails/{id} | write | emails | Update a logged email engagement. |
| DELETE | crm/v3/objects/emails/{id} | write | emails | Archive a logged email engagement. |
| POST | crm/v3/objects/emails/batch/create | write | emails | Create a batch of logged email engagements. |
| POST | crm/v3/objects/emails/batch/update | write | emails | Update a batch of logged email engagements. |
| POST | crm/v3/objects/emails/batch/upsert | write | emails | Create or update a batch of logged email engagements by unique property. |
| POST | crm/v3/objects/emails/batch/archive | write | emails | Archive a batch of logged email engagements. |
| GET | crm/v3/objects/meetings | read | meetings | List logged meetings. |
| GET | crm/v3/objects/meetings/{id} | read | meetings | Get a logged meeting by ID. |
| POST | crm/v3/objects/meetings/search | read | meetings | Search logged meetings with filters; POST only carries the query. |
| POST | crm/v3/objects/meetings/batch/read | read | meetings | Read a batch of logged meetings by ID; POST only carries the ID list. |
| POST | crm/v3/objects/meetings | write | meetings | Create a logged meeting. |
| PATCH | crm/v3/objects/meetings/{id} | write | meetings | Update a logged meeting. |
| DELETE | crm/v3/objects/meetings/{id} | write | meetings | Archive a logged meeting. |
| POST | crm/v3/objects/meetings/batch/create | write | meetings | Create a batch of logged meetings. |
| POST | crm/v3/objects/meetings/batch/update | write | meetings | Update a batch of logged meetings. |
| POST | crm/v3/objects/meetings/batch/upsert | write | meetings | Create or update a batch of logged meetings by unique property. |
| POST | crm/v3/objects/meetings/batch/archive | write | meetings | Archive a batch of logged meetings. |
| GET | crm/v3/objects/tasks | read | tasks | List tasks. |
| GET | crm/v3/objects/tasks/{id} | read | tasks | Get a task by ID. |
| POST | crm/v3/objects/tasks/search | read | tasks | Search tasks with filters; POST only carries the query. |
| POST | crm/v3/objects/tasks/batch/read | read | tasks | Read a batch of tasks by ID; POST only carries the ID list. |
| POST | crm/v3/objects/tasks | write | tasks | Create a task. |
| PATCH | crm/v3/objects/tasks/{id} | write | tasks | Update a task. |
| DELETE | crm/v3/objects/tasks/{id} | write | tasks | Archive a task. |
| POST | crm/v3/objects/tasks/batch/create | write | tasks | Create a batch of tasks. |
| POST | crm/v3/objects/tasks/batch/update | write | tasks | Update a batch of tasks. |
| POST | crm/v3/objects/tasks/batch/upsert | write | tasks | Create or update a batch of tasks by unique property. |
| POST | crm/v3/objects/tasks/batch/archive | write | tasks | Archive a batch of tasks. |
| GET | crm/v3/objects/users | read | users | List user records. |
| GET | crm/v3/objects/users/{id} | read | users | Get a user record by ID. |
| POST | crm/v3/objects/users/search | read | users | Search user records with filters; POST only carries the query. |
| POST | crm/v3/objects/users/batch/read | read | users | Read a batch of user records by ID; POST only carries the ID list. |
| POST | crm/v3/objects/users | write | users | Create a user record. |
| PATCH | crm/v3/objects/users/{id} | write | users | Update a user record. |
| DELETE | crm/v3/objects/users/{id} | write | users | Archive a user record. |
| POST | crm/v3/objects/users/batch/create | write | users | Create a batch of user records. |
| POST | crm/v3/objects/users/batch/update | write | users | Update a batch of user records. |
| POST | crm/v3/objects/users/batch/upsert | write | users | Create or update a batch of user records by unique property. |
| POST | crm/v3/objects/users/batch/archive | write | users | Archive a batch of user records. |
| GET | crm/v3/objects/{id} | read | objects | List records of any object type. |
| GET | crm/v3/objects/{id}/{id} | read | objects | Get a record of any object type by ID. |
| POST | crm/v3/objects/{id}/search | read | objects | Search records of any object type with filters; POST only carries the query. |
| POST | crm/v3/objects/{id}/batch/read | read | objects | Read a batch of records of any object type by ID; POST only carries the ID list. |
| POST | crm/v3/objects/{id} | write | objects | Create a record of any object type. |
| PATCH | crm/v3/objects/{id}/{id} | write | objects | Update a record of any object type. |
| DELETE | crm/v3/objects/{id}/{id} | write | objects | Archive a record of any object type. |
| POST | crm/v3/objects/{id}/batch/create | write | objects | Create a batch of records of any object type. |
| POST | crm/v3/objects/{id}/batch/update | write | objects | Update a batch of records of any object type. |
| POST | crm/v3/objects/{id}/batch/upsert | write | objects | Create or update a batch of records of any object type by unique property. |
| POST | crm/v3/objects/{id}/batch/archive | write | objects | Archive a batch of records of any object type. |
| POST | crm/v3/objects/{id}/merge | write | objects | Merge two records of any object type into one. |
| POST | crm/v3/objects/{id}/gdpr-delete | write | objects | Permanently delete a record of any object type and its data for GDPR. |
| GET | crm/objects/{id}/{id} | read | objects | List records of any object type (date-versioned path). |
| GET | crm/objects/{id}/{id}/{id} | read | objects | Get a record of any object type by ID (date-versioned path). |
| POST | crm/objects/{id}/{id}/search | read | objects | Search records of any object type with filters; POST only carries the query (date-versioned path). |
| POST | crm/objects/{id}/{id}/batch/read | read | objects | Read a batch of records of any object type by ID; POST only carries the ID list (date-versioned path). |
| POST | crm/objects/{id}/{id} | write | objects | Create a record of any object type (date-versioned path). |
| PATCH | crm/objects/{id}/{id}/{id} | write | objects | Update a record of any object type (date-versioned path). |
| DELETE | crm/objects/{id}/{id}/{id} | write | objects | Archive a record of any object type (date-versioned path). |
| POST | crm/objects/{id}/{id}/batch/create | write | objects | Create a batch of records of any object type (date-versioned path). |
| POST | crm/objects/{id}/{id}/batch/update | write | objects | Update a batch of records of any object type (date-versioned path). |
| POST | crm/objects/{id}/{id}/batch/upsert | write | objects | Create or update a batch of records of any object type by unique property (date-versioned path). |
| POST | crm/objects/{id}/{id}/batch/archive | write | objects | Archive a batch of records of any object type (date-versioned path). |
| POST | crm/objects/{id}/{id}/merge | write | objects | Merge two records of any object type into one (date-versioned path). |
| POST | crm/objects/{id}/{id}/gdpr-delete | write | objects | Permanently delete a record of any object type and its data for GDPR (date-versioned path). |
| GET | crm/v3/objects/{id}/{id}/associations/{id} | read | associations | List records of one type associated with a record (v3). |
| PUT | crm/v3/objects/{id}/{id}/associations/{id}/{id}/{id} | write | associations | Associate two records with an association type (v3). |
| DELETE | crm/v3/objects/{id}/{id}/associations/{id}/{id}/{id} | write | associations | Remove an association between two records (v3). |
| GET | crm/objects/{id}/{id}/{id}/associations/{id} | read | associations | List records of one type associated with a record (date-versioned path). |
| PUT | crm/objects/{id}/{id}/{id}/associations/{id}/{id}/{id} | write | associations | Associate two records with an association type (date-versioned path). |
| DELETE | crm/objects/{id}/{id}/{id}/associations/{id}/{id}/{id} | write | associations | Remove an association between two records (date-versioned path). |
| PUT | crm/objects/{id}/{id}/{id}/associations/{id}/{id} | write | associations | Associate two records with labels (date-versioned path). |
| PUT | crm/objects/{id}/{id}/{id}/associations/default/{id}/{id} | write | associations | Associate two records with the default association type (date-versioned path). |
| DELETE | crm/objects/{id}/{id}/{id}/associations/{id}/{id} | write | associations | Remove all associations between two records (date-versioned path). |
| GET | crm/v4/objects/{id}/{id}/associations/{id} | read | associations | List records of one type associated with a record (v4). |
| PUT | crm/v4/objects/{id}/{id}/associations/{id}/{id} | write | associations | Associate two records with labels (v4). |
| PUT | crm/v4/objects/{id}/{id}/associations/default/{id}/{id} | write | associations | Associate two records with the default association type (v4). |
| DELETE | crm/v4/objects/{id}/{id}/associations/{id}/{id} | write | associations | Remove all associations between two records (v4). |
| GET | crm/v3/associations/{id}/{id}/types | read | associations | List association types between two object types (v3). |
| POST | crm/v3/associations/{id}/{id}/batch/read | read | associations | Read associations for a batch of records (v3); POST only carries the ID list. |
| POST | crm/v3/associations/{id}/{id}/batch/create | write | associations | Create a batch of associations (v3). |
| POST | crm/v3/associations/{id}/{id}/batch/archive | write | associations | Remove a batch of associations (v3). |
| POST | crm/v4/associations/{id}/{id}/batch/read | read | associations | Read associations for a batch of records; POST only carries the ID list (v4). |
| POST | crm/v4/associations/{id}/{id}/batch/create | write | associations | Create a batch of labelled associations (v4). |
| POST | crm/v4/associations/{id}/{id}/batch/associate/default | write | associations | Create a batch of default associations (v4). |
| POST | crm/v4/associations/{id}/{id}/batch/archive | write | associations | Remove a batch of associations (v4). |
| POST | crm/v4/associations/{id}/{id}/batch/labels/archive | write | associations | Remove specific labels from a batch of associations (v4). |
| GET | crm/v4/associations/{id}/{id}/labels | read | associations | List association labels between two object types (v4). |
| POST | crm/v4/associations/{id}/{id}/labels | write | associations | Create an association label (v4). |
| PUT | crm/v4/associations/{id}/{id}/labels | write | associations | Update an association label (v4). |
| DELETE | crm/v4/associations/{id}/{id}/labels/{id} | write | associations | Delete an association label (v4). |
| POST | crm/v4/associations/usage/high-usage-report/{id} | write | associations | Request a high-association-usage report, which HubSpot generates and sends to a user (v4). |
| POST | crm/associations/{id}/{id}/{id}/batch/read | read | associations | Read associations for a batch of records; POST only carries the ID list (date-versioned or version-first path). |
| POST | crm/associations/{id}/{id}/{id}/batch/create | write | associations | Create a batch of labelled associations (date-versioned or version-first path). |
| POST | crm/associations/{id}/{id}/{id}/batch/associate/default | write | associations | Create a batch of default associations (date-versioned or version-first path). |
| POST | crm/associations/{id}/{id}/{id}/batch/archive | write | associations | Remove a batch of associations (date-versioned or version-first path). |
| POST | crm/associations/{id}/{id}/{id}/batch/labels/archive | write | associations | Remove specific labels from a batch of associations (date-versioned or version-first path). |
| GET | crm/associations/{id}/{id}/{id}/labels | read | associations | List association labels between two object types (date-versioned or version-first path). |
| POST | crm/associations/{id}/{id}/{id}/labels | write | associations | Create an association label (date-versioned or version-first path). |
| PUT | crm/associations/{id}/{id}/{id}/labels | write | associations | Update an association label (date-versioned or version-first path). |
| DELETE | crm/associations/{id}/{id}/{id}/labels/{id} | write | associations | Delete an association label (date-versioned or version-first path). |
| POST | crm/associations/{id}/usage/high-usage-report/{id} | write | associations | Request a high-association-usage report, which HubSpot generates and sends to a user (date-versioned or version-first path). |
| GET | crm/associations/{id}/definitions/configurations/all | read | associations | List all association limit configurations. |
| GET | crm/associations/{id}/definitions/configurations/{id}/{id} | read | associations | Get association limit configurations between two object types. |
| POST | crm/associations/{id}/definitions/configurations/{id}/{id}/batch/create | write | associations | Create association limit configurations. |
| POST | crm/associations/{id}/definitions/configurations/{id}/{id}/batch/update | write | associations | Update association limit configurations. |
| POST | crm/associations/{id}/definitions/configurations/{id}/{id}/batch/purge | write | associations | Remove association limit configurations. |
| GET | crm/v3/properties/{id} | read | properties | List the properties of an object type. |
| GET | crm/v3/properties/{id}/{id} | read | properties | Get a property definition. |
| POST | crm/v3/properties/{id}/batch/read | read | properties | Read a batch of property definitions; POST only carries the names. |
| POST | crm/v3/properties/{id} | write | properties | Create a property. |
| PATCH | crm/v3/properties/{id}/{id} | write | properties | Update a property. |
| DELETE | crm/v3/properties/{id}/{id} | write | properties | Archive a property. |
| POST | crm/v3/properties/{id}/batch/create | write | properties | Create a batch of properties. |
| POST | crm/v3/properties/{id}/batch/archive | write | properties | Archive a batch of properties. |
| GET | crm/properties/{id}/{id} | read | properties | List the properties of an object type (date-versioned path). |
| GET | crm/properties/{id}/{id}/{id} | read | properties | Get a property definition (date-versioned path). |
| POST | crm/properties/{id}/{id}/batch/read | read | properties | Read a batch of property definitions; POST only carries the names (date-versioned path). |
| POST | crm/properties/{id}/{id} | write | properties | Create a property (date-versioned path). |
| PATCH | crm/properties/{id}/{id}/{id} | write | properties | Update a property (date-versioned path). |
| DELETE | crm/properties/{id}/{id}/{id} | write | properties | Archive a property (date-versioned path). |
| POST | crm/properties/{id}/{id}/batch/create | write | properties | Create a batch of properties (date-versioned path). |
| POST | crm/properties/{id}/{id}/batch/archive | write | properties | Archive a batch of properties (date-versioned path). |
| GET | crm/v3/properties/{id}/groups | read | property groups | List the property groups of an object type. |
| GET | crm/v3/properties/{id}/groups/{id} | read | property groups | Get a property group. |
| POST | crm/v3/properties/{id}/groups | write | property groups | Create a property group. |
| PATCH | crm/v3/properties/{id}/groups/{id} | write | property groups | Update a property group. |
| DELETE | crm/v3/properties/{id}/groups/{id} | write | property groups | Archive a property group. |
| GET | crm/properties/{id}/{id}/groups | read | property groups | List the property groups of an object type (date-versioned path). |
| GET | crm/properties/{id}/{id}/groups/{id} | read | property groups | Get a property group (date-versioned path). |
| POST | crm/properties/{id}/{id}/groups | write | property groups | Create a property group (date-versioned path). |
| PATCH | crm/properties/{id}/{id}/groups/{id} | write | property groups | Update a property group (date-versioned path). |
| DELETE | crm/properties/{id}/{id}/groups/{id} | write | property groups | Archive a property group (date-versioned path). |
| GET | crm/v3/property-validations/{id} | read | property validations | List property validation rules for an object type. |
| GET | crm/v3/property-validations/{id}/{id} | read | property validations | List validation rules for a property. |
| GET | crm/v3/property-validations/{id}/{id}/rule-type/{id} | read | property validations | Get one validation rule of a property. |
| PUT | crm/v3/property-validations/{id}/{id}/rule-type/{id} | write | property validations | Set a validation rule on a property. |
| GET | crm/property-validations/{id}/{id} | read | property validations | List property validation rules for an object type (date-versioned path). |
| GET | crm/property-validations/{id}/{id}/{id} | read | property validations | List validation rules for a property (date-versioned path). |
| GET | crm/property-validations/{id}/{id}/{id}/rule-type/{id} | read | property validations | Get one validation rule of a property (date-versioned path). |
| PUT | crm/property-validations/{id}/{id}/{id}/rule-type/{id} | write | property validations | Set a validation rule on a property (date-versioned path). |
| GET | crm/v3/schemas | read | schemas | List custom object schemas (older crm/v3/schemas path). |
| GET | crm/v3/schemas/{id} | read | schemas | Get a custom object schema (older crm/v3/schemas path). |
| POST | crm/v3/schemas | write | schemas | Create a custom object schema (older crm/v3/schemas path). |
| PATCH | crm/v3/schemas/{id} | write | schemas | Update a custom object schema (older crm/v3/schemas path). |
| DELETE | crm/v3/schemas/{id} | write | schemas | Delete a custom object schema (older crm/v3/schemas path). |
| POST | crm/v3/schemas/{id}/associations | write | schemas | Add an association definition to a custom object schema (older crm/v3/schemas path). |
| DELETE | crm/v3/schemas/{id}/associations/{id} | write | schemas | Remove an association definition from a custom object schema (older crm/v3/schemas path). |
| GET | crm-object-schemas/{id}/schemas | read | schemas | List custom object schemas. |
| GET | crm-object-schemas/{id}/schemas/{id} | read | schemas | Get a custom object schema. |
| POST | crm-object-schemas/{id}/schemas | write | schemas | Create a custom object schema. |
| PATCH | crm-object-schemas/{id}/schemas/{id} | write | schemas | Update a custom object schema. |
| DELETE | crm-object-schemas/{id}/schemas/{id} | write | schemas | Delete a custom object schema. |
| POST | crm-object-schemas/{id}/schemas/{id}/associations | write | schemas | Add an association definition to a custom object schema. |
| DELETE | crm-object-schemas/{id}/schemas/{id}/associations/{id} | write | schemas | Remove an association definition from a custom object schema. |
| POST | crm-object-schemas/{id}/schemas/batch/read | read | schemas | Read a batch of custom object schemas; POST only carries the ID list. |
| GET | crm/v3/pipelines/{id} | read | pipelines | List the pipelines of an object type. |
| GET | crm/v3/pipelines/{id}/{id} | read | pipelines | Get a pipeline. |
| GET | crm/v3/pipelines/{id}/{id}/audit | read | pipelines | Get the change history of a pipeline. |
| GET | crm/v3/pipelines/{id}/{id}/stages | read | pipelines | List the stages of a pipeline. |
| GET | crm/v3/pipelines/{id}/{id}/stages/{id} | read | pipelines | Get a pipeline stage. |
| GET | crm/v3/pipelines/{id}/{id}/stages/{id}/audit | read | pipelines | Get the change history of a pipeline stage. |
| POST | crm/v3/pipelines/{id} | write | pipelines | Create a pipeline. |
| PUT | crm/v3/pipelines/{id}/{id} | write | pipelines | Replace a pipeline. |
| PATCH | crm/v3/pipelines/{id}/{id} | write | pipelines | Update a pipeline. |
| DELETE | crm/v3/pipelines/{id}/{id} | write | pipelines | Delete a pipeline. |
| POST | crm/v3/pipelines/{id}/{id}/stages | write | pipelines | Create a pipeline stage. |
| PUT | crm/v3/pipelines/{id}/{id}/stages/{id} | write | pipelines | Replace a pipeline stage. |
| PATCH | crm/v3/pipelines/{id}/{id}/stages/{id} | write | pipelines | Update a pipeline stage. |
| DELETE | crm/v3/pipelines/{id}/{id}/stages/{id} | write | pipelines | Delete a pipeline stage. |
| GET | crm/pipelines/{id}/{id} | read | pipelines | List the pipelines of an object type (date-versioned path). |
| GET | crm/pipelines/{id}/{id}/{id} | read | pipelines | Get a pipeline (date-versioned path). |
| GET | crm/pipelines/{id}/{id}/{id}/audit | read | pipelines | Get the change history of a pipeline (date-versioned path). |
| GET | crm/pipelines/{id}/{id}/{id}/stages | read | pipelines | List the stages of a pipeline (date-versioned path). |
| GET | crm/pipelines/{id}/{id}/{id}/stages/{id} | read | pipelines | Get a pipeline stage (date-versioned path). |
| GET | crm/pipelines/{id}/{id}/{id}/stages/{id}/audit | read | pipelines | Get the change history of a pipeline stage (date-versioned path). |
| POST | crm/pipelines/{id}/{id} | write | pipelines | Create a pipeline (date-versioned path). |
| PUT | crm/pipelines/{id}/{id}/{id} | write | pipelines | Replace a pipeline (date-versioned path). |
| PATCH | crm/pipelines/{id}/{id}/{id} | write | pipelines | Update a pipeline (date-versioned path). |
| DELETE | crm/pipelines/{id}/{id}/{id} | write | pipelines | Delete a pipeline (date-versioned path). |
| POST | crm/pipelines/{id}/{id}/{id}/stages | write | pipelines | Create a pipeline stage (date-versioned path). |
| PUT | crm/pipelines/{id}/{id}/{id}/stages/{id} | write | pipelines | Replace a pipeline stage (date-versioned path). |
| PATCH | crm/pipelines/{id}/{id}/{id}/stages/{id} | write | pipelines | Update a pipeline stage (date-versioned path). |
| DELETE | crm/pipelines/{id}/{id}/{id}/stages/{id} | write | pipelines | Delete a pipeline stage (date-versioned path). |
| GET | crm/v3/owners | read | owners | List owners. |
| GET | crm/v3/owners/{id} | read | owners | Get an owner by ID. |
| GET | crm/owners/{id} | read | owners | List owners (date-versioned path). |
| GET | crm/owners/{id}/{id} | read | owners | Get an owner by ID (date-versioned path). |
| GET | crm/v3/lists | read | lists | Get several lists by ID. |
| GET | crm/v3/lists/{id} | read | lists | Get a list by ID. |
| GET | crm/v3/lists/object-type-id/{id}/name/{id} | read | lists | Get a list by name and object type. |
| POST | crm/v3/lists/search | read | lists | Search lists; POST only carries the query. |
| GET | crm/v3/lists/idmapping | read | lists | Translate a legacy list ID to a list ID. |
| POST | crm/v3/lists/idmapping | read | lists | Translate a batch of legacy list IDs; POST only carries the IDs. |
| GET | crm/v3/lists/{id}/memberships | read | lists | List the records in a list. |
| GET | crm/v3/lists/{id}/memberships/join-order | read | lists | List the records in a list ordered by date added. |
| GET | crm/v3/lists/records/{id}/{id}/memberships | read | lists | List the lists a record belongs to. |
| POST | crm/v3/lists/records/memberships/batch/read | read | lists | Read list memberships for a batch of records; POST only carries the IDs. |
| GET | crm/v3/lists/{id}/schedule-conversion | read | lists | Get the scheduled conversion of a list. |
| GET | crm/v3/lists/{id}/size-and-edits-history/between | read | lists | Get the size and edit history of a list. |
| GET | crm/v3/lists/folders | read | lists | Get list folders. |
| POST | crm/v3/lists | write | lists | Create a list. |
| DELETE | crm/v3/lists/{id} | write | lists | Delete a list. |
| PUT | crm/v3/lists/{id}/restore | write | lists | Restore a deleted list. |
| PUT | crm/v3/lists/{id}/update-list-name | write | lists | Rename a list. |
| PUT | crm/v3/lists/{id}/update-list-filters | write | lists | Change the filter definition of a list. |
| PUT | crm/v3/lists/{id}/memberships/add | write | lists | Add records to a list. |
| PUT | crm/v3/lists/{id}/memberships/remove | write | lists | Remove records from a list. |
| PUT | crm/v3/lists/{id}/memberships/add-and-remove | write | lists | Add and remove records of a list in one call. |
| PUT | crm/v3/lists/{id}/memberships/add-from/{id} | write | lists | Add all records of another list to a list. |
| DELETE | crm/v3/lists/{id}/memberships | write | lists | Remove all records from a list. |
| PUT | crm/v3/lists/{id}/schedule-conversion | write | lists | Schedule the conversion of an active list to a static list. |
| DELETE | crm/v3/lists/{id}/schedule-conversion | write | lists | Cancel the scheduled conversion of a list. |
| POST | crm/v3/lists/folders | write | lists | Create a list folder. |
| PUT | crm/v3/lists/folders/move-list | write | lists | Move a list into a folder. |
| PUT | crm/v3/lists/folders/{id}/move/{id} | write | lists | Move a list folder. |
| PUT | crm/v3/lists/folders/{id}/rename | write | lists | Rename a list folder. |
| DELETE | crm/v3/lists/folders/{id} | write | lists | Delete a list folder. |
| GET | crm/lists/{id} | read | lists | Get several lists by ID (date-versioned path). |
| GET | crm/lists/{id}/{id} | read | lists | Get a list by ID (date-versioned path). |
| GET | crm/lists/{id}/object-type-id/{id}/name/{id} | read | lists | Get a list by name and object type (date-versioned path). |
| POST | crm/lists/{id}/search | read | lists | Search lists; POST only carries the query (date-versioned path). |
| GET | crm/lists/{id}/idmapping | read | lists | Translate a legacy list ID to a list ID (date-versioned path). |
| POST | crm/lists/{id}/idmapping | read | lists | Translate a batch of legacy list IDs; POST only carries the IDs (date-versioned path). |
| GET | crm/lists/{id}/{id}/memberships | read | lists | List the records in a list (date-versioned path). |
| GET | crm/lists/{id}/{id}/memberships/join-order | read | lists | List the records in a list ordered by date added (date-versioned path). |
| GET | crm/lists/{id}/records/{id}/{id}/memberships | read | lists | List the lists a record belongs to (date-versioned path). |
| POST | crm/lists/{id}/records/memberships/batch/read | read | lists | Read list memberships for a batch of records; POST only carries the IDs (date-versioned path). |
| GET | crm/lists/{id}/{id}/schedule-conversion | read | lists | Get the scheduled conversion of a list (date-versioned path). |
| GET | crm/lists/{id}/{id}/size-and-edits-history/between | read | lists | Get the size and edit history of a list (date-versioned path). |
| GET | crm/lists/{id}/folders | read | lists | Get list folders (date-versioned path). |
| POST | crm/lists/{id} | write | lists | Create a list (date-versioned path). |
| DELETE | crm/lists/{id}/{id} | write | lists | Delete a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/restore | write | lists | Restore a deleted list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/update-list-name | write | lists | Rename a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/update-list-filters | write | lists | Change the filter definition of a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/memberships/add | write | lists | Add records to a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/memberships/remove | write | lists | Remove records from a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/memberships/add-and-remove | write | lists | Add and remove records of a list in one call (date-versioned path). |
| PUT | crm/lists/{id}/{id}/memberships/add-from/{id} | write | lists | Add all records of another list to a list (date-versioned path). |
| DELETE | crm/lists/{id}/{id}/memberships | write | lists | Remove all records from a list (date-versioned path). |
| PUT | crm/lists/{id}/{id}/schedule-conversion | write | lists | Schedule the conversion of an active list to a static list (date-versioned path). |
| DELETE | crm/lists/{id}/{id}/schedule-conversion | write | lists | Cancel the scheduled conversion of a list (date-versioned path). |
| POST | crm/lists/{id}/folders | write | lists | Create a list folder (date-versioned path). |
| PUT | crm/lists/{id}/folders/move-list | write | lists | Move a list into a folder (date-versioned path). |
| PUT | crm/lists/{id}/folders/{id}/move/{id} | write | lists | Move a list folder (date-versioned path). |
| PUT | crm/lists/{id}/folders/{id}/rename | write | lists | Rename a list folder (date-versioned path). |
| DELETE | crm/lists/{id}/folders/{id} | write | lists | Delete a list folder (date-versioned path). |
| POST | crm/lists/{id}/all | read | lists | List all lists with paging; POST only carries the paging options (date-versioned path). |
| GET | crm/v3/imports | read | imports | List imports. |
| GET | crm/v3/imports/{id} | read | imports | Get the status of an import. |
| GET | crm/v3/imports/{id}/errors | read | imports | List the errors of an import. |
| POST | crm/v3/imports | write | imports | Start an import that creates or updates records from an uploaded file. |
| POST | crm/v3/imports/{id}/cancel | write | imports | Cancel a running import. |
| GET | crm/imports/{id} | read | imports | List imports (date-versioned path). |
| GET | crm/imports/{id}/{id} | read | imports | Get the status of an import (date-versioned path). |
| GET | crm/imports/{id}/{id}/errors | read | imports | List the errors of an import (date-versioned path). |
| POST | crm/imports/{id} | write | imports | Start an import that creates or updates records from an uploaded file (date-versioned path). |
| POST | crm/imports/{id}/{id}/cancel | write | imports | Cancel a running import (date-versioned path). |
| GET | crm/v3/exports/export/{id} | read | exports | Get the details of an export. |
| GET | crm/v3/exports/export/async/tasks/{id}/status | read | exports | Get the status of an export task, including the file download URL once complete. |
| POST | crm/v3/exports/export/async | write | exports | Start an export, which creates an export job and a downloadable file in the account. |
| GET | crm/exports/{id}/export/{id} | read | exports | Get the details of an export (date-versioned path). |
| GET | crm/exports/{id}/export/async/tasks/{id}/status | read | exports | Get the status of an export task, including the file download URL once complete (date-versioned path). |
| POST | crm/exports/{id}/export/async | write | exports | Start an export, which creates an export job and a downloadable file in the account (date-versioned path). |
| GET | crm/v3/limits/records | read | limits | Get record limits and usage. |
| GET | crm/v3/limits/custom-object-types | read | limits | Get custom object type limits and usage. |
| GET | crm/v3/limits/custom-properties | read | limits | Get custom property limits and usage. |
| GET | crm/v3/limits/calculated-properties | read | limits | Get calculated property limits and usage. |
| GET | crm/v3/limits/pipelines | read | limits | Get pipeline limits and usage. |
| GET | crm/v3/limits/associations/labels | read | limits | Get association label limits and usage. |
| GET | crm/v3/limits/associations/records/from | read | limits | Get record association limits and usage. |
| GET | crm/v3/limits/associations/records/{id}/to | read | limits | Get record association limits from an object type. |
| GET | crm/v3/limits/associations/records/{id}/{id} | read | limits | Get record association limits between two object types. |
| GET | crm/limits/{id}/records | read | limits | Get record limits and usage (date-versioned path). |
| GET | crm/limits/{id}/custom-object-types | read | limits | Get custom object type limits and usage (date-versioned path). |
| GET | crm/limits/{id}/custom-properties | read | limits | Get custom property limits and usage (date-versioned path). |
| GET | crm/limits/{id}/calculated-properties | read | limits | Get calculated property limits and usage (date-versioned path). |
| GET | crm/limits/{id}/pipelines | read | limits | Get pipeline limits and usage (date-versioned path). |
| GET | crm/limits/{id}/associations/labels | read | limits | Get association label limits and usage (date-versioned path). |
| GET | crm/limits/{id}/associations/records/from | read | limits | Get record association limits and usage (date-versioned path). |
| GET | crm/limits/{id}/associations/records/{id}/to | read | limits | Get record association limits from an object type (date-versioned path). |
| GET | crm/limits/{id}/associations/records/{id}/{id} | read | limits | Get record association limits between two object types (date-versioned path). |
| GET | account-info/{id}/details | read | account | Get account details such as portal ID, time zone and currency. |
| GET | account-info/{id}/api-usage/daily | read | account | Get daily API usage and limits for the account. |
| GET | account-info/{id}/api-usage/daily/private-apps | read | account | Get daily API usage of private apps. |
| GET | account-info/{id}/api-usage/daily/privately-distributed | read | account | Get daily API usage of privately distributed apps. |
| GET | account-info/{id}/activity/audit-logs | read | account | List account audit log entries. |
| GET | account-info/{id}/activity/login | read | account | List account login activity. |
| GET | account-info/{id}/activity/security | read | account | List account security activity. |
| GET | business-units/v3/business-units/user/{id} | read | account | List the business units (brands) a user belongs to. |
| GET | business-units/public/{id}/business-units/user/{id} | read | account | List the business units (brands) a user belongs to (date-versioned path). |
| DELETE | appinstalls/{id}/external-install | write | account | Uninstall the connected app from the account. |
| GET | tax-rates/{id}/tax-rates | read | tax rates | List tax rates. |
| GET | tax-rates/{id}/tax-rates/{id} | read | tax rates | Get a tax rate. |
| GET | oauth/v1/access-tokens/{id} | write | oauth | Get access token metadata; kept out of read because the path carries a raw token and the response echoes it. |
| GET | oauth/v1/refresh-tokens/{id} | write | oauth | Get refresh token metadata; kept out of read because the path carries a raw token and the response echoes it. |
| DELETE | oauth/v1/refresh-tokens/{id} | write | oauth | Revoke a refresh token. |
| POST | oauth/{id}/token | write | oauth | Exchange a code or refresh token for new tokens; issues credentials. |
| POST | oauth/{id}/token/introspect | write | oauth | Introspect a token; kept out of read because it takes client credentials and raw tokens. |
| POST | oauth/{id}/token/revoke | write | oauth | Revoke a token. |
| GET | settings/v3/users | read | settings users | List the users of the account. |
| GET | settings/v3/users/{id} | read | settings users | Get a user of the account. |
| GET | settings/v3/users/roles | read | settings users | List the roles of the account. |
| GET | settings/v3/users/teams | read | settings users | List the teams of the account. |
| POST | settings/v3/users | write | settings users | Add a user to the account, which sends an invitation. |
| PUT | settings/v3/users/{id} | write | settings users | Change a user's role or teams. |
| DELETE | settings/v3/users/{id} | write | settings users | Remove a user from the account. |
| GET | settings/users/{id} | read | settings users | List the users of the account (date-versioned or version-first path). |
| GET | settings/users/{id}/{id} | read | settings users | Get a user of the account (date-versioned or version-first path). |
| GET | settings/users/{id}/roles | read | settings users | List the roles of the account (date-versioned or version-first path). |
| GET | settings/users/{id}/teams | read | settings users | List the teams of the account (date-versioned or version-first path). |
| GET | settings/users/{id}/seats | read | settings users | List the seats of the account (date-versioned or version-first path). |
| POST | settings/users/{id} | write | settings users | Add a user to the account, which sends an invitation (date-versioned or version-first path). |
| PUT | settings/users/{id}/{id} | write | settings users | Change a user's role or teams (date-versioned or version-first path). |
| DELETE | settings/users/{id}/{id} | write | settings users | Remove a user from the account (date-versioned or version-first path). |
| GET | settings/teams/{id} | read | teams | List teams (date-versioned path). |
| GET | settings/teams/{id}/{id} | read | teams | Get a team (date-versioned path). |
| GET | settings/teams/{id}/{id}/members | read | teams | List the members of a team (date-versioned path). |
| POST | settings/teams/{id} | write | teams | Create a team (date-versioned path). |
| PATCH | settings/teams/{id}/{id} | write | teams | Update a team (date-versioned path). |
| DELETE | settings/teams/{id}/{id} | write | teams | Delete a team (date-versioned path). |
| POST | settings/teams/{id}/{id}/members | write | teams | Add members to a team (date-versioned path). |
| POST | settings/teams/{id}/{id}/members/batch | write | teams | Assign a batch of members to a team (date-versioned path). |
| DELETE | settings/teams/{id}/{id}/members/{id} | write | teams | Remove a member from a team (date-versioned path). |
| GET | settings/v3/currencies/codes | read | currencies | List supported currency codes. |
| GET | settings/v3/currencies/company-currency | read | currencies | Get the company currency. |
| GET | settings/v3/currencies/exchange-rates | read | currencies | List exchange rates. |
| GET | settings/v3/currencies/exchange-rates/current | read | currencies | List current exchange rates. |
| GET | settings/v3/currencies/exchange-rates/{id} | read | currencies | Get an exchange rate. |
| POST | settings/v3/currencies/exchange-rates/batch/read | read | currencies | Read a batch of exchange rates; POST only carries the ID list. |
| GET | settings/v3/currencies/central-fx-rates/information | read | currencies | Get central exchange rate settings. |
| GET | settings/v3/currencies/central-fx-rates/unsupported-currencies | read | currencies | List currencies not covered by central exchange rates. |
| PUT | settings/v3/currencies/company-currency | write | currencies | Set the company currency. |
| POST | settings/v3/currencies/exchange-rates | write | currencies | Add an exchange rate. |
| PATCH | settings/v3/currencies/exchange-rates/{id} | write | currencies | Update an exchange rate. |
| POST | settings/v3/currencies/exchange-rates/batch/create | write | currencies | Create a batch of exchange rates. |
| POST | settings/v3/currencies/exchange-rates/batch/update | write | currencies | Update a batch of exchange rates. |
| POST | settings/v3/currencies/exchange-rates/update-visibility | write | currencies | Show or hide a currency. |
| POST | settings/v3/currencies/central-fx-rates/add-currency | write | currencies | Add a currency that uses central exchange rates. |
| GET | settings/currencies/{id}/codes | read | currencies | List supported currency codes (date-versioned path). |
| GET | settings/currencies/{id}/company-currency | read | currencies | Get the company currency (date-versioned path). |
| GET | settings/currencies/{id}/exchange-rates | read | currencies | List exchange rates (date-versioned path). |
| GET | settings/currencies/{id}/exchange-rates/current | read | currencies | List current exchange rates (date-versioned path). |
| GET | settings/currencies/{id}/exchange-rates/{id} | read | currencies | Get an exchange rate (date-versioned path). |
| POST | settings/currencies/{id}/exchange-rates/batch/read | read | currencies | Read a batch of exchange rates; POST only carries the ID list (date-versioned path). |
| GET | settings/currencies/{id}/central-fx-rates/information | read | currencies | Get central exchange rate settings (date-versioned path). |
| GET | settings/currencies/{id}/central-fx-rates/unsupported-currencies | read | currencies | List currencies not covered by central exchange rates (date-versioned path). |
| PUT | settings/currencies/{id}/company-currency | write | currencies | Set the company currency (date-versioned path). |
| POST | settings/currencies/{id}/exchange-rates | write | currencies | Add an exchange rate (date-versioned path). |
| PATCH | settings/currencies/{id}/exchange-rates/{id} | write | currencies | Update an exchange rate (date-versioned path). |
| POST | settings/currencies/{id}/exchange-rates/batch/create | write | currencies | Create a batch of exchange rates (date-versioned path). |
| POST | settings/currencies/{id}/exchange-rates/batch/update | write | currencies | Update a batch of exchange rates (date-versioned path). |
| POST | settings/currencies/{id}/exchange-rates/update-visibility | write | currencies | Show or hide a currency (date-versioned path). |
| POST | settings/currencies/{id}/central-fx-rates/add-currency | write | currencies | Add a currency that uses central exchange rates (date-versioned path). |
