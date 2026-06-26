# Activity Reference

## When to Read

- When saving, publishing, canceling, or deleting activities
- When completing a free-ticket activity workflow
- When querying activity detail, search, signup, or signup-list flows
- When generating activity share links

## Related Capabilities

| Capability ID | API | Method |
| --- | --- | --- |
| `activity.save` | `/outer/api/v1/common/activity/save` | `PUT` |
| `activity.publish` | `/outer/api/v1/common/activity/publish` | `POST` |
| `activity.cancel` | `/outer/api/v1/common/activity/cancel` | `PUT` |
| `activity.delete` | `/outer/api/v1/common/activity/delete` | `DELETE` |
| `activity.detail` | `/outer/api/v1/common/activity/detail` | `GET` |
| `activity.search` | `/outer/api/v1/common/activity/search` | `GET` |
| `activity.org.list` | `/outer/api/v1/common/activity/org/ac` | `GET` |
| `activity.user.sign.list` | `/outer/api/v1/common/activity/user/sign/list` | `GET` |
| `activity.sign.list` | `/outer/api/v1/common/activity/sign/signList` | `GET` |
| `activity.signup` | `/outer/api/v1/common/activity/orders/signup` | `POST` |

## `activity.save`

- Endpoint: `PUT /outer/api/v1/common/activity/save`
- Authentication: yes
- Required headers:
  - `Authorization`
  - `x-language`
  - `x-timezone`
- Current minimum key fields:
  - `title`
  - `orgId`
  - `beginTime`
  - `endTime`
  - `venue`
  - `openSign`
  - `richText`
  - `tickets`
- Confirmed constraints:
  - `orgId` cannot be empty
  - `title` cannot be empty
  - at least one ticket is required
  - at least one ticket must have `hiddenTicket=0`
- Key response fields:
  - `data.id`, which is the draft `id` used for publish
  - `data.tickets[]`, which contains ticket `id` values required for signup

## `activity.publish`

- Endpoint: `POST /outer/api/v1/common/activity/publish`
- Minimum request body:
  - `{ "id": <draftId> }`
- Confirmed constraints:
  - `endTime >= current time`
  - `beginTime <= endTime`
  - `publish` first loads the saved draft by `dto.id` and then runs publish validation
  - the current skill supports free tickets only

Understand the publish flow in this order:

1. `activity.save` submits the complete activity draft.
2. Take `data.id` from the response.
3. Pass that draft `id` into `activity.publish`.

## Free-Ticket Minimum Example

```json
{
  "title": "Agent Activity Demo",
  "orgId": 1141,
  "quantity": 30,
  "quantityLimit": 1,
  "beginTime": 1774780022676,
  "endTime": 1774790822676,
  "published": 0,
  "venue": 2,
  "openSignInfo": 0,
  "openSign": 1,
  "customerServices": [],
  "richText": [
    { "insert": "Agent activity for free-ticket workflow verification.\n" }
  ],
  "tickets": [
    {
      "title": "Free Ticket",
      "description": "Agent free-ticket verification",
      "openTicketLimit": 1,
      "ticketLimit": 30,
      "openSalesStart": 0,
      "openSalesEnd": 0,
      "hiddenTicket": 0,
      "status": 1,
      "paid": 0,
      "amount": 0,
      "currency": 1
    }
  ],
  "multipleTicket": 0
}
```

## Other Endpoints

### `activity.cancel`

- Minimum request body: `{ "id": <activityId> }`

### `activity.delete`

- Minimum request body: `{ "id": <activityId> }`

### `activity.detail`

- Query: `id`

### `activity.search`

- Query:
  - `keyword`
  - `page`
  - `pageSize`
  - `nextId`

### `activity.org.list`

- Query:
  - `orgId`
  - `tab`
  - `location`
  - `keyword`
  - `page`
  - `pageSize`
  - `nextId`

### `activity.user.sign.list`

- Queries the activities already joined by the current user.

### `activity.sign.list`

- Queries the signup list for an activity.
- The current account may fail in practice because of permission restrictions.

### `activity.signup`

- Minimum request body should include at least:
  - `id`
  - `tickets[].id`
  - `tickets[].quantity`
- Operational notes:
  - call `join-org` before signup
  - use a separate session file for the attendee agent

## Share Links

Server share-base configuration:

- Production: `https://share.zingup.club/`
- Test and local: `https://test-share.groupoo.net/`

Recommended SSR rule for activity share links:

```text
{shareBase}ssr/shareEvent/{activityId}?id={activityId}&t2=2&t8=ch
```

Additional validation notes:

- The historically verified test link `https://test-web.groupoo.net/ssr/shareEvent/{activityId}?id={activityId}&t2=2&t8=ch` opens successfully.
- Backend email and signup logic also build links with the same `shareEvent` rule.

Code evidence:

- `biz-service/.../ActivityEmailService.java`
- `biz-service/.../ActivitySignUpService.java`
- `biz-config.share.url` in `application-prod.yml`, `application-test.yml`, and `application-local.yml`

## Common CLI Commands

```bash
python scripts/org_skill_cli.py --env test activity-save --json-file activity.json
python scripts/org_skill_cli.py --env test activity-publish --draft-id 5912
python scripts/org_skill_cli.py --env test activity-detail --activity-id 5911
python scripts/org_skill_cli.py --env test activity-search --keyword meetup
```

## Code Locations

- Activity controller: `biz-service/.../ActivityOuterController.java`
- Activity service: `biz-service/.../ActivityInfoService.java`
- Signup service: `biz-service/.../ActivitySignUpService.java`
- Ticket logic: `biz-service/.../ActivityTicketLogic.java`
