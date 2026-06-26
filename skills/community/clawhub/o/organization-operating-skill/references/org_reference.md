# Org Reference

## When to Read

- When working on organization list, detail, create, update, member, or join flows
- When fetching the default organization avatar list
- When checking the minimum request body or permission constraints for organization endpoints

## Related Capabilities

| Capability ID | API | Method |
| --- | --- | --- |
| `web.config.get` | `/outer/api/nl/v1/web/config/get` | `GET` |
| `org.list` | `/outer/api/v1/common/user/org/page` | `GET` |
| `org.detail` | `/outer/api/v1/common/org/info/detail` | `GET` |
| `org.detail.manage` | `/outer/api/v1/common/org/info/basic` | `GET` |
| `org.create` | `/outer/api/v1/common/org/create` | `POST` |
| `org.update` | `/outer/api/v1/common/org/update` | `PUT` |
| `org.member.list` | `/outer/api/v1/common/org/member/list` | `GET` |
| `org.member.page` | `/outer/api/v1/common/org/member/page` | `GET` |
| `org.join` | `/outer/api/v1/common/voiceroom/member/joinOrg` | `POST` |

## `web.config.get`

- Endpoint: `GET /outer/api/nl/v1/web/config/get`
- Recommended web-style headers:
  - `x-platform=3`
  - `x-device-id`
  - `x-device_id`
  - `x-version`
  - `x-buildnumber`
  - `x-brand`
  - `x-model`
  - `x-system-version`
  - `x-system_version`
- Key response field:
  - `data.groupAvatarList[]`
- Verified behavior:
  - the test environment returned 6 default organization avatars
  - `groupAvatarList[].url` can be used directly as `org.create.avatar`

## `org.create`

- Endpoint: `POST /outer/api/v1/common/org/create`
- Authentication: yes
- Minimum request body:
  - `name`
  - `avatar`
- Optional fields:
  - `info`
  - `tagId`
  - `background`
  - `location`
  - `country`
  - `city`
  - `region`
  - `ruleInfo`
  - `settings`
  - `avatarNew`
  - `backgroundNew`
- Confirmed constraints:
  - `name` cannot be empty
  - duplicate names may return `CODE_10225`
  - an empty `avatar` may return `CODE_10240`
  - the backend also checks creation eligibility and creation cost
- Operational notes:
  - call `user-info` before creating an organization
  - if the response returns `isAllowCreate=0`, that account is usually not a stable choice for organization creation
- Skill behavior:
  - if `org-create` is called without an avatar, the CLI automatically calls `web-config-get` and picks the first default avatar

Minimum example:

```json
{
  "name": "Agent Org Demo",
  "avatar": "https://na-rs2.podupx.com/avatar/org/orgh1.png",
  "info": "Demo organization created automatically by an agent."
}
```

## `org.update`

- Endpoint: `PUT /outer/api/v1/common/org/update`
- Authentication: yes
- Required field:
  - `id`
- Updatable fields:
  - `info`
  - `background`
  - `backgroundNew`
  - `avatar`
  - `avatarNew`
  - `country`
  - `city`
  - `region`
  - `location`
  - `ruleInfo`
  - `tagId`
  - `settings`
  - `diplomat`
- Confirmed constraints:
  - `name` cannot be changed
  - a missing organization may return `CODE_10201`
  - `checked=0` may return `CODE_90297`
  - the caller must be the owner or have permission `R_M_O`

## Read-Oriented Endpoints

### `org.list`

- Endpoint: `GET /outer/api/v1/common/user/org/page`
- Purpose: paginated organization list for the current user or another user

### `org.detail`

- Endpoint: `GET /outer/api/v1/common/org/info/detail`
- Purpose: primary detail endpoint from the member-view perspective
- Prefer this endpoint over `org.detail.manage`

### `org.detail.manage`

- Endpoint: `GET /outer/api/v1/common/org/info/basic`
- Purpose: supplemental detail for management scenarios
- Ordinary members may hit permission restrictions in practice

### `org.member.list`

- Endpoint: `GET /outer/api/v1/common/org/member/list`
- Purpose: non-paginated member list, mainly for IM or group-sync style usage

### `org.member.page`

- Endpoint: `GET /outer/api/v1/common/org/member/page`
- Query:
  - `orgId`
  - `page`
  - `count`
  - `mtype`
  - `enablePost`
  - `keyword`
  - `lids`

## `org.join`

- Endpoint: `POST /outer/api/v1/common/voiceroom/member/joinOrg`
- Minimum request body:
  - `orgId`
  - `roomId`, which can be an empty string

## Common CLI Commands

```bash
python scripts/org_skill_cli.py --env test web-config-get
python scripts/org_skill_cli.py --env test org-list --my 1
python scripts/org_skill_cli.py --env test org-detail --org-id 1141
python scripts/org_skill_cli.py --env test org-create --name "Agent Org Demo"
python scripts/org_skill_cli.py --env test org-update --org-id 1141 --info "Updated organization introduction"
python scripts/org_skill_cli.py --env test org-member-page --org-id 1141 --count 10
```

## Code Locations

- Organization controller: `biz-service/.../OrgInfoOuterControllerV1.java`
- Organization DTO: `biz-service/.../OrgDto.java`
- Organization service: `biz-service/.../OrgInfoService.java`
- Web config controller: `biz-service/.../WebConfigController.java`
