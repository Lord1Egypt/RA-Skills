# Mailgun access policy

An access policy limits which endpoints Mailgun connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/mailgun#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Mailgun: its 104 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create mailgun --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v5/accounts/limit/custom/monthly"},
    {"method": "GET", "path": "v5/accounts/subaccounts"},
    {"method": "GET", "path": "v5/accounts/subaccounts/ip_pools/all"},
    {"method": "GET", "path": "v5/accounts/subaccounts/{id}"},
    {"method": "GET", "path": "v5/accounts/subaccounts/{id}/limit/custom/monthly"},
    {"method": "GET", "path": "v1/alerts/events"},
    {"method": "GET", "path": "v1/alerts/slack/channels"},
    {"method": "GET", "path": "v1/alerts/slack/channels/{id}"},
    {"method": "GET", "path": "v3/{id}/whitelists"},
    {"method": "GET", "path": "v3/{id}/whitelists/{id}"},
    {"method": "POST", "path": "v1/analytics/logs"},
    {"method": "POST", "path": "v1/analytics/metrics"},
    {"method": "POST", "path": "v1/analytics/tags"},
    {"method": "GET", "path": "v1/analytics/tags/limits"},
    {"method": "POST", "path": "v1/analytics/usage/metrics"},
    {"method": "POST", "path": "v2/bounce-classification/metrics"},
    {"method": "GET", "path": "v3/{id}/bounces"},
    {"method": "GET", "path": "v3/{id}/bounces/{id}"},
    {"method": "GET", "path": "v3/{id}/complaints"},
    {"method": "GET", "path": "v3/{id}/complaints/{id}"},
    {"method": "GET", "path": "v1/dkim/keys"},
    {"method": "GET", "path": "v3/domains"},
    {"method": "GET", "path": "v3/domains/{id}"},
    {"method": "GET", "path": "v3/domains/{id}/credentials"},
    {"method": "GET", "path": "v3/domains/{id}/limits/tag"},
    {"method": "GET", "path": "v3/domains/{id}/messages/{id}"},
    {"method": "GET", "path": "v3/domains/{id}/sending_queues"},
    {"method": "GET", "path": "v3/domains/{id}/tag/countries"},
    {"method": "GET", "path": "v3/domains/{id}/tag/devices"},
    {"method": "GET", "path": "v3/domains/{id}/tag/providers"},
    {"method": "GET", "path": "v3/domains/{id}/tracking"},
    {"method": "GET", "path": "v3/domains/{id}/webhooks"},
    {"method": "GET", "path": "v3/domains/{id}/webhooks/{id}"},
    {"method": "GET", "path": "v4/domains"},
    {"method": "GET", "path": "v4/domains/{id}"},
    {"method": "GET", "path": "v4/domains/{id}/keys"},
    {"method": "GET", "path": "v3/{id}/events"},
    {"method": "GET", "path": "v3/forwards"},
    {"method": "GET", "path": "v3/forwards/{id}"},
    {"method": "GET", "path": "v2/ip_whitelist"},
    {"method": "GET", "path": "v1/dynamic_pools/domains"},
    {"method": "GET", "path": "v1/dynamic_pools/domains/{id}/history"},
    {"method": "GET", "path": "v1/dynamic_pools/domains/{id}/preview"},
    {"method": "GET", "path": "v1/dynamic_pools/history"},
    {"method": "GET", "path": "v3/domains/dynamic_pools/assignable"},
    {"method": "GET", "path": "v3/dynamic_pools"},
    {"method": "GET", "path": "v3/ip_pools"},
    {"method": "GET", "path": "v3/ip_pools/{id}"},
    {"method": "GET", "path": "v3/ip_pools/{id}/domains"},
    {"method": "GET", "path": "v3/ip_warmups"},
    {"method": "GET", "path": "v3/ip_warmups/{id}"},
    {"method": "GET", "path": "v3/ips"},
    {"method": "GET", "path": "v3/ips/account/settings"},
    {"method": "GET", "path": "v3/ips/details/all"},
    {"method": "GET", "path": "v3/ips/domain/{id}"},
    {"method": "GET", "path": "v3/ips/request/new"},
    {"method": "GET", "path": "v3/ips/{id}"},
    {"method": "GET", "path": "v3/ips/{id}/domains"},
    {"method": "GET", "path": "v1/keys"},
    {"method": "GET", "path": "v3/lists"},
    {"method": "GET", "path": "v3/lists/pages"},
    {"method": "GET", "path": "v3/lists/{id}"},
    {"method": "GET", "path": "v3/lists/{id}/members"},
    {"method": "GET", "path": "v3/lists/{id}/members/pages"},
    {"method": "GET", "path": "v3/lists/{id}/members/{id}"},
    {"method": "GET", "path": "v3/routes"},
    {"method": "GET", "path": "v3/routes/match"},
    {"method": "GET", "path": "v3/routes/{id}"},
    {"method": "GET", "path": "v5/sandbox/auth_recipients"},
    {"method": "GET", "path": "v3/stats/filter"},
    {"method": "GET", "path": "v3/stats/total"},
    {"method": "GET", "path": "v3/stats/total/domains"},
    {"method": "GET", "path": "v3/{id}/aggregates/countries"},
    {"method": "GET", "path": "v3/{id}/aggregates/devices"},
    {"method": "GET", "path": "v3/{id}/aggregates/providers"},
    {"method": "GET", "path": "v3/{id}/stats/total"},
    {"method": "GET", "path": "v3/{id}/tag"},
    {"method": "GET", "path": "v3/{id}/tag/stats"},
    {"method": "GET", "path": "v3/{id}/tag/stats/aggregates"},
    {"method": "GET", "path": "v3/{id}/tags"},
    {"method": "GET", "path": "v3/{id}/templates"},
    {"method": "GET", "path": "v3/{id}/templates/{id}"},
    {"method": "GET", "path": "v3/{id}/templates/{id}/versions"},
    {"method": "GET", "path": "v3/{id}/templates/{id}/versions/{id}"},
    {"method": "GET", "path": "v4/templates"},
    {"method": "GET", "path": "v4/templates/{id}"},
    {"method": "GET", "path": "v4/templates/{id}/versions"},
    {"method": "GET", "path": "v4/templates/{id}/versions/{id}"},
    {"method": "GET", "path": "v1/thresholds/alerts/send"},
    {"method": "GET", "path": "v1/thresholds/alerts/send/{id}"},
    {"method": "GET", "path": "v1/thresholds/hits"},
    {"method": "GET", "path": "v1/thresholds/limits"},
    {"method": "GET", "path": "v1/thresholds/limits/{id}"},
    {"method": "GET", "path": "v2/thresholds/limits"},
    {"method": "GET", "path": "v2/thresholds/limits-primary"},
    {"method": "GET", "path": "v2/thresholds/limits/{id}"},
    {"method": "GET", "path": "v2/x509/{id}/status"},
    {"method": "GET", "path": "v3/{id}/unsubscribes"},
    {"method": "GET", "path": "v3/{id}/unsubscribes/{id}"},
    {"method": "GET", "path": "v5/users"},
    {"method": "GET", "path": "v5/users/me"},
    {"method": "GET", "path": "v5/users/{id}"},
    {"method": "GET", "path": "v1/webhooks"},
    {"method": "GET", "path": "v1/webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Mailgun endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| PUT | v5/accounts | write | accounts | Update variable account settings. |
| PUT | v5/accounts/features | write | accounts | Update account feature. |
| GET | v5/accounts/http_signing_key | write | accounts | Get webhook signing key saved on the account. Kept out of read: response is the account webhook signing key. |
| POST | v5/accounts/http_signing_key | write | accounts | Create or regenerate webhook signing key on an account. |
| PUT | v5/accounts/limit/custom/enable | write | accounts | Re-enable account disabled for hitting send limit. |
| GET | v5/accounts/limit/custom/monthly | read | accounts | Get current custom sending limit. |
| PUT | v5/accounts/limit/custom/monthly | write | accounts | Set a custom sending limit. |
| DELETE | v5/accounts/limit/custom/monthly | write | accounts | Delete a custom sending limit. |
| POST | v5/accounts/resend_activation_email | write | accounts | Resend account activation email to the account owner. |
| GET | v5/accounts/subaccounts | read | accounts | List all subaccounts. |
| POST | v5/accounts/subaccounts | write | accounts | Create a subaccount. |
| DELETE | v5/accounts/subaccounts | write | accounts | Delete a subaccount. |
| GET | v5/accounts/subaccounts/ip_pools/all | read | accounts | List DIPPs delegated to subaccounts. |
| GET | v5/accounts/subaccounts/{id} | read | accounts | Get a single subaccount. |
| POST | v5/accounts/subaccounts/{id}/disable | write | accounts | Disable a subaccount. |
| POST | v5/accounts/subaccounts/{id}/enable | write | accounts | Enable a subaccount. |
| PUT | v5/accounts/subaccounts/{id}/features | write | accounts | Update subaccount feature. |
| PUT | v5/accounts/subaccounts/{id}/ip_pool | write | accounts | Delegate a DIPP to a subaccount. |
| DELETE | v5/accounts/subaccounts/{id}/ip_pool | write | accounts | Revoke a DIPP delegated to a subaccount. |
| GET | v5/accounts/subaccounts/{id}/limit/custom/monthly | read | accounts | Get current custom sending limit. |
| PUT | v5/accounts/subaccounts/{id}/limit/custom/monthly | write | accounts | Set a custom sending limit. |
| DELETE | v5/accounts/subaccounts/{id}/limit/custom/monthly | write | accounts | Delete a custom sending limit. |
| POST | v1/alerts/email/test | write | alerts | Test message. |
| GET | v1/alerts/events | read | alerts | List events. |
| GET | v1/alerts/settings | write | alerts | List Alerts. Kept out of read: response includes the webhook signing key and Slack token. |
| POST | v1/alerts/settings/events | write | alerts | Add Alert. |
| PUT | v1/alerts/settings/events/{id} | write | alerts | Update Alert. |
| DELETE | v1/alerts/settings/events/{id} | write | alerts | Remove Alert. |
| PUT | v1/alerts/settings/slack | write | alerts | Update Slack settings. |
| DELETE | v1/alerts/settings/slack | write | alerts | Delete Slack settings. |
| PUT | v1/alerts/settings/webhooks/signing_key | write | alerts | Reset Webhook Signing Key. |
| GET | v1/alerts/slack/channels | read | alerts | List Slack channels. |
| GET | v1/alerts/slack/channels/{id} | read | alerts | Get Slack channel. |
| DELETE | v1/alerts/slack/oauth | write | alerts | Revoke Slack access token. |
| POST | v1/alerts/slack/test | write | alerts | Test message. |
| POST | v1/alerts/webhooks/test | write | alerts | Test webhook. |
| GET | v3/{id}/whitelists | read | allowlist | List allowlist records for domain. |
| POST | v3/{id}/whitelists | write | allowlist | Add allowlist record. |
| DELETE | v3/{id}/whitelists | write | allowlist | Clear allowlist. |
| POST | v3/{id}/whitelists/import | write | allowlist | Import allowlist. |
| GET | v3/{id}/whitelists/{id} | read | allowlist | Lookup allowlist record. |
| DELETE | v3/{id}/whitelists/{id} | write | allowlist | Remove entry from allowlist. |
| POST | v1/analytics/logs | read | analytics | List logs. |
| POST | v1/analytics/metrics | read | analytics | Query account metrics. |
| POST | v1/analytics/tags | read | analytics | Post query to list account tags or search for single tag. |
| PUT | v1/analytics/tags | write | analytics | Update account tag. |
| DELETE | v1/analytics/tags | write | analytics | Delete account tag. |
| GET | v1/analytics/tags/limits | read | analytics | Get account tag limit information. |
| POST | v1/analytics/usage/metrics | read | analytics | Query account usage metrics. |
| POST | v2/bounce-classification/metrics | read | analytics | List statistic v2. |
| GET | v3/{id}/bounces | read | bounces | List all bounces. |
| POST | v3/{id}/bounces | write | bounces | Add bounces. |
| DELETE | v3/{id}/bounces | write | bounces | Clear all bounces. |
| POST | v3/{id}/bounces/import | write | bounces | Import list of bounces. |
| GET | v3/{id}/bounces/{id} | read | bounces | Lookup bounce record. |
| DELETE | v3/{id}/bounces/{id} | write | bounces | Remove bounce. |
| GET | v3/{id}/complaints | read | complaints | List all complaints. |
| POST | v3/{id}/complaints | write | complaints | Add complaints. |
| DELETE | v3/{id}/complaints | write | complaints | Clear all complaints. |
| POST | v3/{id}/complaints/import | write | complaints | Import complaint list. |
| GET | v3/{id}/complaints/{id} | read | complaints | Lookup complaint record. |
| DELETE | v3/{id}/complaints/{id} | write | complaints | Remove complaint. |
| GET | v1/dkim/keys | read | dkim | List keys for all domains. |
| POST | v1/dkim/keys | write | dkim | Create a domain key. |
| DELETE | v1/dkim/keys | write | dkim | Delete a domain key. |
| POST | v1/dkim_management/domains/{id}/rotate | write | dkim | Rotate Automatic Sender Security DKIM key for a domain. |
| PUT | v1/dkim_management/domains/{id}/rotation | write | dkim | Update Automatic Sender Security DKIM key rotation for a domain. |
| GET | v3/domains | read | domains | Get a list of domains. |
| GET | v3/domains/{id} | read | domains | Get details of a domain. |
| DELETE | v3/domains/{id} | write | domains | Delete a domain. |
| GET | v3/domains/{id}/credentials | read | domains | List Mailgun SMTP credential metadata for a given domain. |
| POST | v3/domains/{id}/credentials | write | domains | Create Mailgun SMTP credentials for a given domain. |
| DELETE | v3/domains/{id}/credentials | write | domains | Delete all Mailgun SMTP credentials for a domain. |
| PUT | v3/domains/{id}/credentials/{id} | write | domains | Update Mailgun SMTP credentials. |
| DELETE | v3/domains/{id}/credentials/{id} | write | domains | Delete Mailgun SMTP credentials. |
| PUT | v3/domains/{id}/dkim_authority | write | domains | Update DKIM authority. |
| PUT | v3/domains/{id}/dkim_selector | write | domains | Update a DKIM selector. |
| POST | v3/domains/{id}/dynamic_pools | write | domains | Enroll domain. |
| DELETE | v3/domains/{id}/dynamic_pools | write | domains | Remove domain from dynamic IP pools. |
| DELETE | v3/domains/{id}/ips/{id} | write | domains | Remove an IP from the domain pool, unlink a DIPP or remove the domain pool. |
| GET | v3/domains/{id}/limits/tag | read | domains | Get tag limits. |
| GET | v3/domains/{id}/messages/{id} | read | domains | Retrieve a stored email. |
| POST | v3/domains/{id}/messages/{id} | write | domains | Resend an email. |
| DELETE | v3/domains/{id}/pool/{id} | write | domains | Remove an IP from the domain pool, unlink a DIPP or remove the domain pool. |
| GET | v3/domains/{id}/sending_queues | read | domains | Get messages queue status. |
| GET | v3/domains/{id}/tag/countries | read | domains | List of supported country codes. |
| GET | v3/domains/{id}/tag/devices | read | domains | List of supported devices. |
| GET | v3/domains/{id}/tag/providers | read | domains | List of supported providers. |
| GET | v3/domains/{id}/tracking | read | domains | Get tracking settings. |
| PUT | v3/domains/{id}/tracking/click | write | domains | Update click tracking settings. |
| PUT | v3/domains/{id}/tracking/open | write | domains | Update open tracking settings. |
| PUT | v3/domains/{id}/tracking/unsubscribe | write | domains | Update unsubscribe tracking settings. |
| GET | v3/domains/{id}/webhooks | read | domains | Get domain webhooks. |
| POST | v3/domains/{id}/webhooks | write | domains | Create a domain webhook. |
| GET | v3/domains/{id}/webhooks/{id} | read | domains | Get domain webhooks by type. |
| PUT | v3/domains/{id}/webhooks/{id} | write | domains | Update domain webhook. |
| DELETE | v3/domains/{id}/webhooks/{id} | write | domains | Delete domain webhooks by type. |
| GET | v4/domains | read | domains | Get domains. |
| POST | v4/domains | write | domains | Create a domain. |
| GET | v4/domains/{id} | read | domains | Get domain details. |
| PUT | v4/domains/{id} | write | domains | Update domain. |
| GET | v4/domains/{id}/keys | read | domains | List domain keys. |
| PUT | v4/domains/{id}/keys/{id}/activate | write | domains | Activate a domain key. |
| PUT | v4/domains/{id}/keys/{id}/deactivate | write | domains | Deactivate a domain key. |
| PUT | v4/domains/{id}/verify | write | domains | Verify Domain. |
| POST | v4/domains/{id}/webhooks | write | domains | Create domain webhooks (v4). |
| PUT | v4/domains/{id}/webhooks | write | domains | Update domain webhooks (v4). |
| DELETE | v4/domains/{id}/webhooks | write | domains | Delete domain webhooks (v4). |
| DELETE | v3/{id}/envelopes | write | envelopes | Delete scheduled and undelivered mail. |
| GET | v3/{id}/events | read | events | Retrieves a paginated list of events. |
| GET | v3/forwards | read | forwards | List forward rules. |
| POST | v3/forwards | write | forwards | Create a forward rule. |
| GET | v3/forwards/{id} | read | forwards | Get a single forward rule by ID. |
| PUT | v3/forwards/{id} | write | forwards | Update a single forward rule by ID. |
| DELETE | v3/forwards/{id} | write | forwards | Delete a single forward rule by ID. |
| GET | v2/ip_whitelist | read | ip-allowlist | List Mailgun account IP allowlist entries. |
| POST | v2/ip_whitelist | write | ip-allowlist | Add Mailgun account IP allowlist entry. |
| PUT | v2/ip_whitelist | write | ip-allowlist | Update individual Mailgun account IP allowlist entry's description. |
| DELETE | v2/ip_whitelist | write | ip-allowlist | Delete Mailgun account IP allowlist entry. |
| GET | v1/dynamic_pools/domains | read | ip-pools | List all domains assigned to dynamic IP pools. |
| GET | v1/dynamic_pools/domains/{id}/history | read | ip-pools | List domain history. |
| PUT | v1/dynamic_pools/domains/{id}/override | write | ip-pools | Override domain assignment. |
| DELETE | v1/dynamic_pools/domains/{id}/override | write | ip-pools | Remove override. |
| GET | v1/dynamic_pools/domains/{id}/preview | read | ip-pools | Preview domain assignment. |
| GET | v1/dynamic_pools/history | read | ip-pools | List account history. |
| POST | v3/domains/all/dynamic_pools/enroll | write | ip-pools | Enroll all account domains. |
| GET | v3/domains/dynamic_pools/assignable | read | ip-pools | List assignable domains. |
| GET | v3/dynamic_pools | read | ip-pools | List all Dynamic IP pools. |
| POST | v3/dynamic_pools/all | write | ip-pools | Initialize/set IPs for all pools. |
| DELETE | v3/dynamic_pools/all | write | ip-pools | Remove all dynamic IP pools. |
| PATCH | v3/dynamic_pools/{id} | write | ip-pools | Update pool IPs. |
| POST | v3/dynamic_pools/{id}/{id} | write | ip-pools | Add IP to Dynamic IP Pool. |
| GET | v3/ip_pools | read | ip-pools | List dedicated IP pools of the account. |
| POST | v3/ip_pools | write | ip-pools | Add a new DIPP to the account. |
| GET | v3/ip_pools/{id} | read | ip-pools | Get DIPP details. |
| PATCH | v3/ip_pools/{id} | write | ip-pools | Edit DIPP. |
| DELETE | v3/ip_pools/{id} | write | ip-pools | Delete the DIPP. |
| PUT | v3/ip_pools/{id}/delegate | write | ip-pools | Delegate DIPP to Subaccount. |
| DELETE | v3/ip_pools/{id}/delegate | write | ip-pools | Revoke DIPP from Subaccount. |
| GET | v3/ip_pools/{id}/domains | read | ip-pools | Get domains linked to DIPP. |
| POST | v3/ip_pools/{id}/ips.json | write | ip-pools | Add multiple IPs to the DIPP. |
| PUT | v3/ip_pools/{id}/ips/{id} | write | ip-pools | Add an IP to a DIPP. |
| DELETE | v3/ip_pools/{id}/ips/{id} | write | ip-pools | Remove an IP from a DIPP. |
| GET | v3/ip_warmups | read | ip-warmups | Retrieves the list of in-flight IP address warmup statuses. |
| GET | v3/ip_warmups/{id} | read | ip-warmups | Retrieves the status of an in-flight IP warmup. |
| POST | v3/ip_warmups/{id} | write | ip-warmups | Creates a warmup plan for an IP Address. |
| DELETE | v3/ip_warmups/{id} | write | ip-warmups | Cancels the warmup plan for an IP address. |
| GET | v3/ips | read | ips | List account IPs. |
| GET | v3/ips/account/settings | read | ips | Get DIPP spillover settings for an account. |
| PATCH | v3/ips/account/settings | write | ips | Set or Modify the dedicated IP pool used for IP spillover. |
| GET | v3/ips/details/all | read | ips | List account IPs - detailed view. |
| GET | v3/ips/domain/{id} | read | ips | Get the dedicated IP pool used for spillover for a domain. |
| PATCH | v3/ips/domain/{id} | write | ips | Set or modify the dediciated IP pool used for spillover for a domain. |
| GET | v3/ips/request/new | read | ips | Return the number of IPs available to the account per its billing plan. |
| POST | v3/ips/request/new | write | ips | Add a new dedicated IP to the account. |
| PATCH | v3/ips/subaccounts | write | ips | Update subaccount IP assignments. |
| GET | v3/ips/{id} | read | ips | Get details about account IP. |
| GET | v3/ips/{id}/domains | read | ips | Get all domains of an account where a specific IP is assigned. |
| POST | v3/ips/{id}/domains | write | ips | Assign an IP to all account domains. |
| DELETE | v3/ips/{id}/domains | write | ips | Remove an IP from all account domains. |
| POST | v3/ips/{id}/ip_band | write | ips | Place account IP into a dedicated IP band. |
| GET | v1/keys | read | keys | List Mailgun API keys. |
| POST | v1/keys | write | keys | Create Mailgun API key. |
| POST | v1/keys/public | write | keys | Regenerate Mailgun Public API key. |
| DELETE | v1/keys/{id} | write | keys | Delete Mailgun API key. |
| GET | v3/lists | read | mailing-lists | Get mailing lists. |
| POST | v3/lists | write | mailing-lists | Create a mailing list. |
| GET | v3/lists/pages | read | mailing-lists | Get mailing lists by page. |
| GET | v3/lists/{id} | read | mailing-lists | Get a mailing list by address. |
| PUT | v3/lists/{id} | write | mailing-lists | Update a mailing list. |
| DELETE | v3/lists/{id} | write | mailing-lists | Delete a mailing list. |
| GET | v3/lists/{id}/members | read | mailing-lists | Get mailing lists members. |
| POST | v3/lists/{id}/members | write | mailing-lists | Create a mailing list member. |
| POST | v3/lists/{id}/members.csv | write | mailing-lists | Bulk upload members to a mailing list (CSV). |
| POST | v3/lists/{id}/members.json | write | mailing-lists | Bulk upload members to a mailing list (JSON). |
| GET | v3/lists/{id}/members/pages | read | mailing-lists | Get members by page. |
| GET | v3/lists/{id}/members/{id} | read | mailing-lists | Get a member. |
| PUT | v3/lists/{id}/members/{id} | write | mailing-lists | Update a mailing list member. |
| DELETE | v3/lists/{id}/members/{id} | write | mailing-lists | Delete a member. |
| POST | v3/{id}/messages | write | messages | Send an email. |
| POST | v3/{id}/messages.mime | write | messages | Send an email in MIME format. |
| GET | v3/routes | read | routes | Get all routes. |
| POST | v3/routes | write | routes | Create a route. |
| GET | v3/routes/match | read | routes | Match address to route. |
| GET | v3/routes/{id} | read | routes | Get a route. |
| PUT | v3/routes/{id} | write | routes | Update a route. |
| DELETE | v3/routes/{id} | write | routes | Delete a route. |
| GET | v5/sandbox/auth_recipients | read | sandbox | Get authorized email recipients for a sandbox domain. |
| POST | v5/sandbox/auth_recipients | write | sandbox | Add authorized email recipient for a sandbox domain. |
| DELETE | v5/sandbox/auth_recipients/{id} | write | sandbox | Remove an authorized sandbox domain email recipient. |
| GET | v3/stats/filter | read | stats | Filtered/grouped totals for entire account. |
| GET | v3/stats/total | read | stats | Totals for entire account. |
| GET | v3/stats/total/domains | read | stats | Totals for account domains for a single time resolution. |
| GET | v3/{id}/aggregates/countries | read | stats | Aggregate counts by country. |
| GET | v3/{id}/aggregates/devices | read | stats | Aggregate counts by devices triggering events. |
| GET | v3/{id}/aggregates/providers | read | stats | Aggregate counts by ESP. |
| GET | v3/{id}/stats/total | read | stats | Totals for entire domain. |
| GET | v3/{id}/tag | read | tags | Get a tag. |
| PUT | v3/{id}/tag | write | tags | Update tag. |
| DELETE | v3/{id}/tag | write | tags | Delete tag. |
| GET | v3/{id}/tag/stats | read | tags | Get stats by tag. |
| GET | v3/{id}/tag/stats/aggregates | read | tags | Get aggregate stat types by tag. |
| GET | v3/{id}/tags | read | tags | List all tags. |
| GET | v3/{id}/templates | read | templates | Get templates. |
| POST | v3/{id}/templates | write | templates | Create a template. |
| DELETE | v3/{id}/templates | write | templates | Delete all templates. |
| GET | v3/{id}/templates/{id} | read | templates | Get template. |
| PUT | v3/{id}/templates/{id} | write | templates | Update template. |
| DELETE | v3/{id}/templates/{id} | write | templates | Delete a template. |
| PUT | v3/{id}/templates/{id}/copy | write | templates | Copy a template. |
| PUT | v3/{id}/templates/{id}/rename/{id} | write | templates | Rename a template. |
| GET | v3/{id}/templates/{id}/versions | read | templates | Get all template versions. |
| POST | v3/{id}/templates/{id}/versions | write | templates | Create a template version. |
| GET | v3/{id}/templates/{id}/versions/{id} | read | templates | Get a version. |
| PUT | v3/{id}/templates/{id}/versions/{id} | write | templates | Update a version. |
| DELETE | v3/{id}/templates/{id}/versions/{id} | write | templates | Delete a version. |
| PUT | v3/{id}/templates/{id}/versions/{id}/copy/{id} | write | templates | Copy a version. |
| GET | v4/templates | read | templates | Get account-level templates. |
| POST | v4/templates | write | templates | Create an account-level template. |
| DELETE | v4/templates | write | templates | Delete all account-level templates. |
| GET | v4/templates/{id} | read | templates | Get an account-level template. |
| PUT | v4/templates/{id} | write | templates | Update an account-level template. |
| DELETE | v4/templates/{id} | write | templates | Delete an account-level template. |
| PUT | v4/templates/{id}/copy | write | templates | Copy a template. |
| PUT | v4/templates/{id}/rename/{id} | write | templates | Rename a template. |
| GET | v4/templates/{id}/versions | read | templates | Get all account-level template versions. |
| POST | v4/templates/{id}/versions | write | templates | Create an account-level template version. |
| GET | v4/templates/{id}/versions/{id} | read | templates | Get an account-level template version. |
| PUT | v4/templates/{id}/versions/{id} | write | templates | Update an account-level template version. |
| DELETE | v4/templates/{id}/versions/{id} | write | templates | Delete an account-level template version. |
| PUT | v4/templates/{id}/versions/{id}/copy/{id} | write | templates | Copy an account-level template version. |
| GET | v1/thresholds/alerts/send | read | thresholds | List send alerts. |
| POST | v1/thresholds/alerts/send | write | thresholds | Create a send alert for an account. |
| GET | v1/thresholds/alerts/send/{id} | read | thresholds | Get a send alert. |
| PUT | v1/thresholds/alerts/send/{id} | write | thresholds | Update a send alert. |
| DELETE | v1/thresholds/alerts/send/{id} | write | thresholds | Delete a send alert. |
| GET | v1/thresholds/hits | read | thresholds | List account hits. |
| GET | v1/thresholds/limits | read | thresholds | List limit thresholds for an account. |
| POST | v1/thresholds/limits | write | thresholds | Create a limit threshold for an account. |
| GET | v1/thresholds/limits/{id} | read | thresholds | Get a limit threshold for an account. |
| PUT | v1/thresholds/limits/{id} | write | thresholds | Update a limit threshold for an account. |
| DELETE | v1/thresholds/limits/{id} | write | thresholds | Delete a limit threshold for an account. |
| GET | v2/thresholds/limits | read | thresholds | List all limits for a given subaccount. |
| POST | v2/thresholds/limits | write | thresholds | Create a limit for an account or subaccount. |
| GET | v2/thresholds/limits-primary | read | thresholds | Get parent-level limit warning settings for an account. |
| POST | v2/thresholds/limits-primary | write | thresholds | Create parent-level limit warning settings for an account. |
| PUT | v2/thresholds/limits-primary | write | thresholds | Update parent-level limit warning settings for an account. |
| DELETE | v2/thresholds/limits-primary | write | thresholds | Delete parent-level limit warning settings for an account. |
| GET | v2/thresholds/limits/{id} | read | thresholds | Get a limit for a subaccount for the given metric if it exists, otherwise returns 404. Takes the SubAccountID from the X-Mailgun-On-Behalf-Of header. |
| PUT | v2/thresholds/limits/{id} | write | thresholds | Update a limit for an account given the metric name in the path. |
| DELETE | v2/thresholds/limits/{id} | write | thresholds | Delete a limit for an account given the metric name in the path. |
| POST | v2/x509/{id} | write | tracking-certificates | Tracking Certificate: Generate. |
| PUT | v2/x509/{id} | write | tracking-certificates | Tracking Certificate: Regenerate expired certificate. |
| GET | v2/x509/{id}/status | read | tracking-certificates | Tracking Certificate: Get certificate and status. |
| GET | v3/{id}/unsubscribes | read | unsubscribes | List all unsubscribes. |
| POST | v3/{id}/unsubscribes | write | unsubscribes | Add unsubscribes. |
| DELETE | v3/{id}/unsubscribes | write | unsubscribes | Clear all unsubscribes. |
| POST | v3/{id}/unsubscribes/import | write | unsubscribes | Import unsubscribe list. |
| GET | v3/{id}/unsubscribes/{id} | read | unsubscribes | Lookup unsubscribe record. |
| DELETE | v3/{id}/unsubscribes/{id} | write | unsubscribes | Remove unsubscribe. |
| GET | v5/users | read | users | Get users on an account. |
| GET | v5/users/me | read | users | Get one's own user details. |
| GET | v5/users/{id} | read | users | Get a user's details. |
| GET | v1/webhooks | read | webhooks | List account-level webhooks. |
| POST | v1/webhooks | write | webhooks | Create an account-level webhook. |
| DELETE | v1/webhooks | write | webhooks | Delete account-level webhooks. |
| GET | v1/webhooks/{id} | read | webhooks | Get account-level webhook by ID. |
| PUT | v1/webhooks/{id} | write | webhooks | Update an account-level webhook. |
| DELETE | v1/webhooks/{id} | write | webhooks | Delete account-level webhook by ID. |
