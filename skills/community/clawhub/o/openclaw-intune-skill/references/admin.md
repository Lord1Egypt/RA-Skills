# Users, Groups, RBAC, Terms & Notifications

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.
Note: `$filter`/`$search` on `/users` and `/groups` needs
`ConsistencyLevel: eventual` + `$count=true` — `graph.sh` adds this
automatically.

## 1. Users & groups

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 1.1 | List users | GET `/users?$select=displayName,userPrincipalName,accountEnabled,jobTitle` | 0 | |
| 1.2 | Search user | GET `/users?$filter=startsWith(displayName,'{name}')` | 0 | |
| 1.3 | User details | GET `/users/{userId}` | 0 | |
| 1.4 | List groups | GET `/groups?$select=displayName,description,groupTypes,membershipRule` | 0 | |
| 1.5 | Group members | GET `/groups/{groupId}/members` | 0 | |
| 1.6 | Add user to group | POST `/groups/{groupId}/members/$ref` | 2 | Body: `{"@odata.id":"https://graph.microsoft.com/v1.0/directoryObjects/{userId}"}`. Fails on dynamic groups — check `groupTypes` first |
| 1.7 | Remove user from group | DELETE `/groups/{groupId}/members/{userId}/$ref` | 2 | |
| 1.8 | Devices of a user | GET `/users/{userId}/managedDevices` | 0 | |

Group membership changes (1.6/1.7) are **Tier 2: never execute without an
explicit confirmation** that names the user, the group, whether the group is
static, and the likely downstream effects — group changes cascade into
policy, app and Conditional Access assignments.

## 2. RBAC (Intune roles)

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 2.1 | List role definitions | GET `/deviceManagement/roleDefinitions` | 0 |
| 2.2 | List role assignments | GET `/deviceManagement/roleAssignments` | 0 |
| 2.3 | Role details | GET `/deviceManagement/roleDefinitions/{id}` | 0 |

## 3. Terms & Conditions, notification templates

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 3.1 | List T&C | GET `/deviceManagement/termsAndConditions` | 0 |
| 3.2 | T&C details | GET `/deviceManagement/termsAndConditions/{id}` | 0 |
| 3.3 | Acceptance status | GET `/deviceManagement/termsAndConditions/{id}/acceptanceStatuses` | 0 |
| 3.4 | Create T&C | POST `/deviceManagement/termsAndConditions` | 2 |
| 3.5 | List notification templates | GET `/deviceManagement/notificationMessageTemplates` | 0 |
| 3.6 | Create notification template | POST `/deviceManagement/notificationMessageTemplates` | 2 |
| 3.7 | Send test notification | POST `/deviceManagement/notificationMessageTemplates/{id}/sendTestMessage` | 1 |
