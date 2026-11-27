# Make access policy

An access policy limits which endpoints Make connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/make#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Make: its 197 read-only endpoints, plus deny rules for the 1 write endpoint a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create make --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v2/affiliate/commission-info"},
    {"method": "GET", "path": "api/v2/affiliate/commissions"},
    {"method": "GET", "path": "api/v2/affiliate/partner-register"},
    {"method": "GET", "path": "api/v2/affiliate/partner-settings"},
    {"method": "GET", "path": "api/v2/affiliate/stats"},
    {"method": "GET", "path": "api/v2/agents"},
    {"method": "GET", "path": "api/v2/agents/{id}"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/agents"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/agents/{id}"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/contexts"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/llm-providers"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/llm-providers/{id}"},
    {"method": "GET", "path": "api/v2/ai-agents/v1/llm-providers/{id}/models"},
    {"method": "GET", "path": "api/v2/analytics/{id}"},
    {"method": "GET", "path": "api/v2/imt/apps/{id}/{id}/modules-with-credentials"},
    {"method": "GET", "path": "api/v2/audit-logs/organization/{id}"},
    {"method": "GET", "path": "api/v2/audit-logs/organization/{id}/filters"},
    {"method": "GET", "path": "api/v2/audit-logs/team/{id}"},
    {"method": "GET", "path": "api/v2/audit-logs/team/{id}/filters"},
    {"method": "GET", "path": "api/v2/audit-logs/v2/organization/{id}"},
    {"method": "GET", "path": "api/v2/audit-logs/v2/organization/{id}/filters"},
    {"method": "GET", "path": "api/v2/audit-logs/v2/team/{id}"},
    {"method": "GET", "path": "api/v2/audit-logs/v2/team/{id}/filters"},
    {"method": "GET", "path": "api/v2/audit-logs/v2/{id}/{id}"},
    {"method": "GET", "path": "api/v2/audit-logs/{id}/{id}"},
    {"method": "GET", "path": "api/v2/cashier/prices/{id}"},
    {"method": "GET", "path": "api/v2/cashier/vat-validation/patterns"},
    {"method": "GET", "path": "api/v2/connections"},
    {"method": "GET", "path": "api/v2/connections/{id}"},
    {"method": "GET", "path": "api/v2/connections/{id}/editable-data-schema"},
    {"method": "GET", "path": "api/v2/credential-requests/apps/{id}/{id}/modules-with-credentials"},
    {"method": "GET", "path": "api/v2/credential-requests/requests"},
    {"method": "GET", "path": "api/v2/credential-requests/requests/{id}"},
    {"method": "GET", "path": "api/v2/credential-requests/requests/{id}/detail"},
    {"method": "GET", "path": "api/v2/custom-property-structures"},
    {"method": "GET", "path": "api/v2/custom-property-structures/{id}/custom-property-structure-items"},
    {"method": "GET", "path": "api/v2/data-stores"},
    {"method": "GET", "path": "api/v2/data-stores/{id}"},
    {"method": "GET", "path": "api/v2/data-stores/{id}/data"},
    {"method": "GET", "path": "api/v2/data-structures"},
    {"method": "GET", "path": "api/v2/data-structures/{id}"},
    {"method": "GET", "path": "api/v2/devices"},
    {"method": "GET", "path": "api/v2/devices/{id}"},
    {"method": "GET", "path": "api/v2/devices/{id}/incomings"},
    {"method": "GET", "path": "api/v2/devices/{id}/incomings/stats"},
    {"method": "GET", "path": "api/v2/devices/{id}/incomings/{id}"},
    {"method": "GET", "path": "api/v2/devices/{id}/outgoings"},
    {"method": "GET", "path": "api/v2/devices/{id}/outgoings/{id}"},
    {"method": "GET", "path": "api/v2/dlqs"},
    {"method": "GET", "path": "api/v2/dlqs/{id}"},
    {"method": "GET", "path": "api/v2/dlqs/{id}/blueprint"},
    {"method": "GET", "path": "api/v2/dlqs/{id}/bundle"},
    {"method": "GET", "path": "api/v2/dlqs/{id}/logs"},
    {"method": "GET", "path": "api/v2/dlqs/{id}/logs/{id}"},
    {"method": "GET", "path": "api/v2/enums/apps-review-statuses"},
    {"method": "GET", "path": "api/v2/enums/countries"},
    {"method": "GET", "path": "api/v2/enums/imt-regions"},
    {"method": "GET", "path": "api/v2/enums/imt-zones"},
    {"method": "GET", "path": "api/v2/enums/languages"},
    {"method": "GET", "path": "api/v2/enums/locales"},
    {"method": "GET", "path": "api/v2/enums/module-types"},
    {"method": "GET", "path": "api/v2/enums/organization-features"},
    {"method": "GET", "path": "api/v2/enums/timezones"},
    {"method": "GET", "path": "api/v2/enums/us-states"},
    {"method": "GET", "path": "api/v2/enums/user-api-token-scopes"},
    {"method": "GET", "path": "api/v2/enums/user-email-notifications"},
    {"method": "GET", "path": "api/v2/enums/user-features"},
    {"method": "GET", "path": "api/v2/enums/variable-types"},
    {"method": "GET", "path": "api/v2/event-subscriptions/v1/organizations/{id}/event-types"},
    {"method": "GET", "path": "api/v2/event-subscriptions/v1/organizations/{id}/subscriptions"},
    {"method": "GET", "path": "api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}"},
    {"method": "GET", "path": "api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/deliveries"},
    {"method": "GET", "path": "api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/deliveries/{id}"},
    {"method": "GET", "path": "api/v2/functions"},
    {"method": "GET", "path": "api/v2/functions/{id}"},
    {"method": "GET", "path": "api/v2/functions/{id}/history"},
    {"method": "GET", "path": "api/v2/hooks/{id}/incomings"},
    {"method": "GET", "path": "api/v2/hooks/{id}/incomings/stats"},
    {"method": "GET", "path": "api/v2/hooks/{id}/incomings/{id}"},
    {"method": "GET", "path": "api/v2/hooks/{id}/logs"},
    {"method": "GET", "path": "api/v2/hooks/{id}/logs/{id}"},
    {"method": "GET", "path": "api/v2/keys"},
    {"method": "GET", "path": "api/v2/keys/types"},
    {"method": "GET", "path": "api/v2/keys/{id}"},
    {"method": "GET", "path": "api/v2/notifications"},
    {"method": "GET", "path": "api/v2/notifications/{id}"},
    {"method": "GET", "path": "api/v2/organizations"},
    {"method": "GET", "path": "api/v2/organizations/invitation"},
    {"method": "GET", "path": "api/v2/organizations/{id}"},
    {"method": "GET", "path": "api/v2/organizations/{id}/apps"},
    {"method": "GET", "path": "api/v2/organizations/{id}/check-team-permission"},
    {"method": "GET", "path": "api/v2/organizations/{id}/feature-controls"},
    {"method": "GET", "path": "api/v2/organizations/{id}/managed-organizations"},
    {"method": "GET", "path": "api/v2/organizations/{id}/managed-organizations-consumption"},
    {"method": "GET", "path": "api/v2/organizations/{id}/payments"},
    {"method": "GET", "path": "api/v2/organizations/{id}/private-spaces-settings"},
    {"method": "POST", "path": "api/v2/organizations/{id}/scenarios/executions/io-data/counts"},
    {"method": "POST", "path": "api/v2/organizations/{id}/scenarios/executions/io-data/search"},
    {"method": "POST", "path": "api/v2/organizations/{id}/scenarios/executions/search"},
    {"method": "POST", "path": "api/v2/organizations/{id}/scenarios/{id}/executions/{id}/io-data/search"},
    {"method": "GET", "path": "api/v2/organizations/{id}/sso-certificates"},
    {"method": "GET", "path": "api/v2/organizations/{id}/subscription"},
    {"method": "GET", "path": "api/v2/organizations/{id}/subscription/payment-method-types"},
    {"method": "GET", "path": "api/v2/organizations/{id}/subscription/payment-methods"},
    {"method": "GET", "path": "api/v2/organizations/{id}/universal-discount"},
    {"method": "GET", "path": "api/v2/organizations/{id}/usage"},
    {"method": "GET", "path": "api/v2/organizations/{id}/user-organization-roles"},
    {"method": "GET", "path": "api/v2/organizations/{id}/user-organization-roles/{id}"},
    {"method": "GET", "path": "api/v2/organizations/{id}/variables"},
    {"method": "GET", "path": "api/v2/organizations/{id}/variables/{id}/history"},
    {"method": "GET", "path": "api/v2/ping"},
    {"method": "GET", "path": "api/v2/private-spaces"},
    {"method": "GET", "path": "api/v2/private-spaces/{id}"},
    {"method": "GET", "path": "api/v2/scenario-labels"},
    {"method": "GET", "path": "api/v2/scenarios"},
    {"method": "GET", "path": "api/v2/scenarios/ai-agents"},
    {"method": "POST", "path": "api/v2/scenarios/ai-agents/modules"},
    {"method": "GET", "path": "api/v2/scenarios/consumptions"},
    {"method": "GET", "path": "api/v2/scenarios/trash/count"},
    {"method": "GET", "path": "api/v2/scenarios/{id}"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/blueprint"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/blueprints"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/build-variables"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/custom-properties"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/executions/{id}"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/interface"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/logs"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/logs/{id}"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/modules/operations"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/modules/{id}/logs"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/notes"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/notes/{id}"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/triggers"},
    {"method": "GET", "path": "api/v2/scenarios/{id}/usage"},
    {"method": "GET", "path": "api/v2/scenarios-folders"},
    {"method": "GET", "path": "api/v2/scenarios-shared"},
    {"method": "GET", "path": "api/v2/scenarios-shared/{id}"},
    {"method": "GET", "path": "api/v2/scenarios-shared/{id}/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps"},
    {"method": "GET", "path": "api/v2/sdk/apps/connections/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/connections/{id}/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/invites/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/webhooks/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/webhooks/{id}/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/connections"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/webhooks"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/changes/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/events-log"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/functions"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/functions/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/functions/{id}/code"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/functions/{id}/test"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/icon/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/modules"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/modules/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/modules/{id}/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/readme"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/review"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/rpcs"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/rpcs/{id}"},
    {"method": "GET", "path": "api/v2/sdk/apps/{id}/{id}/rpcs/{id}/{id}"},
    {"method": "GET", "path": "api/v2/teams"},
    {"method": "GET", "path": "api/v2/teams/{id}"},
    {"method": "GET", "path": "api/v2/teams/{id}/connections/{id}/access-list"},
    {"method": "GET", "path": "api/v2/teams/{id}/feature-controls"},
    {"method": "GET", "path": "api/v2/teams/{id}/keys/{id}/access-list"},
    {"method": "GET", "path": "api/v2/teams/{id}/usage"},
    {"method": "GET", "path": "api/v2/teams/{id}/user-team-roles"},
    {"method": "GET", "path": "api/v2/teams/{id}/user-team-roles/{id}"},
    {"method": "GET", "path": "api/v2/teams/{id}/variables"},
    {"method": "GET", "path": "api/v2/teams/{id}/variables/{id}/history"},
    {"method": "GET", "path": "api/v2/templates"},
    {"method": "GET", "path": "api/v2/templates/public"},
    {"method": "GET", "path": "api/v2/templates/public/{id}"},
    {"method": "GET", "path": "api/v2/templates/public/{id}/blueprint"},
    {"method": "GET", "path": "api/v2/templates/{id}"},
    {"method": "GET", "path": "api/v2/templates/{id}/blueprint"},
    {"method": "GET", "path": "api/v2/mailhub/users/{id}/organizations/{id}/teams/{id}/preferences"},
    {"method": "GET", "path": "api/v2/mailhub/users/{id}/preferences"},
    {"method": "GET", "path": "api/v2/users"},
    {"method": "GET", "path": "api/v2/users/by-permission"},
    {"method": "GET", "path": "api/v2/users/me"},
    {"method": "GET", "path": "api/v2/users/me/current-authorization"},
    {"method": "GET", "path": "api/v2/users/me/oauth-connections"},
    {"method": "GET", "path": "api/v2/users/me/onboarding-survey"},
    {"method": "GET", "path": "api/v2/users/me/organization-invitations"},
    {"method": "GET", "path": "api/v2/users/roles"},
    {"method": "GET", "path": "api/v2/users/roles/permissions"},
    {"method": "GET", "path": "api/v2/users/roles/{id}"},
    {"method": "GET", "path": "api/v2/users/unread-notifications"},
    {"method": "GET", "path": "api/v2/users/user-team-notifications/{id}"},
    {"method": "GET", "path": "api/v2/users/user-team-notifications/{id}/{id}"},
    {"method": "GET", "path": "api/v2/users/{id}/user-organization-roles"},
    {"method": "GET", "path": "api/v2/users/{id}/user-organization-roles/{id}"},
    {"method": "GET", "path": "api/v2/users/{id}/user-team-roles"},
    {"method": "GET", "path": "api/v2/users/{id}/user-team-roles/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "api/v2/sdk/apps/connections/{id}/common"}
  ]
}
```

## Endpoints

The Make endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v2/affiliate/commission-info | read | affiliate | Retrieves general info about accumulated commissions of the current user. |
| GET | api/v2/affiliate/commissions | read | affiliate | Retrieves detailed data about individual commisions of the current user. |
| GET | api/v2/affiliate/partner-register | read | affiliate | Returns what the affiliate partner registration form needs. |
| POST | api/v2/affiliate/partner-register | write | affiliate | Registers the user as a partner in the affiliate program. |
| GET | api/v2/affiliate/partner-settings | read | affiliate | Returns the payout settings of the user's affiliate partner. |
| POST | api/v2/affiliate/partner-settings | write | affiliate | Updates the Wise payout settings of the user's affiliate partner. |
| POST | api/v2/affiliate/payout-request | write | affiliate | Request a payout of available commissions. |
| POST | api/v2/affiliate/recipient/onboarding-link | write | affiliate | Creates a single-use, Stripe-hosted link where an affiliate partner paid out through Stripe enters or updates. |
| GET | api/v2/affiliate/stats | read | affiliate | Retrieves graph data for commisions in the past year for the current user. |
| GET | api/v2/agents | read | agents | Retrieves a collection of agents for a company with a given ID. |
| GET | api/v2/agents/{id} | read | agents | Retrieves an agents for a agent with given ID. |
| POST | api/v2/agents/{id} | write | agents | Creates a new agent. |
| PATCH | api/v2/agents/{id} | write | agents | Updates a new agent with given ID. |
| DELETE | api/v2/agents/{id} | write | agents | Removes an agent with a given ID. |
| GET | api/v2/ai-agents/v1/agents | read | ai-agents | Retrieve a list of all agents. |
| POST | api/v2/ai-agents/v1/agents | write | ai-agents | Create a new agent. |
| GET | api/v2/ai-agents/v1/agents/{id} | read | ai-agents | Retrieve an agent by its ID. |
| PATCH | api/v2/ai-agents/v1/agents/{id} | write | ai-agents | Modify an existing agent by its ID. |
| DELETE | api/v2/ai-agents/v1/agents/{id} | write | ai-agents | Delete an agent by its ID. |
| POST | api/v2/ai-agents/v1/agents/{id}/run | write | ai-agents | Run an agent with the provided ID. |
| POST | api/v2/ai-agents/v1/agents/{id}/run/stream | write | ai-agents | Run an agent with the provided ID and stream the response using Server Sent Events (SSE). |
| GET | api/v2/ai-agents/v1/contexts | read | ai-agents | Retrieve a list of all context for an agent. |
| POST | api/v2/ai-agents/v1/contexts | write | ai-agents | Create a new context with an optional file upload. |
| DELETE | api/v2/ai-agents/v1/contexts/{id} | write | ai-agents | Delete a context by its ID. |
| GET | api/v2/ai-agents/v1/llm-providers | read | ai-agents | Retrieve a list of all LLM providers. |
| GET | api/v2/ai-agents/v1/llm-providers/{id} | read | ai-agents | Retrieve details of a specific LLM provider by ID. |
| GET | api/v2/ai-agents/v1/llm-providers/{id}/models | read | ai-agents | Retrieve a list of models for a specific LLM provider by ID. |
| GET | api/v2/analytics/{id} | read | analytics | Gets analytics data for the specified organization. |
| GET | api/v2/imt/apps/{id}/{id}/modules-with-credentials | read | apps | Deprecated. |
| GET | api/v2/audit-logs/organization/{id} | read | audit-logs | Gets a list of all audit log entries for the specified organization. |
| GET | api/v2/audit-logs/organization/{id}/filters | read | audit-logs | Gets available audit logs filters for the organization. |
| GET | api/v2/audit-logs/team/{id} | read | audit-logs | Gets a list of all audit log entries for the specified team. |
| GET | api/v2/audit-logs/team/{id}/filters | read | audit-logs | Gets available audit logs filters for the team. |
| GET | api/v2/audit-logs/v2/organization/{id} | read | audit-logs | Gets a list of all audit log entries for the specified organization. |
| GET | api/v2/audit-logs/v2/organization/{id}/filters | read | audit-logs | Gets available audit logs filters for the organization. |
| GET | api/v2/audit-logs/v2/team/{id} | read | audit-logs | Gets a list of all audit log entries for the specified team. |
| GET | api/v2/audit-logs/v2/team/{id}/filters | read | audit-logs | Gets available audit logs filters for the team. |
| GET | api/v2/audit-logs/v2/{id}/{id} | read | audit-logs | Gets details of the audit log entry with the specified UUID. |
| GET | api/v2/audit-logs/{id}/{id} | read | audit-logs | Gets details of the audit log entry with the specified UUID. |
| GET | api/v2/cashier/prices/{id} | read | cashier | Get price detail. |
| GET | api/v2/cashier/vat-validation/patterns | read | cashier | Proxies imt-cashier's VAT-ID format patterns (EU + Northern Ireland). |
| GET | api/v2/connections | read | connections | Retrieves a collection of all connections for a team with a given ID. |
| POST | api/v2/connections | write | connections | Creates a new connection with data passed in the request body. |
| GET | api/v2/connections/{id} | read | connections | Retrieves details of a connection with a given ID. |
| PATCH | api/v2/connections/{id} | write | connections | Updates the specified connection's name. |
| DELETE | api/v2/connections/{id} | write | connections | Deletes a connection with a given ID and returns the ID in the response. |
| GET | api/v2/connections/{id}/editable-data-schema | read | connections | Gets a list of connection parameters that can be updated. |
| POST | api/v2/connections/{id}/make-locked | write | connections | Restricts the connection's visibility to its access list (visibility: locked). |
| POST | api/v2/connections/{id}/make-team | write | connections | Makes a locked connection visible to the whole team again (visibility: team) and clears the connection's. |
| POST | api/v2/connections/{id}/scoped | write | connections | Verifies if a scope for a given connection is set. |
| POST | api/v2/connections/{id}/set-data | write | connections | Updates the specified connection with data in the request body. |
| POST | api/v2/connections/{id}/test | write | connections | Verifies the connection status. |
| POST | api/v2/credential-requests/actions/create | write | credential-requests | Creates a new Action for a Credential Creation. |
| GET | api/v2/credential-requests/apps/{id}/{id}/modules-with-credentials | read | credential-requests | Retrieves all modules with credential requirements for a specific app and version. |
| POST | api/v2/credential-requests/credentials/{id}/decline | write | credential-requests | Declines a credential by setting its state to declined and recording the reason. |
| POST | api/v2/credential-requests/credentials/{id}/delete-remote | write | credential-requests | Deletes a credential from the remote platform (Make Web API) and resets its state to pending. |
| POST | api/v2/credential-requests/credentials/{id}/request-reauthorize | write | credential-requests | Tests the OAuth connection and transitions to reauthorizing state if invalid. |
| GET | api/v2/credential-requests/requests | read | credential-requests | Retrieves a list of Credential Requests. |
| POST | api/v2/credential-requests/requests | write | credential-requests | Creates a new request for Credentials. |
| POST | api/v2/credential-requests/requests/v2 | write | credential-requests | Creates a new request for Credentials using app and module selections. |
| GET | api/v2/credential-requests/requests/{id} | read | credential-requests | Retrieves a single Credential Request. |
| DELETE | api/v2/credential-requests/requests/{id} | write | credential-requests | Deletes the given Credential Request. |
| GET | api/v2/credential-requests/requests/{id}/detail | read | credential-requests | Retrieves detail of a single Credential Request with associated credentials. |
| GET | api/v2/custom-property-structures | read | custom-property-structures | Gets a list of custom properties structures in the organization. |
| POST | api/v2/custom-property-structures | write | custom-property-structures | Creates a custom properties structure. |
| PATCH | api/v2/custom-property-structures/custom-property-structure-items/{id} | write | custom-property-structures | Updates the specified item of a custom property structure. |
| DELETE | api/v2/custom-property-structures/custom-property-structure-items/{id} | write | custom-property-structures | Deletes the specified custom property structure item. |
| GET | api/v2/custom-property-structures/{id}/custom-property-structure-items | read | custom-property-structures | Gets the list of structure items in the specified custom properties structure. |
| POST | api/v2/custom-property-structures/{id}/custom-property-structure-items | write | custom-property-structures | Creates custom properties structure items. |
| GET | api/v2/data-stores | read | data-stores | Retrieves a collection of all data stores for a team with a given ID. |
| POST | api/v2/data-stores | write | data-stores | Creates a new data store with data passed in the request body. |
| DELETE | api/v2/data-stores | write | data-stores | Deletes data stores with given IDs and returns their IDs in the response. |
| GET | api/v2/data-stores/{id} | read | data-stores | Retrieves details of a data store with a given ID. |
| PATCH | api/v2/data-stores/{id} | write | data-stores | Updates properties of a data store with a given ID in a team with a given ID by passing new values in the request body. |
| GET | api/v2/data-stores/{id}/data | read | data-stores | Retrieves a collection of all records from a data store with a given ID. |
| POST | api/v2/data-stores/{id}/data | write | data-stores | Creates a new record in a data store with a given ID and returns all record details. |
| DELETE | api/v2/data-stores/{id}/data | write | data-stores | Deletes records from the specified data store. |
| PUT | api/v2/data-stores/{id}/data/{id} | write | data-stores | Updates a data store record with a given key by passing new data in the request body. |
| PATCH | api/v2/data-stores/{id}/data/{id} | write | data-stores | Updates a data store record with a given key by passing new data in the request body. |
| GET | api/v2/data-structures | read | data-structures | Retrieves a collection of all data structures for a team with a given ID. |
| POST | api/v2/data-structures | write | data-structures | Creates a new data structure with data passed in the request body. |
| GET | api/v2/data-structures/{id} | read | data-structures | Retrieves a data structure with a given ID. |
| PATCH | api/v2/data-structures/{id} | write | data-structures | Updates the specified data structure. |
| DELETE | api/v2/data-structures/{id} | write | data-structures | Deletes a data structure with a given ID and returns the ID in the response. |
| POST | api/v2/data-structures/{id}/clone | write | data-structures | Clones the specified data structure. |
| GET | api/v2/devices | read | devices | Get a list of devices of a given team. |
| POST | api/v2/devices/request | write | devices | Required scope: devices:write. |
| GET | api/v2/devices/{id} | read | devices | The ID can be id or udid. |
| PATCH | api/v2/devices/{id} | write | devices | Update a device. |
| DELETE | api/v2/devices/{id} | write | devices | Delete. |
| GET | api/v2/devices/{id}/incomings | read | devices | Required scope: devices:read. |
| DELETE | api/v2/devices/{id}/incomings | write | devices | "ids" and "all" can no be used together. |
| GET | api/v2/devices/{id}/incomings/stats | read | devices | Required scope: devices:read. |
| GET | api/v2/devices/{id}/incomings/{id} | read | devices | Required scope: devices:read. |
| GET | api/v2/devices/{id}/outgoings | read | devices | Required scope: devices:read. |
| DELETE | api/v2/devices/{id}/outgoings | write | devices | "ids" and "all" can no be used together. |
| GET | api/v2/devices/{id}/outgoings/{id} | read | devices | Required scope: devices:read. |
| GET | api/v2/dlqs | read | dlqs | Retrieves the list of incomplete executions of the specified scenario. |
| DELETE | api/v2/dlqs | write | dlqs | Deletes incomplete executions of the specified scenario. |
| POST | api/v2/dlqs/retry | write | dlqs | Triggers a retry of the specified incomplete executions. |
| GET | api/v2/dlqs/{id} | read | dlqs | Gets detail of the specified incomplete execution. |
| PATCH | api/v2/dlqs/{id} | write | dlqs | Updates the specified incomplete execution. |
| DELETE | api/v2/dlqs/{id} | write | dlqs | Required scope: datastores:write. |
| GET | api/v2/dlqs/{id}/blueprint | read | dlqs | Gets the blueprint of the scenario that caused the incomplete execution. |
| GET | api/v2/dlqs/{id}/bundle | read | dlqs | Gets bundles that caused the incomplete execution. |
| GET | api/v2/dlqs/{id}/logs | read | dlqs | Gets data about attempts to resolve an incomplete execution. |
| GET | api/v2/dlqs/{id}/logs/{id} | read | dlqs | Gets detail of the specified incomplete execution log. |
| POST | api/v2/dlqs/{id}/retry | write | dlqs | Triggers a retry of the specified incomplete execution. |
| GET | api/v2/enums/apps-review-statuses | read | enums | Gets the list of statuses that Make assigns to custom apps. |
| GET | api/v2/enums/countries | read | enums | Gets the list of countries and their countryId values in the id column. |
| GET | api/v2/enums/imt-regions | read | enums | Gets the list of Make regions and their regionId values in the id column. |
| GET | api/v2/enums/imt-zones | read | enums | Gets the list of Make zones and their zoneId values in the id column. |
| GET | api/v2/enums/languages | read | enums | Gets the list of languages and their language codes. |
| GET | api/v2/enums/locales | read | enums | Gets the list of locales and their localeId values and locale codes. |
| GET | api/v2/enums/module-types | read | enums | Gets the list of module types. |
| GET | api/v2/enums/organization-features | read | enums | Gets the list of all existing organization features and their descriptions. |
| GET | api/v2/enums/timezones | read | enums | Gets the list of timezones and their timezoneId values. |
| GET | api/v2/enums/us-states | read | enums | Gets the list of US states and their id values along with the two-letter state code. |
| GET | api/v2/enums/user-api-token-scopes | read | enums | Gets the list of all of the existing user API token scopes. |
| GET | api/v2/enums/user-email-notifications | read | enums | Gets the list of available email notification settings and their notificationId values. |
| GET | api/v2/enums/user-features | read | enums | Gets the list of all existing user features and their descriptions. |
| GET | api/v2/enums/variable-types | read | enums | Retrieves the mapping of custom variable types and their typeId values. |
| GET | api/v2/event-subscriptions/v1/organizations/{id}/event-types | read | event-subscriptions | Lists the event types a subscription can receive, with the JSON Schema of each payload version. |
| GET | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions | read | event-subscriptions | Lists the event subscriptions of the organization. |
| POST | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions | write | event-subscriptions | Creates an event subscription that sends the selected events to url. |
| GET | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id} | read | event-subscriptions | Gets an event subscription and its current status. |
| PATCH | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id} | write | event-subscriptions | Updates the fields in the request body and leaves the others unchanged. |
| DELETE | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id} | write | event-subscriptions | Deletes the event subscription. |
| GET | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/deliveries | read | event-subscriptions | Lists the deliveries of an event subscription, newest first by default. |
| GET | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/deliveries/{id} | read | event-subscriptions | Gets a delivery with the event that was sent and every attempt to send it. |
| POST | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/deliveries/{id}/resend | write | event-subscriptions | Sends the delivery's event to the endpoint again as a new, manual attempt. |
| POST | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/disable | write | event-subscriptions | Stops sending events to the subscription until it is enabled again. |
| POST | api/v2/event-subscriptions/v1/organizations/{id}/subscriptions/{id}/enable | write | event-subscriptions | Starts sending events to the subscription again, including one that is suspended after repeated failed deliveries. |
| GET | api/v2/functions | read | functions | Retrieves a list of custom functions available in the team. |
| POST | api/v2/functions | write | functions | Creates a custom function. |
| POST | api/v2/functions/eval | write | functions | Checks the custom functions code. |
| GET | api/v2/functions/{id} | read | functions | Gets detailed information about a custom function. |
| PATCH | api/v2/functions/{id} | write | functions | Updates custom functions description or code. |
| DELETE | api/v2/functions/{id} | write | functions | Deletes the custom function. |
| GET | api/v2/functions/{id}/history | read | functions | Gets history of updates of the specified custom function. |
| GET | api/v2/hooks | write | hooks | Retrieves a collection of all hooks for a team with a given ID. Kept out of read: it returns webhook URLs, which act as secrets that trigger scenarios. |
| POST | api/v2/hooks | write | hooks | Creates a new hook with data passed in the request body. |
| GET | api/v2/hooks/{id} | write | hooks | Retrieves details of a hook with a given ID including hooks data. Kept out of read: it returns the webhook URL, which acts as a secret that triggers the scenario. |
| PATCH | api/v2/hooks/{id} | write | hooks | Updates a hook with a given ID by passing new values in the request body. |
| DELETE | api/v2/hooks/{id} | write | hooks | Deletes a hook with a given ID and returns the ID in the response. |
| POST | api/v2/hooks/{id}/disable | write | hooks | Disables a hook with a given ID. |
| POST | api/v2/hooks/{id}/enable | write | hooks | Enables a disabled hook with a given ID. |
| GET | api/v2/hooks/{id}/incomings | read | hooks | Retrieves a list of webhook queue items waiting for processing with the specified webhook. |
| DELETE | api/v2/hooks/{id}/incomings | write | hooks | Deletes items from the processing queue of the specified webhook. |
| GET | api/v2/hooks/{id}/incomings/stats | read | hooks | Gets webhook processing queue stats. |
| GET | api/v2/hooks/{id}/incomings/{id} | read | hooks | Retrieves detail information about the specified webhook queue item. |
| POST | api/v2/hooks/{id}/learn-start | write | hooks | Starts the process of learning the request body structure by a hook with a given ID. |
| POST | api/v2/hooks/{id}/learn-stop | write | hooks | Stops the process of learning the request body structure by a hook with a given ID. |
| GET | api/v2/hooks/{id}/logs | read | hooks | Retrieves a list of the specified webhook execution logs. |
| GET | api/v2/hooks/{id}/logs/{id} | read | hooks | Retrieves the specified webhook execution log. |
| GET | api/v2/hooks/{id}/ping | write | hooks | Determines if a hook with a given ID is active and retrieves its properties that provide you with the address of the hook and inform if the hook is attached, what is. Kept out of read: it pings the webhook, which is an action rather than a read. |
| POST | api/v2/hooks/{id}/set-data | write | hooks | Sets data for a hook with a given ID. |
| GET | api/v2/keys | read | keys | Gets the list of keys in your custom keychain. |
| POST | api/v2/keys | write | keys | Creates a key in your keychain. |
| GET | api/v2/keys/types | read | keys | Gets the list of available key types. |
| GET | api/v2/keys/{id} | read | keys | Gets details of the specified key. |
| PATCH | api/v2/keys/{id} | write | keys | Updates a key name, connection parameters, or both with the data specified in the request body. |
| DELETE | api/v2/keys/{id} | write | keys | Deletes the specified key. |
| POST | api/v2/keys/{id}/make-locked | write | keys | Restricts the key's visibility to its access list (visibility: locked). |
| POST | api/v2/keys/{id}/make-team | write | keys | Makes a locked key visible to the whole team again (visibility: team) and clears the key's entire access. |
| GET | api/v2/notifications | read | notifications | Retrieves a collection of all notifications for the authenticated user. |
| DELETE | api/v2/notifications | write | notifications | Deletes notifications with given IDs and returns their IDs in the response. |
| POST | api/v2/notifications/mark-as-read | write | notifications | Marks all notifications as read and returns the IDs of the updated notifications in the response. |
| GET | api/v2/notifications/{id} | read | notifications | Retrieves details and full content of a notification with a given ID. |
| GET | api/v2/organizations | read | organizations | Retrieves a collection of all organizations, in which the user has membership. |
| POST | api/v2/organizations | write | organizations | Create a new organization using the data sent in the request body. |
| POST | api/v2/organizations/accept-invitation | write | organizations | Accept invitation. |
| GET | api/v2/organizations/invitation | read | organizations | Invitation detail. |
| GET | api/v2/organizations/{id} | read | organizations | Retrieves detail information of the organization with the specified organizationId. |
| PATCH | api/v2/organizations/{id} | write | organizations | Updates the organization data with the values in the request body. |
| DELETE | api/v2/organizations/{id} | write | organizations | Deletes the organization with the specified organizationId. |
| GET | api/v2/organizations/{id}/apps | read | organizations | Get list of custom apps associated with the users in the organization. |
| GET | api/v2/organizations/{id}/check-team-permission | read | organizations | Checks if the current user has a specific team (company) permission on any team within the specified organization. |
| GET | api/v2/organizations/{id}/feature-controls | read | organizations | Retrieves all feature controls for the specified organization. |
| PATCH | api/v2/organizations/{id}/feature-controls | write | organizations | Sets a feature control of the specified organization to the requested state. |
| GET | api/v2/organizations/{id}/hooks | write | organizations | Retrieves hooks from the teams of an organization, including private spaces. Kept out of read: it returns webhook URLs, which act as secrets that trigger scenarios. |
| POST | api/v2/organizations/{id}/invite | write | organizations | Invite a user to the organization. |
| GET | api/v2/organizations/{id}/managed-organizations | read | organizations | Retrieves the collection of child organizations. |
| POST | api/v2/organizations/{id}/managed-organizations | write | organizations | A successful response contains information about the new organization and user. |
| GET | api/v2/organizations/{id}/managed-organizations-consumption | read | organizations | Retrieves the collection of child organizations with consumption of opertaions/credits. |
| PATCH | api/v2/organizations/{id}/managed-organizations/{id} | write | organizations | A successful response contains summary of new operation limits for parent and child organization. |
| GET | api/v2/organizations/{id}/payments | read | organizations | Get list of past payments. |
| GET | api/v2/organizations/{id}/private-spaces-settings | read | organizations | Returns the private-spaces settings for the organization. |
| PATCH | api/v2/organizations/{id}/private-spaces-settings | write | organizations | Updates the organization's private-spaces settings. |
| POST | api/v2/organizations/{id}/scenarios/executions/io-data/counts | read | organizations | Counts how many scenarios and executions across the organization (or a specific team) produced module input/output (IO) data matching a free-text query. |
| POST | api/v2/organizations/{id}/scenarios/executions/io-data/search | read | organizations | Searches the module input/output (IO) data produced by scenario executions across the organization (or a specific team) using a free-text query. |
| POST | api/v2/organizations/{id}/scenarios/executions/search | read | organizations | Retrieves execution logs across all scenarios in an organization (or a specific team within the organization), narrowed by from/to, execution status, scenarioIds, or... |
| POST | api/v2/organizations/{id}/scenarios/{id}/executions/{id}/io-data/search | read | organizations | Searches the module input/output (IO) data produced by a single scenario execution using a free-text query, and returns every matching IO-data record for that... |
| GET | api/v2/organizations/{id}/sso-certificates | read | organizations | Get all SSO certificates. |
| GET | api/v2/organizations/{id}/subscription | read | organizations | Get detail of an active subscription. |
| POST | api/v2/organizations/{id}/subscription | write | organizations | Create a new subscription. |
| PATCH | api/v2/organizations/{id}/subscription | write | organizations | Change subscription. |
| DELETE | api/v2/organizations/{id}/subscription | write | organizations | Cancel the active subscription. |
| POST | api/v2/organizations/{id}/subscription-free | write | organizations | Sets Free plan subscription. |
| POST | api/v2/organizations/{id}/subscription/pause | write | organizations | Schedules a pause for the active monthly self-service subscription. |
| GET | api/v2/organizations/{id}/subscription/payment-method-types | read | organizations | Returns a list of available payment method types for the organization's subscription. |
| GET | api/v2/organizations/{id}/subscription/payment-methods | read | organizations | Returns a list of payment methods for the organization's subscription. |
| DELETE | api/v2/organizations/{id}/subscription/payment-methods/{id} | write | organizations | Deletes a payment method from the organization's subscription. |
| PATCH | api/v2/organizations/{id}/subscription/payment-methods/{id}/default | write | organizations | Sets a payment method as the default for the organization's subscription. |
| POST | api/v2/organizations/{id}/subscription/unpause | write | organizations | Ends the pause for the subscription. |
| PATCH | api/v2/organizations/{id}/tfa-enforcement | write | organizations | Enables or disables two-factor authentication (TFA) enforcement for the specified organization. |
| GET | api/v2/organizations/{id}/universal-discount | read | organizations | Returns the current universal discount (active or dormant) for the organization. |
| POST | api/v2/organizations/{id}/universal-discount/claim-cancellation-offer | write | organizations | Claims a cancellation offer discount for the organization. |
| POST | api/v2/organizations/{id}/universal-discount/redeem | write | organizations | Activates a dormant universal discount on the user's current subscription. |
| GET | api/v2/organizations/{id}/usage | read | organizations | Retrieves a list of daily centicredits, operations, and data transfer usage across all scenarios within all teams in the specified organization for the past 30 days. |
| GET | api/v2/organizations/{id}/user-organization-roles | read | organizations | Retrieves information about all users and their roles in the organization with the specified organizationId. |
| POST | api/v2/organizations/{id}/user-organization-roles/transfer | write | organizations | Transfer organization ownership to the specified user. |
| GET | api/v2/organizations/{id}/user-organization-roles/{id} | read | organizations | Retrieves information about a user role in an organization with the specified userId and organizationId. |
| GET | api/v2/organizations/{id}/variables | read | organizations | Retrieves the collection of organization variables. |
| POST | api/v2/organizations/{id}/variables | write | organizations | Creates new organization variable. |
| PATCH | api/v2/organizations/{id}/variables/{id} | write | organizations | Updates custom organization variable with the specified variable name. |
| DELETE | api/v2/organizations/{id}/variables/{id} | write | organizations | Deletes organization variable. |
| GET | api/v2/organizations/{id}/variables/{id}/history | read | organizations | Gets the history of updates of the specified custom variable. |
| GET | api/v2/ping | read | ping | Pings the Make API service. |
| GET | api/v2/private-spaces | read | private-spaces | Gets the list of private spaces in the organization with specified organizationId. |
| GET | api/v2/private-spaces/{id} | read | private-spaces | Returns the details of a single private space. |
| PATCH | api/v2/private-spaces/{id} | write | private-spaces | Updates a private space. |
| POST | api/v2/rpcs/{id}/{id}/{id} | write | rpcs | Call RPC. |
| GET | api/v2/scenario-labels | read | scenario-labels | Retrieves the colour-coded labels owned by a team, sorted by name (case-insensitive) ascending. |
| POST | api/v2/scenario-labels | write | scenario-labels | Creates a new team label. |
| POST | api/v2/scenario-labels/assign-scenarios | write | scenario-labels | Assigns every accepted team label to every accepted scenario in one transaction. |
| POST | api/v2/scenario-labels/unassign-scenarios | write | scenario-labels | Removes every accepted team label from every accepted scenario in one transaction. |
| PATCH | api/v2/scenario-labels/{id} | write | scenario-labels | Renames, re-colours, or re-describes a team label. |
| DELETE | api/v2/scenario-labels/{id} | write | scenario-labels | Deletes a team label. |
| POST | api/v2/scenario-labels/{id}/scenarios/{id} | write | scenario-labels | Assigns a team label to a single scenario. |
| DELETE | api/v2/scenario-labels/{id}/scenarios/{id} | write | scenario-labels | Removes a team label from a single scenario. |
| GET | api/v2/scenarios | read | scenarios | Retrieves a collection of all scenarios for a team or an organization with a given ID. |
| POST | api/v2/scenarios | write | scenarios | Creates a new scenario with data passed in the request body. |
| GET | api/v2/scenarios/ai-agents | read | scenarios | Retrieves scenarios that contain at least one AI agent module for the specified team. |
| POST | api/v2/scenarios/ai-agents/modules | read | scenarios | Retrieves local AI agent module and tool details for scenarios belonging to the specified team. |
| GET | api/v2/scenarios/consumptions | read | scenarios | Retrieves a list of scenarios and their current consumption. |
| POST | api/v2/scenarios/move-to-trash | write | scenarios | Moves up to 1,000 scenarios of one team to the trash in a single request. |
| PATCH | api/v2/scenarios/tools/{id} | write | scenarios | Updates a tool configuration with a given scenario ID by passing new values in the request body. |
| GET | api/v2/scenarios/trash/count | read | scenarios | Returns the number of scenarios currently in the trash for a team — scenarios that were. |
| GET | api/v2/scenarios/{id} | read | scenarios | Retrieves all available properties of a scenario with a given ID. |
| PATCH | api/v2/scenarios/{id} | write | scenarios | Updates a scenario with a given ID by passing new values in the request body. |
| DELETE | api/v2/scenarios/{id} | write | scenarios | Deletes a scenario with a given ID and returns the ID in the response. |
| GET | api/v2/scenarios/{id}/blueprint | read | scenarios | Retrieves a blueprint of a scenario with a given ID. |
| GET | api/v2/scenarios/{id}/blueprints | read | scenarios | Retrieves a collection of all blueprints versions for a scenario with a given ID. |
| GET | api/v2/scenarios/{id}/build-variables | read | scenarios | Retrieves buildtime variables of a scenario with the given ID. |
| POST | api/v2/scenarios/{id}/build-variables | write | scenarios | Adds new buildtime team or user defined variable/s. |
| PUT | api/v2/scenarios/{id}/build-variables | write | scenarios | Updates team or user defined buildtime variable/s. |
| DELETE | api/v2/scenarios/{id}/build-variables | write | scenarios | Deletes a buildtime variable with a given value for a scenario with a given ID and returns OK in the response. |
| POST | api/v2/scenarios/{id}/clone | write | scenarios | Clones the specified scenario. |
| GET | api/v2/scenarios/{id}/custom-properties | read | scenarios | Gets custom properties data of the specified scenario. |
| POST | api/v2/scenarios/{id}/custom-properties | write | scenarios | Fills in custom properties data for the specified scenario. |
| PUT | api/v2/scenarios/{id}/custom-properties | write | scenarios | Sets custom properties data for the specified scenario. |
| PATCH | api/v2/scenarios/{id}/custom-properties | write | scenarios | Updates custom properties data of the specified scenario. |
| DELETE | api/v2/scenarios/{id}/custom-properties | write | scenarios | Deletes custom properties data. |
| GET | api/v2/scenarios/{id}/data/{id} | write | scenarios | Verifies whether the module data is set or not. Kept out of read: it requires the scenarios:write scope. |
| GET | api/v2/scenarios/{id}/executions/{id} | read | scenarios | Retrieves details about an execution. |
| POST | api/v2/scenarios/{id}/executions/{id}/replay | write | scenarios | Replays one execution of the scenario. |
| POST | api/v2/scenarios/{id}/executions/{id}/stop | write | scenarios | Stops a running execution. |
| GET | api/v2/scenarios/{id}/interface | read | scenarios | Retrieves the scenario inputs and outputs specification for the specified scenario. |
| PATCH | api/v2/scenarios/{id}/interface | write | scenarios | Updates specification of the scenario inputs. |
| GET | api/v2/scenarios/{id}/logs | read | scenarios | Retrieves a collection of all logs for a scenario with a given ID. |
| GET | api/v2/scenarios/{id}/logs/{id} | read | scenarios | Retrieves an execution log with a given ID for a scenario with a given ID. |
| GET | api/v2/scenarios/{id}/modules/operations | read | scenarios | Retrieves an aggregated list of operations per module within a specified time period. |
| GET | api/v2/scenarios/{id}/modules/{id}/logs | read | scenarios | Retrieves an operation logs of a given module within a given scenario. |
| GET | api/v2/scenarios/{id}/notes | read | scenarios | Retrieves a collection of all scenario notes for a team and organization with a given ID. |
| POST | api/v2/scenarios/{id}/notes | write | scenarios | Creates a new scenario note with data passed in the request body. |
| GET | api/v2/scenarios/{id}/notes/{id} | read | scenarios | Retrieves all available properties of a scenario note with a given ID. |
| PATCH | api/v2/scenarios/{id}/notes/{id} | write | scenarios | Updates a scenario note with a given ID by passing new values in the request body. |
| DELETE | api/v2/scenarios/{id}/notes/{id} | write | scenarios | Deletes a scenario note with a given ID and returns the ID in the response. |
| POST | api/v2/scenarios/{id}/replay | write | scenarios | Replays the specified executions of the scenario. |
| POST | api/v2/scenarios/{id}/restore | write | scenarios | Restores a soft-deleted ("trashed") scenario with the given ID back to active, as long as it. |
| POST | api/v2/scenarios/{id}/run | write | scenarios | Runs the specified scenario. |
| POST | api/v2/scenarios/{id}/start | write | scenarios | Activates the specified scenario. |
| POST | api/v2/scenarios/{id}/stop | write | scenarios | Deactivates and stops the specified scenario if the scenario is running. |
| GET | api/v2/scenarios/{id}/triggers | read | scenarios | Retrieves properties of a trigger included in a scenario with a given ID. |
| GET | api/v2/scenarios/{id}/usage | read | scenarios | Retrieves a list of daily centicredits, operations, and data transfer usage for a specified scenario over the past 30 days. |
| GET | api/v2/scenarios-folders | read | scenarios-folders | Retrieves direct scenario folder children for a team or organization. |
| POST | api/v2/scenarios-folders | write | scenarios-folders | Creates a new scenario folder with data passed in the request body. |
| POST | api/v2/scenarios-folders/move-scenarios | write | scenarios-folders | Moves selected scenarios from the specified team into a target folder. |
| POST | api/v2/scenarios-folders/reorder | write | scenarios-folders | Sets manual positions for direct sibling folders within one parent. |
| PATCH | api/v2/scenarios-folders/{id} | write | scenarios-folders | Updates a scenario folder with a given ID by passing a new name, a new parent folder, or both in the request body. |
| DELETE | api/v2/scenarios-folders/{id} | write | scenarios-folders | Deletes a scenario folder with a given ID and returns the ID in the response. |
| GET | api/v2/scenarios-shared | read | scenarios-shared | Returns a paginated list of shared scenarios for a specified organization or team. |
| GET | api/v2/scenarios-shared/{id} | read | scenarios-shared | Returns all shares created for the specified scenario. |
| POST | api/v2/scenarios-shared/{id} | write | scenarios-shared | Creates a share of the specified scenario. |
| GET | api/v2/scenarios-shared/{id}/{id} | read | scenarios-shared | Get shared scenario detail by ID. |
| PATCH | api/v2/scenarios-shared/{id}/{id} | write | scenarios-shared | Updates a shared scenario by ID by passing new values in the request body. |
| DELETE | api/v2/scenarios-shared/{id}/{id} | write | scenarios-shared | Deletes a shared scenario and returns the ID in the response. |
| GET | api/v2/sdk/apps | read | sdk-apps | Retrieves a collection of all apps available to the authenticated user. |
| POST | api/v2/sdk/apps | write | sdk-apps | Creates a new app with data passed in the request body. |
| GET | api/v2/sdk/apps/connections/{id} | read | sdk-apps | Get Connection. |
| PATCH | api/v2/sdk/apps/connections/{id} | write | sdk-apps | Update Connection. |
| DELETE | api/v2/sdk/apps/connections/{id} | write | sdk-apps | Deletes a connection. |
| GET | api/v2/sdk/apps/connections/{id}/common | write | sdk-apps | Get Connection Common. Kept out of read: common data holds app credentials such as client secrets. |
| PUT | api/v2/sdk/apps/connections/{id}/common | write | sdk-apps | Set Connection Common. |
| POST | api/v2/sdk/apps/connections/{id}/recreate | write | sdk-apps | Recreates an existing app connection and synchronises it with HQ. |
| GET | api/v2/sdk/apps/connections/{id}/{id} | read | sdk-apps | Available sections: api, parameters, scopes, scope, install, installSpec. |
| PUT | api/v2/sdk/apps/connections/{id}/{id} | write | sdk-apps | Available sections: api, parameters, scopes, scope, installSpec, install. |
| GET | api/v2/sdk/apps/invites/{id} | read | sdk-apps | Get App Invite. |
| POST | api/v2/sdk/apps/invites/{id} | write | sdk-apps | Accept App Invite. |
| GET | api/v2/sdk/apps/webhooks/{id} | read | sdk-apps | Get Webhook. |
| PATCH | api/v2/sdk/apps/webhooks/{id} | write | sdk-apps | Update Webhook. |
| DELETE | api/v2/sdk/apps/webhooks/{id} | write | sdk-apps | Delete Webhook. |
| GET | api/v2/sdk/apps/webhooks/{id}/{id} | read | sdk-apps | Get Webhook Section. |
| PUT | api/v2/sdk/apps/webhooks/{id}/{id} | write | sdk-apps | Send the section with Content-Type: application/jsonc (recommended) to keep comments and formatting. |
| GET | api/v2/sdk/apps/{id}/connections | read | sdk-apps | List App Connections. |
| POST | api/v2/sdk/apps/{id}/connections | write | sdk-apps | Create Connection. |
| GET | api/v2/sdk/apps/{id}/webhooks | read | sdk-apps | List App Webhooks. |
| POST | api/v2/sdk/apps/{id}/webhooks | write | sdk-apps | Create Webhook. |
| GET | api/v2/sdk/apps/{id}/{id} | read | sdk-apps | Get App. |
| PATCH | api/v2/sdk/apps/{id}/{id} | write | sdk-apps | Patch App. |
| DELETE | api/v2/sdk/apps/{id}/{id} | write | sdk-apps | Delete App. |
| POST | api/v2/sdk/apps/{id}/{id}/base | write | sdk-apps | Set app base configuration. |
| PATCH | api/v2/sdk/apps/{id}/{id}/base | write | sdk-apps | Patch app base configuration. |
| GET | api/v2/sdk/apps/{id}/{id}/changes/{id} | read | sdk-apps | Get Change. |
| POST | api/v2/sdk/apps/{id}/{id}/clone | write | sdk-apps | Clone App. |
| POST | api/v2/sdk/apps/{id}/{id}/clone-major | write | sdk-apps | Clones the app to the next major version with the same app name. |
| POST | api/v2/sdk/apps/{id}/{id}/closedsource | write | sdk-apps | Set App ClosedSource. |
| POST | api/v2/sdk/apps/{id}/{id}/commit | write | sdk-apps | Commit Changes. |
| GET | api/v2/sdk/apps/{id}/{id}/common | write | sdk-apps | Get app client id and client secret. Kept out of read: common data holds app credentials such as client secrets. |
| PUT | api/v2/sdk/apps/{id}/{id}/common | write | sdk-apps | Sets the common data for the app based on the parameters passed in the request body. |
| GET | api/v2/sdk/apps/{id}/{id}/events-log | read | sdk-apps | Get App Events Log. |
| GET | api/v2/sdk/apps/{id}/{id}/functions | read | sdk-apps | List App Functions. |
| POST | api/v2/sdk/apps/{id}/{id}/functions | write | sdk-apps | Create Function. |
| GET | api/v2/sdk/apps/{id}/{id}/functions/{id} | read | sdk-apps | Get Function. |
| DELETE | api/v2/sdk/apps/{id}/{id}/functions/{id} | write | sdk-apps | Delete Function. |
| GET | api/v2/sdk/apps/{id}/{id}/functions/{id}/code | read | sdk-apps | Get Function Code. |
| PUT | api/v2/sdk/apps/{id}/{id}/functions/{id}/code | write | sdk-apps | Set Function Code. |
| GET | api/v2/sdk/apps/{id}/{id}/functions/{id}/test | read | sdk-apps | Get Function Test. |
| PUT | api/v2/sdk/apps/{id}/{id}/functions/{id}/test | write | sdk-apps | Set Function Test. |
| PUT | api/v2/sdk/apps/{id}/{id}/groups | write | sdk-apps | Available sections: base, groups, install, installSpec. |
| PUT | api/v2/sdk/apps/{id}/{id}/icon | write | sdk-apps | Set App Logo. |
| GET | api/v2/sdk/apps/{id}/{id}/icon/{id} | read | sdk-apps | Get App Logo. |
| PUT | api/v2/sdk/apps/{id}/{id}/install | write | sdk-apps | Available sections: base, groups, install, installSpec. |
| GET | api/v2/sdk/apps/{id}/{id}/modules | read | sdk-apps | List App Modules. |
| POST | api/v2/sdk/apps/{id}/{id}/modules | write | sdk-apps | Create Module. |
| GET | api/v2/sdk/apps/{id}/{id}/modules/{id} | read | sdk-apps | Get Module. |
| PATCH | api/v2/sdk/apps/{id}/{id}/modules/{id} | write | sdk-apps | Updates a module. |
| DELETE | api/v2/sdk/apps/{id}/{id}/modules/{id} | write | sdk-apps | Delete Module. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/api | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| POST | api/v2/sdk/apps/{id}/{id}/modules/{id}/clone | write | sdk-apps | Creates a duplicate of a module. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/epoch | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/interface | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/parameters | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/samples | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/scope | write | sdk-apps | Available sections: api, epoch, parameters, expect, interface, samples, scope. |
| GET | api/v2/sdk/apps/{id}/{id}/modules/{id}/{id} | read | sdk-apps | Get Module Section. |
| POST | api/v2/sdk/apps/{id}/{id}/modules/{id}/{id} | write | sdk-apps | Set Module Deprecation. |
| PUT | api/v2/sdk/apps/{id}/{id}/modules/{id}/{id} | write | sdk-apps | Set Module Consumable. |
| POST | api/v2/sdk/apps/{id}/{id}/opensource | write | sdk-apps | Beta, stable. |
| GET | api/v2/sdk/apps/{id}/{id}/readme | read | sdk-apps | Get App Docs. |
| PUT | api/v2/sdk/apps/{id}/{id}/readme | write | sdk-apps | Set App Docs. |
| GET | api/v2/sdk/apps/{id}/{id}/review | read | sdk-apps | Get App Review. |
| POST | api/v2/sdk/apps/{id}/{id}/review | write | sdk-apps | Request Review. |
| PUT | api/v2/sdk/apps/{id}/{id}/review/form | write | sdk-apps | Submit App Review Form. |
| POST | api/v2/sdk/apps/{id}/{id}/rollback | write | sdk-apps | Rollback Changes. |
| GET | api/v2/sdk/apps/{id}/{id}/rpcs | read | sdk-apps | List App RPCs. |
| POST | api/v2/sdk/apps/{id}/{id}/rpcs | write | sdk-apps | Create RPC. |
| GET | api/v2/sdk/apps/{id}/{id}/rpcs/{id} | read | sdk-apps | Get RPC. |
| POST | api/v2/sdk/apps/{id}/{id}/rpcs/{id} | write | sdk-apps | Tests the RPC. |
| PATCH | api/v2/sdk/apps/{id}/{id}/rpcs/{id} | write | sdk-apps | Patch RPC. |
| DELETE | api/v2/sdk/apps/{id}/{id}/rpcs/{id} | write | sdk-apps | Delete RPC. |
| GET | api/v2/sdk/apps/{id}/{id}/rpcs/{id}/{id} | read | sdk-apps | Get RPC Section. |
| PUT | api/v2/sdk/apps/{id}/{id}/rpcs/{id}/{id} | write | sdk-apps | Available sections: api, parameters. |
| POST | api/v2/sdk/apps/{id}/{id}/uninstall | write | sdk-apps | Uninstall App from Organization. |
| POST | api/v2/sdk/apps/{id}/{id}/{id} | write | sdk-apps | Set App Visibility. |
| GET | api/v2/teams | read | teams | Gets the list of teams in the organization with specified organizationId. |
| POST | api/v2/teams | write | teams | Create a new team in the organization with the specified organizationId. |
| GET | api/v2/teams/{id} | read | teams | Returns information about the team with the specified teamId. |
| PATCH | api/v2/teams/{id} | write | teams | Updates information about the team with the specified teamId. |
| DELETE | api/v2/teams/{id} | write | teams | Deletes the team with the specified teamId. |
| GET | api/v2/teams/{id}/connections/{id}/access-list | read | teams | Returns the access list (entity ACL) of a connection — the principals granted a role on it. |
| POST | api/v2/teams/{id}/connections/{id}/access-list/users | write | teams | Adds a user to a connection's access list (entity ACL) with a role. |
| PATCH | api/v2/teams/{id}/connections/{id}/access-list/users/{id} | write | teams | Changes the entity-tier role of a user already on a connection's access list. |
| DELETE | api/v2/teams/{id}/connections/{id}/access-list/users/{id} | write | teams | Removes a user from a connection's access list. |
| GET | api/v2/teams/{id}/feature-controls | read | teams | Retrieves all feature controls for the specified organization which the team belongs to. |
| GET | api/v2/teams/{id}/keys/{id}/access-list | read | teams | Returns the access list (entity ACL) of a key — the principals granted a role on it. |
| POST | api/v2/teams/{id}/keys/{id}/access-list/users | write | teams | Adds a user to a key's access list (entity ACL) with a role. |
| PATCH | api/v2/teams/{id}/keys/{id}/access-list/users/{id} | write | teams | Changes the entity-tier role of a user already on a key's access list. |
| DELETE | api/v2/teams/{id}/keys/{id}/access-list/users/{id} | write | teams | Removes a user from a key's access list. |
| GET | api/v2/teams/{id}/usage | read | teams | Retrieves a list of daily centicredits, operations, and data transfer usage for all scenarios within a specified team over the past 30 days. |
| GET | api/v2/teams/{id}/user-team-roles | read | teams | Gets list of all users and their roles in the team with the specified teamId. |
| GET | api/v2/teams/{id}/user-team-roles/{id} | read | teams | Retrieves information about user role in a team with the specified userId and teamId. |
| GET | api/v2/teams/{id}/variables | read | teams | Retrieves the collection of team variables. |
| POST | api/v2/teams/{id}/variables | write | teams | Creates new team variable. |
| PATCH | api/v2/teams/{id}/variables/{id} | write | teams | Updates custom team variable with the specified variable name. |
| DELETE | api/v2/teams/{id}/variables/{id} | write | teams | Deletes team variable. |
| GET | api/v2/teams/{id}/variables/{id}/history | read | teams | Gets the history of updates of the specified custom variable. |
| GET | api/v2/templates | read | templates | Retrieves a collection of all templates for a team with a given ID. |
| POST | api/v2/templates | write | templates | Creates a new template with data passed in the request body. |
| GET | api/v2/templates/public | read | templates | Retrieves a collection of all public (approved) templates that are available for anyone. |
| GET | api/v2/templates/public/{id} | read | templates | Retrieves details of a public (approved) template with a given publicUrl. |
| GET | api/v2/templates/public/{id}/blueprint | read | templates | Retrieves a blueprint of a public (approved) template with a given publicUrl. |
| GET | api/v2/templates/{id} | read | templates | Retrieves details of a template with a given ID. |
| PATCH | api/v2/templates/{id} | write | templates | Updates a template with a given ID by passing new values in the request body. |
| DELETE | api/v2/templates/{id} | write | templates | Deletes a template with a given ID and returns the ID in the response. |
| GET | api/v2/templates/{id}/blueprint | read | templates | Retrieves a blueprint of a template with a given ID. |
| POST | api/v2/templates/{id}/publish | write | templates | Publishes a private template with a given ID. |
| POST | api/v2/templates/{id}/request-approval | write | templates | Requests approval of the published template with the given IDs of its private and published versions. |
| PATCH | api/v2/mailhub/users/{id}/organizations/{id}/teams/{id}/native-preferences | write | users | Updates a native email notification preference of a team for the user associated with the API key used for authentication. |
| GET | api/v2/mailhub/users/{id}/organizations/{id}/teams/{id}/preferences | read | users | Get team preferences. |
| PATCH | api/v2/mailhub/users/{id}/organizations/{id}/teams/{id}/preferences | write | users | Update team preferences. |
| GET | api/v2/mailhub/users/{id}/preferences | read | users | Get preferences. |
| PATCH | api/v2/mailhub/users/{id}/preferences | write | users | Update global preferences. |
| GET | api/v2/users | read | users | Retrieves a collection of all users for a team or an organization with a given ID. |
| DELETE | api/v2/users | write | users | Deletes the authenticated user's own account. |
| GET | api/v2/users/by-permission | read | users | Returns users who have a specific permission within an organization or team. |
| POST | api/v2/users/custom-roles | write | users | Creates a new custom organization or team role. |
| PATCH | api/v2/users/custom-roles/{id} | write | users | Updates the name, description, or permissions of an existing custom role. |
| DELETE | api/v2/users/custom-roles/{id} | write | users | Deletes an existing custom role. |
| GET | api/v2/users/me | read | users | Retrieves data about the authenticated user. |
| GET | api/v2/users/me/api-tokens | write | users | Gets the API tokens of the currently authenticated user, newest first. Kept out of read: returns the API token values. |
| POST | api/v2/users/me/api-tokens | write | users | Create a new API token for the currently authenticated user. |
| PATCH | api/v2/users/me/api-tokens/{id} | write | users | Replaces the scopes of the currently authenticated user's API token with the specified creation timestamp. |
| DELETE | api/v2/users/me/api-tokens/{id} | write | users | Deletes currently authenticated user's API token with the specified creation timestamp. |
| GET | api/v2/users/me/current-authorization | read | users | Returns current authorization information for the authenticated user including scope, authentication method used and the organization the authorization is bound to. |
| GET | api/v2/users/me/oauth-connections | read | users | Gets the OAuth connections for the currently authenticated user. |
| DELETE | api/v2/users/me/oauth-connections/{id} | write | users | Delete a specific OAuth connection for the currently authenticated user. |
| GET | api/v2/users/me/onboarding-survey | read | users | Returns whether the authenticated user has a pending onboarding survey. |
| POST | api/v2/users/me/onboarding-survey | write | users | Submits the onboarding survey response for the authenticated user. |
| GET | api/v2/users/me/organization-invitations | read | users | Retrieves organization invitations of the currently authenticated user. |
| GET | api/v2/users/password-reset | write | users | Checks a hash and sets a session for the Reset lost password endpoint. Kept out of read: it sets a password-reset session. |
| POST | api/v2/users/password-reset | write | users | Updates a password for a user based on the session created when calling the Prepare session for password reset endpoint. |
| POST | api/v2/users/password-reset-demand | write | users | Sends password reset demand for a user with an email passed in the request body. |
| GET | api/v2/users/roles | read | users | Gets list of all existing user role names and IDs. |
| GET | api/v2/users/roles/permissions | read | users | Gets a list of all available permissions that can be assigned to user roles. |
| GET | api/v2/users/roles/{id} | read | users | Returns the detail of a single role by its ID. |
| GET | api/v2/users/unread-notifications | read | users | Gets the number of unread notifications for the currently authenticated user. |
| GET | api/v2/users/user-team-notifications/{id} | read | users | Gets the authenticated user's notification settings for a team specified by the teamId. |
| GET | api/v2/users/user-team-notifications/{id}/{id} | read | users | Checks the authenticated user's notification settings for the team and notification type specified by the teamId and notificationId. |
| PUT | api/v2/users/user-team-notifications/{id}/{id} | write | users | Updates the authenticated user's notification settings for the team and notification type specified by the teamId and notificationId. |
| PATCH | api/v2/users/{id} | write | users | Updates a user with a given ID by passing new data in the request body. |
| PUT | api/v2/users/{id}/attributes/email | write | users | Updates an email for a user with a given ID by passing new data in the request body. |
| PUT | api/v2/users/{id}/attributes/password | write | users | Updates a password for a user with a given ID by passing new data in the request body. |
| GET | api/v2/users/{id}/user-organization-roles | read | users | Gets list of all users and their roles in the organization with the specified organizationId. |
| GET | api/v2/users/{id}/user-organization-roles/{id} | read | users | Gets information about user role in an organization with the specified userId and organizationId. |
| POST | api/v2/users/{id}/user-organization-roles/{id} | write | users | Updates the specified user role in the organization. |
| POST | api/v2/users/{id}/user-organization-roles/{id}/transfer | write | users | Transfer organization ownership to the user with the specified userId. |
| GET | api/v2/users/{id}/user-team-roles | read | users | Gets team roles of the user with the specified userId. |
| GET | api/v2/users/{id}/user-team-roles/{id} | read | users | Gets user role detail in the team with the specified teamId. |
| POST | api/v2/users/{id}/user-team-roles/{id} | write | users | Updates the user role in the team with the specified teamId. |
