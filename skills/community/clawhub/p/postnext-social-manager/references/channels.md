# Channels (connections)

Channels are connected in the PostNext web app - there is no API to start an OAuth connection. This skill only lists and reads them.

## List connected channels

`GET /api/connections` returns a **bare JSON array** (no envelope). Each item:

```jsonc
{
  "provider": "twitter",           // one of twitter/instagram/linkedin/threads/youtube/tiktok/bluesky
  "channelName": "@yourbrand",     // the connected handle - use this in a post's channelName
  "providerId": "tw_9f3a1c20e5",   // platform-native account id - use this in a post's providerId
  "uniqueId": "...",                 // internal UUID - do NOT use for posting
  "requiresAttention": true,       // true only when a token refresh actually failed (re-auth needed)
  "isActive": true,
  "avatar": "...", "createdAt": "...", "tokenExpiry": "..."
}
```

## Resolving providerId for a post (trap #3)

To post to a channel, pick the connection by matching `provider` (and `channelName` if the user named one), then copy its **`providerId`** and `channelName` into the post entry. Never use `uniqueId` - the publish worker needs the platform-native `providerId` or it fails silently.

```bash
# providerId + channelName for a given provider
curl -sS https://api-app.postnext.io/api/connections -H "x-api-key: $POSTNEXT_API_KEY" \
  | jq -r '.[] | select(.provider=="twitter") | "\(.channelName)\t\(.providerId)"'
```

Use `requiresAttention == true` (not `tokenExpiry`) to decide whether a channel needs the user to re-authenticate in the web app before it can publish.

## Check one channel

`GET /api/connections/{provider}/{channelName}/check` returns a flat status object whose HTTP status mirrors the `status` field: `active` -> 200, `expired` -> 401, `invalid` -> 404.

```jsonc
{ "status": "active", "message": "...", "expiresAt": "..." }
```
