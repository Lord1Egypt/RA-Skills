# Grafana access policy

An access policy limits which endpoints Grafana connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/grafana#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Grafana: its 28 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create grafana --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/health"},
    {"method": "GET", "path": "api/search"},
    {"method": "GET", "path": "api/dashboards/home"},
    {"method": "GET", "path": "api/dashboards/tags"},
    {"method": "GET", "path": "api/dashboards/uid/{id}"},
    {"method": "GET", "path": "api/folders"},
    {"method": "GET", "path": "api/folders/{id}"},
    {"method": "GET", "path": "api/datasources"},
    {"method": "GET", "path": "api/datasources/{id}"},
    {"method": "GET", "path": "api/datasources/uid/{id}"},
    {"method": "GET", "path": "api/datasources/name/{id}"},
    {"method": "GET", "path": "api/annotations"},
    {"method": "GET", "path": "api/annotations/{id}"},
    {"method": "GET", "path": "api/org"},
    {"method": "GET", "path": "api/org/users"},
    {"method": "GET", "path": "api/user"},
    {"method": "GET", "path": "api/user/orgs"},
    {"method": "GET", "path": "api/users/search"},
    {"method": "GET", "path": "api/teams/search"},
    {"method": "GET", "path": "api/teams/{id}"},
    {"method": "GET", "path": "api/teams/{id}/members"},
    {"method": "GET", "path": "api/serviceaccounts/search"},
    {"method": "GET", "path": "api/plugins"},
    {"method": "GET", "path": "api/ruler/grafana/api/v1/rules"},
    {"method": "GET", "path": "api/v1/provisioning/alert-rules"},
    {"method": "GET", "path": "api/v1/provisioning/alert-rules/{id}"},
    {"method": "GET", "path": "api/v1/provisioning/contact-points"},
    {"method": "GET", "path": "api/v1/provisioning/policies"}
  ],
  "deny": []
}
```

## Endpoints

The Grafana endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/health | read | general | Check that Grafana is up. |
| GET | api/search | read | dashboards | Search dashboards and folders. |
| GET | api/dashboards/home | read | dashboards | Get the home dashboard. |
| GET | api/dashboards/tags | read | dashboards | List dashboard tags. |
| GET | api/dashboards/uid/{id} | read | dashboards | Get a dashboard. |
| POST | api/dashboards/db | write | dashboards | Create or update a dashboard. |
| DELETE | api/dashboards/uid/{id} | write | dashboards | Delete a dashboard. |
| GET | api/folders | read | folders | List folders. |
| GET | api/folders/{id} | read | folders | Get a folder. |
| POST | api/folders | write | folders | Create a folder. |
| PUT | api/folders/{id} | write | folders | Update a folder. |
| DELETE | api/folders/{id} | write | folders | Delete a folder. |
| GET | api/datasources | read | datasources | List datasources. |
| GET | api/datasources/{id} | read | datasources | Get a datasource by ID. |
| GET | api/datasources/uid/{id} | read | datasources | Get a datasource by UID. |
| GET | api/datasources/name/{id} | read | datasources | Get a datasource by name. |
| POST | api/datasources | write | datasources | Create a datasource. |
| PUT | api/datasources/{id} | write | datasources | Update a datasource. |
| DELETE | api/datasources/{id} | write | datasources | Delete a datasource. |
| POST | api/ds/query | write | datasources | Run a datasource query. SQL datasources can change data. |
| GET | api/annotations | read | annotations | List annotations. |
| GET | api/annotations/{id} | read | annotations | Get an annotation. |
| POST | api/annotations | write | annotations | Create an annotation. |
| PUT | api/annotations/{id} | write | annotations | Update an annotation. |
| DELETE | api/annotations/{id} | write | annotations | Delete an annotation. |
| GET | api/org | read | organization | Get the current organization. |
| GET | api/org/users | read | organization | List users in the organization. |
| GET | api/user | read | users | Get the signed-in user. |
| GET | api/user/orgs | read | users | List the signed-in user's organizations. |
| GET | api/users/search | read | users | Search users. |
| GET | api/teams/search | read | teams | Search teams. |
| GET | api/teams/{id} | read | teams | Get a team. |
| GET | api/teams/{id}/members | read | teams | List a team's members. |
| POST | api/teams | write | teams | Create a team. |
| PUT | api/teams/{id} | write | teams | Update a team. |
| DELETE | api/teams/{id} | write | teams | Delete a team. |
| GET | api/serviceaccounts/search | read | service accounts | Search service accounts. |
| GET | api/plugins | read | plugins | List installed plugins. |
| GET | api/ruler/grafana/api/v1/rules | read | alerting | List alert rules. |
| GET | api/v1/provisioning/alert-rules | read | alerting | List provisioned alert rules. |
| GET | api/v1/provisioning/alert-rules/{id} | read | alerting | Get a provisioned alert rule. |
| GET | api/v1/provisioning/contact-points | read | alerting | List contact points. |
| GET | api/v1/provisioning/policies | read | alerting | Get the notification policy tree. |
