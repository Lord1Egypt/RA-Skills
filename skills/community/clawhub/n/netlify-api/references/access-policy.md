# Netlify access policy

An access policy limits which endpoints Netlify connections may call through Maton. Netlify doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/netlify#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Netlify: its 53 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create netlify --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v1/accounts/types"},
    {"method": "GET", "path": "api/v1/services"},
    {"method": "GET", "path": "api/v1/services/{id}"},
    {"method": "GET", "path": "api/v1/services/{id}/manifest"},
    {"method": "GET", "path": "api/v1/agent_runners"},
    {"method": "GET", "path": "api/v1/agent_runners/{id}"},
    {"method": "GET", "path": "api/v1/agent_runners/{id}/diff"},
    {"method": "GET", "path": "api/v1/agent_runners/{id}/sessions"},
    {"method": "GET", "path": "api/v1/agent_runners/{id}/sessions/{id}"},
    {"method": "GET", "path": "api/v1/ai-gateway/providers"},
    {"method": "GET", "path": "api/v1/sites/{id}/assets"},
    {"method": "GET", "path": "api/v1/sites/{id}/assets/{id}"},
    {"method": "GET", "path": "api/v1/accounts/{id}/audit"},
    {"method": "GET", "path": "api/v1/billing/payment_methods"},
    {"method": "GET", "path": "api/v1/sites/{id}/plugin_runs/latest"},
    {"method": "GET", "path": "api/v1/builds/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/builds"},
    {"method": "GET", "path": "api/v1/{id}/builds/status"},
    {"method": "GET", "path": "api/v1/sites/{id}/database/compute/settings"},
    {"method": "GET", "path": "api/v1/sites/{id}/database/migrations"},
    {"method": "GET", "path": "api/v1/sites/{id}/database/migrations/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/database/snapshots"},
    {"method": "GET", "path": "api/v1/deploy_keys"},
    {"method": "GET", "path": "api/v1/deploy_keys/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/deployed-branches"},
    {"method": "GET", "path": "api/v1/sites/{id}/dev_servers"},
    {"method": "GET", "path": "api/v1/sites/{id}/dev_servers/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/dns"},
    {"method": "GET", "path": "api/v1/dns_zones"},
    {"method": "GET", "path": "api/v1/dns_zones/{id}"},
    {"method": "GET", "path": "api/v1/dns_zones/{id}/dns_records"},
    {"method": "GET", "path": "api/v1/dns_zones/{id}/dns_records/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/files"},
    {"method": "GET", "path": "api/v1/sites/{id}/files/**"},
    {"method": "GET", "path": "api/v1/forms/{id}/submissions"},
    {"method": "GET", "path": "api/v1/sites/{id}/forms"},
    {"method": "GET", "path": "api/v1/sites/{id}/functions"},
    {"method": "GET", "path": "api/v1/hooks/types"},
    {"method": "POST", "path": "api/v1/sites/{id}/identity/{id}/users/lookup"},
    {"method": "GET", "path": "api/v1/sites/{id}/identity/{id}/users/{id}"},
    {"method": "GET", "path": "api/v1/{id}/members"},
    {"method": "GET", "path": "api/v1/{id}/members/{id}"},
    {"method": "GET", "path": "api/v1/oauth/tickets/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/metadata"},
    {"method": "GET", "path": "api/v1/sites/{id}/snippets"},
    {"method": "GET", "path": "api/v1/sites/{id}/snippets/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/ssl"},
    {"method": "GET", "path": "api/v1/sites/{id}/ssl/certificates"},
    {"method": "GET", "path": "api/v1/sites/{id}/submissions"},
    {"method": "GET", "path": "api/v1/submissions/{id}"},
    {"method": "GET", "path": "api/v1/sites/{id}/traffic_splits"},
    {"method": "GET", "path": "api/v1/sites/{id}/traffic_splits/{id}"},
    {"method": "GET", "path": "api/v1/user"}
  ],
  "deny": []
}
```

## Endpoints

The Netlify endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v1/accounts | write | accounts | List the current user's teams. Kept out of read: response includes the team site_jwt_secret field. |
| POST | api/v1/accounts | write | accounts | Create a team. |
| GET | api/v1/accounts/types | read | accounts | List plans available for new teams. |
| GET | api/v1/accounts/{id} | write | accounts | Get a team. Kept out of read: response includes the team site_jwt_secret field. |
| PUT | api/v1/accounts/{id} | write | accounts | Update a team. |
| DELETE | api/v1/accounts/{id} | write | accounts | Cancel a team. |
| GET | api/v1/services | read | add-ons | List add-on services. |
| GET | api/v1/services/{id} | read | add-ons | Get an add-on service. |
| GET | api/v1/services/{id}/manifest | read | add-ons | Get an add-on service's manifest. |
| GET | api/v1/sites/{id}/service-instances | write | add-ons | List a site's add-on instances. Kept out of read: response includes the add-on instance env values. |
| POST | api/v1/sites/{id}/services/{id}/instances | write | add-ons | Create an add-on instance. |
| GET | api/v1/sites/{id}/services/{id}/instances/{id} | write | add-ons | Get an add-on instance. Kept out of read: response includes the add-on instance env values. |
| PUT | api/v1/sites/{id}/services/{id}/instances/{id} | write | add-ons | Update an add-on instance. |
| DELETE | api/v1/sites/{id}/services/{id}/instances/{id} | write | add-ons | Delete an add-on instance. |
| GET | api/v1/sites/{id}/agent_runner_hooks | write | agent runner hooks | List a site's agent runner hooks. Kept out of read: response includes hook URLs that trigger runs without further auth. |
| POST | api/v1/sites/{id}/agent_runner_hooks | write | agent runner hooks | Create an agent runner hook. |
| GET | api/v1/sites/{id}/agent_runner_hooks/{id} | write | agent runner hooks | Get an agent runner hook. Kept out of read: response includes hook URLs that trigger runs without further auth. |
| PUT | api/v1/sites/{id}/agent_runner_hooks/{id} | write | agent runner hooks | Update an agent runner hook. |
| DELETE | api/v1/sites/{id}/agent_runner_hooks/{id} | write | agent runner hooks | Delete an agent runner hook. |
| GET | api/v1/agent_runners | read | agent runners | List a site's agent runs. |
| POST | api/v1/agent_runners | write | agent runners | Start an agent run. |
| POST | api/v1/agent_runners/upload_url | write | agent runners | Create an upload URL for agent run files. |
| GET | api/v1/agent_runners/{id} | read | agent runners | Get an agent run. |
| PATCH | api/v1/agent_runners/{id} | write | agent runners | Update an agent run. |
| DELETE | api/v1/agent_runners/{id} | write | agent runners | Stop an agent run (alias). |
| POST | api/v1/agent_runners/{id}/archive | write | agent runners | Archive an agent run. |
| POST | api/v1/agent_runners/{id}/commit | write | agent runners | Commit an agent run's changes to a branch. |
| GET | api/v1/agent_runners/{id}/diff | read | agent runners | Get an agent run's diff. |
| POST | api/v1/agent_runners/{id}/pull_request | write | agent runners | Open a pull request from an agent run. |
| GET | api/v1/agent_runners/{id}/sessions | read | agent runners | List an agent run's sessions. |
| POST | api/v1/agent_runners/{id}/sessions | write | agent runners | Start a follow-up agent run session. |
| GET | api/v1/agent_runners/{id}/sessions/{id} | read | agent runners | Get an agent run session. |
| PATCH | api/v1/agent_runners/{id}/sessions/{id} | write | agent runners | Update an agent run session. |
| DELETE | api/v1/agent_runners/{id}/sessions/{id} | write | agent runners | Stop an agent run session (alias). |
| POST | api/v1/agent_runners/{id}/sessions/{id}/answers | write | agent runners | Answer an agent run session's pending interaction. |
| POST | api/v1/agent_runners/{id}/sessions/{id}/stop | write | agent runners | Stop an agent run session. |
| POST | api/v1/agent_runners/{id}/stop | write | agent runners | Stop an agent run. |
| POST | api/v1/sites/{id}/agent_runners | write | agent runners | Start an agent run on a site. |
| GET | api/v1/accounts/{id}/ai-gateway/token | write | ai gateway | Get a team's AI Gateway token. Kept out of read: returns an AI Gateway token. |
| GET | api/v1/ai-gateway/providers | read | ai gateway | List AI Gateway providers and models. |
| GET | api/v1/sites/{id}/ai-gateway/token | write | ai gateway | Get a site's AI Gateway token. Kept out of read: returns an AI Gateway token. |
| GET | api/v1/sites/{id}/assets | read | assets | List a site's assets. |
| POST | api/v1/sites/{id}/assets | write | assets | Create a site asset. |
| GET | api/v1/sites/{id}/assets/{id} | read | assets | Get a site asset. |
| PUT | api/v1/sites/{id}/assets/{id} | write | assets | Update a site asset's state. |
| DELETE | api/v1/sites/{id}/assets/{id} | write | assets | Delete a site asset. |
| GET | api/v1/sites/{id}/assets/{id}/public_signature | write | assets | Get a site asset's URL. Kept out of read: returns a signed asset URL. |
| GET | api/v1/accounts/{id}/audit | read | audit log | List a team's audit log events. |
| GET | api/v1/billing/payment_methods | read | billing | List payment methods. |
| GET | api/v1/sites/{id}/build_hooks | write | build hooks | List a site's build hooks. Kept out of read: build hook URLs trigger builds without further auth. |
| POST | api/v1/sites/{id}/build_hooks | write | build hooks | Create a build hook. |
| GET | api/v1/sites/{id}/build_hooks/{id} | write | build hooks | Get a build hook. Kept out of read: build hook URLs trigger builds without further auth. |
| PUT | api/v1/sites/{id}/build_hooks/{id} | write | build hooks | Update a build hook. |
| DELETE | api/v1/sites/{id}/build_hooks/{id} | write | build hooks | Delete a build hook. |
| GET | api/v1/sites/{id}/plugin_runs/latest | read | build plugins | List a site's latest build plugin runs. |
| PUT | api/v1/sites/{id}/plugins/{id} | write | build plugins | Update a site's build plugin. |
| GET | api/v1/builds/{id} | read | builds | Get a build. |
| POST | api/v1/builds/{id}/log | write | builds | Add a message to a build log. |
| POST | api/v1/builds/{id}/start | write | builds | Mark a build as started. |
| GET | api/v1/sites/{id}/builds | read | builds | List a site's builds. |
| POST | api/v1/sites/{id}/builds | write | builds | Start a build. |
| GET | api/v1/{id}/builds/status | read | builds | Get a team's build status. |
| POST | api/v1/purge | write | cache | Purge cached content. |
| GET | api/v1/sites/{id}/database | write | database | Get a site database. Kept out of read: response includes the database connection string. |
| POST | api/v1/sites/{id}/database | write | database | Create a site database. |
| DELETE | api/v1/sites/{id}/database | write | database | Delete a site database. |
| POST | api/v1/sites/{id}/database/branch | write | database | Create a database branch. |
| GET | api/v1/sites/{id}/database/branch/{id} | write | database | Get a database branch. Kept out of read: response includes the database connection string. |
| DELETE | api/v1/sites/{id}/database/branch/{id} | write | database | Delete a database branch. |
| PUT | api/v1/sites/{id}/database/branch/{id}/compute/settings | write | database | Set a database branch's compute settings. |
| POST | api/v1/sites/{id}/database/branch/{id}/reset | write | database | Reset a database branch. |
| GET | api/v1/sites/{id}/database/branches | write | database | List database branches. Kept out of read: response includes the database connection string. |
| GET | api/v1/sites/{id}/database/compute/settings | read | database | Get database compute settings. |
| PUT | api/v1/sites/{id}/database/compute/settings | write | database | Set database compute settings. |
| DELETE | api/v1/sites/{id}/database/compute/settings | write | database | Reset database compute settings to defaults. |
| GET | api/v1/sites/{id}/database/migrations | read | database | List database migrations. |
| GET | api/v1/sites/{id}/database/migrations/{id} | read | database | Get a database migration. |
| POST | api/v1/sites/{id}/database/migrations/{id} | write | database | Run database migrations for a deploy. |
| POST | api/v1/sites/{id}/database/snapshot | write | database | Create a database snapshot. |
| DELETE | api/v1/sites/{id}/database/snapshot/{id} | write | database | Delete a database snapshot. |
| POST | api/v1/sites/{id}/database/snapshot/{id}/restore | write | database | Restore a database snapshot. |
| GET | api/v1/sites/{id}/database/snapshots | read | database | List database snapshots. |
| GET | api/v1/deploy_keys | read | deploy keys | List deploy keys. |
| POST | api/v1/deploy_keys | write | deploy keys | Create a deploy key. |
| GET | api/v1/deploy_keys/{id} | read | deploy keys | Get a deploy key. |
| DELETE | api/v1/deploy_keys/{id} | write | deploy keys | Delete a deploy key. |
| GET | api/v1/sites/{id}/deployed-branches | read | deployed branches | List a site's deployed branches. |
| GET | api/v1/deploys/{id} | write | deploys | Get a deploy. Kept out of read: response includes the deploy skew_protection_token. |
| DELETE | api/v1/deploys/{id} | write | deploys | Delete a deploy. |
| POST | api/v1/deploys/{id}/cancel | write | deploys | Cancel a deploy. |
| PUT | api/v1/deploys/{id}/edge_functions/{id} | write | deploys | Upload a deploy's edge functions bundle. |
| PUT | `api/v1/deploys/{id}/files/**` | write | deploys | Upload a deploy file. |
| PUT | api/v1/deploys/{id}/functions/{id} | write | deploys | Upload a deploy function. |
| POST | api/v1/deploys/{id}/lock | write | deploys | Lock a deploy. |
| POST | api/v1/deploys/{id}/plugin_runs | write | deploys | Create a build plugin run. |
| PUT | api/v1/deploys/{id}/server/{id} | write | deploys | Upload a deploy's Netlify Server bundle. |
| POST | api/v1/deploys/{id}/unlock | write | deploys | Unlock a deploy. |
| PATCH | api/v1/deploys/{id}/validations_report | write | deploys | Update a deploy's validations report. |
| GET | api/v1/sites/{id}/deploys | write | deploys | List a site's deploys. Kept out of read: response includes the deploy skew_protection_token. |
| POST | api/v1/sites/{id}/deploys | write | deploys | Create a deploy. |
| GET | api/v1/sites/{id}/deploys/{id} | write | deploys | Get a site's deploy. Kept out of read: response includes the deploy skew_protection_token. |
| PUT | api/v1/sites/{id}/deploys/{id} | write | deploys | Update a deploy. |
| DELETE | api/v1/sites/{id}/deploys/{id} | write | deploys | Delete a site's deploy. |
| POST | api/v1/sites/{id}/deploys/{id}/restore | write | deploys | Restore a previous deploy. |
| GET | api/v1/sites/{id}/dev_server_hooks | write | dev server hooks | List a site's dev server hooks. Kept out of read: response includes hook URLs that trigger runs without further auth. |
| POST | api/v1/sites/{id}/dev_server_hooks | write | dev server hooks | Create a dev server hook. |
| GET | api/v1/sites/{id}/dev_server_hooks/{id} | write | dev server hooks | Get a dev server hook. Kept out of read: response includes hook URLs that trigger runs without further auth. |
| PUT | api/v1/sites/{id}/dev_server_hooks/{id} | write | dev server hooks | Update a dev server hook. |
| DELETE | api/v1/sites/{id}/dev_server_hooks/{id} | write | dev server hooks | Delete a dev server hook. |
| GET | api/v1/sites/{id}/dev_servers | read | dev servers | List a site's dev servers. |
| POST | api/v1/sites/{id}/dev_servers | write | dev servers | Start a dev server. |
| DELETE | api/v1/sites/{id}/dev_servers | write | dev servers | Stop a branch's dev servers. |
| GET | api/v1/sites/{id}/dev_servers/{id} | read | dev servers | Get a dev server. |
| POST | api/v1/sites/{id}/dev_servers/{id}/activity | write | dev servers | Record dev server activity. |
| POST | api/v1/sites/{id}/dev_servers/{id}/state | write | dev servers | Update a dev server's state. |
| GET | api/v1/sites/{id}/dns | read | dns | Get a site's DNS configuration. |
| PUT | api/v1/sites/{id}/dns | write | dns | Configure a site's DNS. |
| GET | api/v1/dns_zones | read | dns zones | List DNS zones. |
| POST | api/v1/dns_zones | write | dns zones | Create a DNS zone. |
| GET | api/v1/dns_zones/{id} | read | dns zones | Get a DNS zone. |
| DELETE | api/v1/dns_zones/{id} | write | dns zones | Delete a DNS zone. |
| GET | api/v1/dns_zones/{id}/dns_records | read | dns zones | List a DNS zone's records. |
| POST | api/v1/dns_zones/{id}/dns_records | write | dns zones | Create a DNS record. |
| GET | api/v1/dns_zones/{id}/dns_records/{id} | read | dns zones | Get a DNS record. |
| DELETE | api/v1/dns_zones/{id}/dns_records/{id} | write | dns zones | Delete a DNS record. |
| PUT | api/v1/dns_zones/{id}/transfer | write | dns zones | Transfer a DNS zone to another team. |
| GET | api/v1/accounts/{id}/env | write | environment variables | List environment variables for a team or site. Kept out of read: returns environment variable values, which commonly hold secrets. |
| POST | api/v1/accounts/{id}/env | write | environment variables | Create environment variables. |
| GET | api/v1/accounts/{id}/env/{id} | write | environment variables | Get an environment variable. Kept out of read: returns environment variable values, which commonly hold secrets. |
| PUT | api/v1/accounts/{id}/env/{id} | write | environment variables | Update an environment variable. |
| PATCH | api/v1/accounts/{id}/env/{id} | write | environment variables | Set a value on an environment variable. |
| DELETE | api/v1/accounts/{id}/env/{id} | write | environment variables | Delete an environment variable. |
| DELETE | api/v1/accounts/{id}/env/{id}/value/{id} | write | environment variables | Delete an environment variable value. |
| GET | api/v1/sites/{id}/env | write | environment variables | List environment variables for a site. Kept out of read: returns environment variable values, which commonly hold secrets. |
| GET | api/v1/sites/{id}/files | read | files | List a site's files. |
| GET | `api/v1/sites/{id}/files/**` | read | files | Get a site file by path. |
| GET | api/v1/forms/{id}/submissions | read | forms | List a form's submissions. |
| GET | api/v1/sites/{id}/forms | read | forms | List a site's forms. |
| DELETE | api/v1/sites/{id}/forms/{id} | write | forms | Delete a form. |
| GET | api/v1/sites/{id}/functions | read | functions | Search a site's functions. |
| GET | api/v1/hooks | write | hooks | List a site's outgoing hooks. Kept out of read: hook data can hold destination URLs and signing secrets. |
| POST | api/v1/hooks | write | hooks | Create an outgoing hook. |
| GET | api/v1/hooks/types | read | hooks | List outgoing hook types. |
| GET | api/v1/hooks/{id} | write | hooks | Get an outgoing hook. Kept out of read: hook data can hold destination URLs and signing secrets. |
| PUT | api/v1/hooks/{id} | write | hooks | Update an outgoing hook. |
| DELETE | api/v1/hooks/{id} | write | hooks | Delete an outgoing hook. |
| POST | api/v1/hooks/{id}/enable | write | hooks | Re-enable an outgoing hook. |
| POST | api/v1/sites/{id}/identity/{id}/users/lookup | read | identity | Look up an Identity user by email. |
| GET | api/v1/sites/{id}/identity/{id}/users/{id} | read | identity | Get an Identity user. |
| GET | api/v1/{id}/members | read | members | List a team's members. |
| POST | api/v1/{id}/members | write | members | Add a member to a team. |
| GET | api/v1/{id}/members/{id} | read | members | Get a team member. |
| PUT | api/v1/{id}/members/{id} | write | members | Update a team member. |
| DELETE | api/v1/{id}/members/{id} | write | members | Remove a team member. |
| POST | api/v1/oauth/tickets | write | oauth | Create an OAuth ticket. |
| GET | api/v1/oauth/tickets/{id} | read | oauth | Get an OAuth ticket. |
| POST | api/v1/oauth/tickets/{id}/exchange | write | oauth | Exchange an OAuth ticket for an access token. |
| GET | api/v1/sites | write | sites | List sites. Kept out of read: response includes the site password, build environment variables and the default hooks access token. |
| POST | api/v1/sites | write | sites | Create a site. |
| GET | api/v1/sites/{id} | write | sites | Get a site. Kept out of read: response includes the site password, build environment variables and the default hooks access token. |
| PATCH | api/v1/sites/{id} | write | sites | Update a site. |
| DELETE | api/v1/sites/{id} | write | sites | Delete a site. |
| PUT | api/v1/sites/{id}/disable | write | sites | Disable a site. |
| PUT | api/v1/sites/{id}/enable | write | sites | Enable a site. |
| GET | api/v1/sites/{id}/metadata | read | sites | Get a site's metadata. |
| PUT | api/v1/sites/{id}/metadata | write | sites | Update a site's metadata. |
| PUT | api/v1/sites/{id}/rollback | write | sites | Roll back a site's production deploy. |
| PUT | api/v1/sites/{id}/unlink_repo | write | sites | Unlink a site's repository. |
| GET | api/v1/{id}/sites | write | sites | List a team's sites. Kept out of read: response includes the site password, build environment variables and the default hooks access token. |
| POST | api/v1/{id}/sites | write | sites | Create a site in a team. |
| GET | api/v1/sites/{id}/snippets | read | snippets | List a site's snippets. |
| POST | api/v1/sites/{id}/snippets | write | snippets | Create a snippet. |
| GET | api/v1/sites/{id}/snippets/{id} | read | snippets | Get a snippet. |
| PUT | api/v1/sites/{id}/snippets/{id} | write | snippets | Update a snippet. |
| DELETE | api/v1/sites/{id}/snippets/{id} | write | snippets | Delete a snippet. |
| GET | api/v1/sites/{id}/ssl | read | ssl | Get a site's TLS certificate. |
| POST | api/v1/sites/{id}/ssl | write | ssl | Provision or update a site's TLS certificate. |
| GET | api/v1/sites/{id}/ssl/certificates | read | ssl | List TLS certificates for a site's domain. |
| GET | api/v1/sites/{id}/submissions | read | submissions | List a site's form submissions. |
| GET | api/v1/submissions/{id} | read | submissions | Get a form submission. |
| DELETE | api/v1/submissions/{id} | write | submissions | Delete a form submission. |
| GET | api/v1/sites/{id}/traffic_splits | read | traffic splits | List a site's split tests. |
| POST | api/v1/sites/{id}/traffic_splits | write | traffic splits | Create a split test. |
| GET | api/v1/sites/{id}/traffic_splits/{id} | read | traffic splits | Get a split test. |
| PUT | api/v1/sites/{id}/traffic_splits/{id} | write | traffic splits | Update a split test. |
| POST | api/v1/sites/{id}/traffic_splits/{id}/publish | write | traffic splits | Publish a split test. |
| POST | api/v1/sites/{id}/traffic_splits/{id}/unpublish | write | traffic splits | Unpublish a split test. |
| GET | api/v1/user | read | user | Get the current user. |
