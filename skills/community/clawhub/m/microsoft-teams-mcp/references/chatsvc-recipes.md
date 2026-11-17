# Teams chat-service recipes

All read-only. Paths are relative to the chat-service base
(`https://teams.cloud.microsoft/api/chatsvc/amer/v1`; set
`TEAMS_CHATSVC_REGION` or `TEAMS_CHATSVC_BASE` before sourcing
`teams-env.sh` for another region). Run `source references/teams-env.sh` and
`teams_token_refresh` first.

## List every chat and channel

```sh
teams_get '/users/ME/conversations?view=msnp24Equivalent&pageSize=200' \
  | jq -r '.conversations[]
      | select(.id | startswith("48:") | not)
      | [.id, (.threadProperties.topic // "(untitled)"), (.lastMessage.originalarrivaltime // "")]
      | @tsv'
```

Response: `{ conversations: [...], _metadata: { backwardLink, forwardLink,
syncState, totalCount } }`. For more, pass `_metadata.backwardLink` to
`teams_get_url` until it is absent or a page is empty.

Tell the kinds apart by id suffix:

| suffix | kind |
| --- | --- |
| `@thread.tacv2` | channel (`threadProperties.spaceId` is its team's id) |
| `@thread.v2` | group or meeting chat (`19:meeting_…` ids are meetings) |
| `@unq.gbl.spaces` | 1:1 chat (no topic — name it after the other person) |
| `48:notes` | the user's own notes self-chat — readable and writable like any chat |
| `48:notifications` | the Activity feed — read-only; see [Activity feed](#activity-feed) |
| `48:*` (other) | system thread (calendar, …) — not a chat; skip |

## Which conversations are unread

The conversation listing can only nominate **candidates** — anything that
arrived after the read marker, or a conversation never opened (no marker):

```sh
teams_get '/users/ME/conversations?view=msnp24Equivalent&pageSize=200' \
  | jq -r '.conversations[]
      | select(.id | startswith("48:") | not)
      | select(.memberProperties.interest != "NotInterested")
      | ((.properties.consumptionhorizon // "0") | split(";")[0] | tonumber? // 0) as $read
      | (.properties.lastimreceivedtime // "" | tostring
          | if test("^[0-9]+$") then tonumber
            else (sub("\\.[0-9]+Z$"; "Z") | (fromdateiso8601? // 0) * 1000) end) as $lastIm
      | (.lastMessage.id // "0" | tonumber? // 0) as $last
      | select([$lastIm, $last] | max > $read)
      | [.id, $read, (.threadProperties.topic // .lastMessage.imdisplayname // "(untitled)")] | @tsv'
```

`properties.consumptionhorizon` is `"<lastReadArrivalMs>;<clientMs>;<messageId>"`.
Nothing at the conversation level says whether a REAL message is waiting:
`lastimreceivedtime` moves for a call recording too, and `lastMessage` can be
stale (an old `RichText/Html` while only `Event/Call` / `ThreadActivity/*`
came since). Confirm each candidate by reading its messages past the marker
(next section, stopping at the first message with `id <= $read`) and keep it
only when one is `Text` / `RichText/Html`, has no `properties.deletetime`,
and is not from you (`.from` is a URL ending in the sender's MRI; yours is
`8:orgid:<oid>` from the token's `oid` claim). That matches Teams' badges
exactly — a meeting chat whose only news is its recording is not unread. A
candidate that answers 404 or 403 (a channel that is gone or no longer
readable) is not unread. Channels with `memberProperties.interest ==
"NotInterested"` are hidden in Teams and show no badge; the filter skips them.

## Read one conversation

```sh
CONV='19:example0001@thread.v2'
teams_get "/users/ME/conversations/$(jq -rn --arg v "$CONV" '$v|@uri')/messages?view=msnp24Equivalent|supportsMessageProperties&pageSize=200&startTime=1" \
  | jq -r '.messages
      | map(select(.messagetype == "Text" or .messagetype == "RichText/Html"))
      | reverse[]
      | [.originalarrivaltime, .imdisplayname, (.content | gsub("<[^>]+>"; ""))] | @tsv'
```

The id must be URL-encoded (it contains `:` and `@`). Messages come newest
first; older pages via `_metadata.backwardLink`. Other `messagetype`s
(`ThreadActivity/*`, `Event/Call`, …) are system events. A message whose
`properties.deletetime` is set was deleted.

In a **channel**, a reply's `conversationLink` ends `;messageid=<rootId>`; a
root post's root id is its own `id`. Group by that to rebuild threads.

## Activity feed

The bell icon's feed is the conversation `48:notifications` (the listing
leaves it out — read its messages by id). No view needs to be open:

```sh
teams_get "/users/ME/conversations/48%3Anotifications/messages?view=msnp24Equivalent|supportsMessageProperties&pageSize=200&startTime=1" \
  | jq -r '.messages[]
      | select(.properties.deletetime | not)
      | select(.properties.activity)
      | (.properties.activity | if type == "string" then (fromjson? // null) else . end) as $a
      | select($a)
      | [($a.activityTimestamp // .originalarrivaltime),
         (if .properties.isread == "true" then "read" else "UNREAD" end),
         ($a.activityType + "/" + ($a.activitySubtype // "")),
         ($a.sourceUserImDisplayName // ""),
         ($a.sourceThreadTopic // $a.sourceThreadId),
         (($a.messagePreview // "") | gsub("<[^>]+>"; "") | .[0:120])]
      | @tsv'
```

Each entry's `properties.activity` — a JSON **string** (occasionally already
an object) — says what happened:

| field | meaning |
| --- | --- |
| `activityType` / `activitySubtype` | the kind — see below |
| `activityTimestamp` | when (ISO 8601); fall back to the entry's `originalarrivaltime` |
| `sourceUserImDisplayName` | who did it |
| `sourceThreadId` | the chat or channel it happened in — pass it to *Read one conversation* |
| `sourceMessageId` / `sourceReplyChainId` | the message, and in a channel its thread root |
| `sourceThreadTopic` / `sourceThreadType` | that conversation's title and type |
| `messagePreview` | the message text (may carry HTML) |

`properties.isread` is `"true"` / `"false"`. Kinds seen live:
`mention/channel|person|team`, `mentionInChat/person|everyone`,
`reaction/<key>` and `reactionInChat/<key>` (the key is the emoji, e.g.
`like`), `reply/` and `replyToReply/`,
`msGraph/privateMeetingCreated|Updated|Forwarded|…` (meeting notices) and
`call/missedMeetingNudge`. `48:mentions` holds just the mentions, in the same
shape. Skip entries with `properties.deletetime` (deleted) and the odd one
with no `properties.activity`. Older pages: `_metadata.backwardLink`, as
anywhere. Reading the feed does not mark it read.

## Attachments

Inline images are `<img src="https://us-api.asm.skype.com/v1/objects/<id>/views/imgo">`
in `content` (the host varies by region):

```sh
teams_get_image 'https://us-api.asm.skype.com/v1/objects/<id>/views/imgo' /tmp/image.jpg
```

Shared files are in `properties.files` — a JSON **string**:

```sh
... | jq -r '.messages[] | select(.properties.files) | .properties.files | fromjson[] | [.fileName, .openUrl] | @tsv'
```

They live in SharePoint and **cannot** be downloaded with the chat-service
token (Graph `/shares` → 403, SharePoint direct → 401) — use the `openUrl`.

## Never

Do not `PUT …/properties?name=consumptionhorizon` — that is how Teams marks a
conversation read, and it would clear the user's unread badges.
