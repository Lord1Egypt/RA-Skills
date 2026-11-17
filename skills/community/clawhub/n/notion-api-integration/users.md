# Users, Bots, and People Properties

What a user object contains depends on a capability, not on permissions — which is why "the email field is missing" is a settings problem, not a bug.

## The Calls

```bash
# The integration's own bot user — the cheapest health check in the API
curl 'https://api.notion.com/v1/users/me' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"

# Everyone the integration can see, paginated at 100
curl 'https://api.notion.com/v1/users?page_size=100' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"

# One user by id
curl 'https://api.notion.com/v1/users/USER_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

## Object Types

| `type` | Contains | Note |
|---|---|---|
| `person` | `name`, `avatar_url`, and `person.email` **only with the with-email capability** | The id is the handle everything else uses |
| `bot` | `bot.owner` (a user or the workspace), `bot.workspace_name` on `/users/me` | Your integration is one of these |

Guests appear as `person` objects too, and a guest removed from the workspace can still be referenced by an old `people` value — expect ids that no longer resolve.

## Capabilities Decide the Shape

- Without any user-information capability, user objects come back thin: an id and little else.
- "Read user information without email addresses" gives names but not emails.
- Granting the with-email variant is a real privacy decision — take it deliberately and record the capability set in `## Integrations` (`auth.md`).
- A `people` property value always carries ids regardless of capability; resolving them to names is what needs the capability.

## Writing a People Property

```json
{"Assignee": {"people": [{"object": "user", "id": "USER_ID"}]}}
```

- Ids only. Names and emails are a `validation_error`.
- Build the name → id map once from `/v1/users` and cache it. Doing a lookup per row turns a 4,000-row backfill into 8,000 requests (`bulk.md`).
- Writing replaces the whole list; adding an assignee means read, merge, write (`properties.md`).
- A user id that is not a member of the workspace is rejected, and the message names the property rather than the reason.

## Mentions

A user mention inside rich text is `{"type": "mention", "mention": {"type": "user", "user": {"id": "USER_ID"}}}`. It renders as a live mention and, unlike a `people` property, works in page content and comments (`comments.md`). Notification behaviour is Notion's, not yours to control from the API.

## Where People Belong in the Boxes

Do not copy `/v1/users` output into a memory box: it is workspace directory data, it goes stale, and it is not yours to duplicate.

- **A cached name → id map for a specific job** belongs with that job, in `artifacts/` or in the script, with the date it was built.
- **A person the user actually deals with** — the workspace admin who grants connections, the client whose workspace this is — goes in the shared `~/Clawic/data/contacts/contacts.md`: one row, `name | role | preferred channel | context`, identified by email or handle, updated in place, never a second row for the same person. Match the file's existing columns if it already has different ones, and never rewrite its header. Past 15 people the box becomes one file per person at `~/Clawic/data/contacts/<name>.md` with `contacts.md` as the index; if it already looks like that, follow it.
- Nothing in either place is a credential. An invite link is not a contact detail.
