# ManyChat access policy

An access policy limits which endpoints ManyChat connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/manychat#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for ManyChat: its 13 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create manychat --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "fb/page/getBotFields"},
    {"method": "GET", "path": "fb/page/getCustomFields"},
    {"method": "GET", "path": "fb/page/getFlows"},
    {"method": "GET", "path": "fb/page/getGrowthTools"},
    {"method": "GET", "path": "fb/page/getInfo"},
    {"method": "GET", "path": "fb/page/getOtnTopics"},
    {"method": "GET", "path": "fb/page/getTags"},
    {"method": "GET", "path": "fb/page/getWidgets"},
    {"method": "GET", "path": "fb/subscriber/findByCustomField"},
    {"method": "GET", "path": "fb/subscriber/findByName"},
    {"method": "GET", "path": "fb/subscriber/findBySystemField"},
    {"method": "GET", "path": "fb/subscriber/getInfo"},
    {"method": "GET", "path": "fb/subscriber/getInfoByUserRef"}
  ],
  "deny": []
}
```

## Endpoints

The ManyChat endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | fb/page/createBotField | write | page | Create bot field. |
| POST | fb/page/createCustomField | write | page | Create custom field. |
| POST | fb/page/createTag | write | page | Create tag. |
| GET | fb/page/getBotFields | read | page | Lists the page bot fields. |
| GET | fb/page/getCustomFields | read | page | Lists the page custom fields. |
| GET | fb/page/getFlows | read | page | Lists the page flows. |
| GET | fb/page/getGrowthTools | read | page | Lists the page growth tools. |
| GET | fb/page/getInfo | read | page | Returns the page info. |
| GET | fb/page/getOtnTopics | read | page | Lists the page OTN topics. |
| GET | fb/page/getTags | read | page | Lists the page tags. |
| GET | fb/page/getWidgets | read | page | Lists the page widgets. |
| POST | fb/page/removeTag | write | page | Remove tag. |
| POST | fb/page/removeTagByName | write | page | Remove tag by name. |
| POST | fb/page/setBotField | write | page | Set bot field. |
| POST | fb/page/setBotFieldByName | write | page | Set bot field by name. |
| POST | fb/page/setBotFields | write | page | Set bot fields. |
| POST | fb/sending/sendContent | write | sending | Send content to subscriber. |
| POST | fb/sending/sendContentByUserRef | write | sending | Send content to user ref. |
| POST | fb/sending/sendFlow | write | sending | Send Automation to subscriber. |
| POST | fb/subscriber/addTag | write | subscriber | Add tag to subscriber. |
| POST | fb/subscriber/addTagByName | write | subscriber | Add tag to subscriber. |
| POST | fb/subscriber/createSubscriber | write | subscriber | Create a Unified subscriber. |
| GET | fb/subscriber/findByCustomField | read | subscriber | Finds subscribers by custom field value. |
| GET | fb/subscriber/findByName | read | subscriber | Finds subscribers by name. |
| GET | fb/subscriber/findBySystemField | read | subscriber | Finds a subscriber by email or phone. |
| GET | fb/subscriber/getInfo | read | subscriber | Returns a subscriber by ID. |
| GET | fb/subscriber/getInfoByUserRef | read | subscriber | Returns a subscriber by user ref. |
| POST | fb/subscriber/removeTag | write | subscriber | Remove tag from subscriber. |
| POST | fb/subscriber/removeTagByName | write | subscriber | Remove tag from subscriber. |
| POST | fb/subscriber/setCustomField | write | subscriber | Set custom field. |
| POST | fb/subscriber/setCustomFieldByName | write | subscriber | Set custom field by name. |
| POST | fb/subscriber/setCustomFields | write | subscriber | Set custom fields. |
| POST | fb/subscriber/updateSubscriber | write | subscriber | Update subscriber. |
| POST | fb/subscriber/verifyBySignedRequest | write | subscriber | Verifies a signed request and returns the subscriber. |
| POST | user/template/generateSingleUseLink | write | templates | Generates a single-use template link. |
