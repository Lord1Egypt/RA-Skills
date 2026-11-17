---
name: "social-postcjo"
description: "Create reviewed posts for Twitter and Farcaster."
---

# Social Post

Prepare, validate, and publish posts for Twitter or Farcaster.

## Safety gate

1. Draft the post.
2. Validate platform limits, links, media paths, and reply targets.
3. Show the exact final text and destinations to the user.
4. Require explicit human approval before any publish or reply action.
5. Publish only the approved payload.
6. Report the resulting post URLs or IDs.

Never expose credentials, private keys, access tokens, or wallet material. Never use an auto-confirm flag. If approval is missing or the payload changes after approval, stop and request approval again.

## Platform checks

- Twitter/X: validate the current platform character limit before publishing.
- Farcaster: validate the current byte limit before publishing.
- Threads: show every segment in order before approval.
- Media: verify that each local file exists and show the attachment list.
- Replies: show the target post URL or ID.

## Dry run

Default to a dry-run preview. A dry run must not publish, reply, upload media, or mutate external state.
