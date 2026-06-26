# imgur-cli

Imgur API CLI for AI agents. Upload/get/delete images, manage albums. Works with anonymous uploads (Client-ID) or authenticated uploads (OAuth access token). Zero extra deps beyond `requests`.

- Official API: https://apidocs.imgur.com/
- Auth: `IMGUR_CLIENT_ID` (anonymous) **or** `IMGUR_ACCESS_TOKEN` (user-owned)

## Quickstart

```bash
pip install -e .
export IMGUR_CLIENT_ID="<your client id>"
imgur-cli upload ./photo.jpg --title "cat pic" | jq '.link'
```

## Commands

```bash
imgur-cli upload <file-or-url> [--title T] [--description D] [--album HASH]
imgur-cli get <image-hash>
imgur-cli delete <delete-hash-or-id>
imgur-cli album-create [--title T] [--description D] [--privacy public|hidden|secret] [--image ID ...]
imgur-cli album-add <album-hash> --image ID [--image ID ...]
```

All commands print the API response `data` object as indented JSON.

## Why this skill

AI agents that post to Instagram, Discord, Reddit, etc. frequently need a zero-friction image host. Imgur has a simple Client-ID upload flow and generous anonymous quotas — perfect as a hosting primitive for agent pipelines. No other ClawHub skill wraps Imgur directly.

## Environment variables
- `IMGUR_CLIENT_ID` — required for anonymous uploads (get one at https://api.imgur.com/oauth2/addclient)
- `IMGUR_ACCESS_TOKEN` — optional OAuth2 bearer token for uploads to a specific user account

If both are set, `IMGUR_ACCESS_TOKEN` takes precedence.

## Notes
- Anonymous uploads return a `deletehash` — save it if you want to delete later.
- Large files are base64-encoded; keep under Imgur's 10MB image limit.
- API rate limits apply (see Imgur dashboard).

## License
MIT
