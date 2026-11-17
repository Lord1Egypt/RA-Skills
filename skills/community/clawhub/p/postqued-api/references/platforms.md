# Postqued publishing targets

Use these fields inside `publish_content.targets` and approval post targets. MCP publishes use `intent` and `dispatchAt`; approval targets omit them until the approved post is scheduled or published.

## Contents

- [Common fields](#common-fields)
- [TikTok](#tiktok)
- [Instagram](#instagram)
- [Facebook](#facebook)
- [Threads](#threads)
- [LinkedIn](#linkedin)
- [YouTube](#youtube)
- [X or Twitter](#x-or-twitter)
- [Pinterest](#pinterest)
- [Reddit](#reddit)
- [Mastodon](#mastodon)
- [Bluesky](#bluesky)

## Common fields

Direct publish target:

```json
{
  "platform": "instagram",
  "accountId": "ACCOUNT_UUID",
  "intent": "publish",
  "caption": "Caption",
  "dispatchAt": null,
  "options": {}
}
```

- `platform`: one of the 11 values documented below
- `accountId`: UUID returned by `list_accounts`
- `intent`: `draft` or `publish`
- `caption`: required for direct publishing
- `dispatchAt`: offset-bearing ISO timestamp or `null` for immediate dispatch
- `options`: platform-specific object

Approval targets use `platform`, `accountId`, `caption`, optional `linkUrl`, and optional `options`.

Reusable `firstComment` shape:

```json
{ "firstComment": { "text": "First comment text" } }
```

## TikTok

Platform value: `tiktok`

Options:

- `privacyLevel`: `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, or `SELF_ONLY`
- `disableComment`, `disableDuet`, `disableStitch`
- `autoAddMusic`
- `videoCoverTimestampMs`, `photoCoverIndex`
- `commercialContent`, `brandContentToggle`, `brandOrganicToggle`
- `authenticContentConfirmed`
- `maxVideoPostDurationSec`

Call `get_creator_info` immediately before composing the target. Use the creator's returned privacy choices and duration limits. Do not assume public posting is available.

## Instagram

Platform value: `instagram`

Options:

- `postType`: `post`, `reel`, or `story`
- `collaborators`: up to three usernames
- `trialReelGraduationStrategy`: `MANUAL` or `SS_PERFORMANCE`
- `firstComment`
- `crop`: `x`, `y`, optional positive `width`, `height`, `zoom`, numeric or `W:H` `aspect`, and optional focal point
- `audio`: selection token, `music` or `original_sound`, title, artist, optional duration, and 0–100 audio/video volume

Obtain an audio `selectionToken` from `list_instagram_audio`; never invent it.

## Facebook

Platform value: `facebook`

Options:

- `postType`: `text`, `photo`, `video`, `reel`, or `link`
- `link`
- `title`
- `firstComment`

## Threads

Platform value: `threads`

Options:

- `replyControl`: `everyone`, `accounts_you_follow`, or `mentioned_only`
- `firstComment`

## LinkedIn

Platform value: `linkedin`

Options:

- `postType`: `text`, `article`, `image`, or `video`
- `articleUrl`, `articleTitle`, `articleDescription`
- `firstComment`

Use `search_linkedin_companies` when publishing through a connected account that can act for organizations.

## YouTube

Platform value: `youtube`

Options:

- `visibility`: `public`, `unlisted`, or `private`
- `title`, `description`, `categoryId`
- `tags`: up to 30 values
- `madeForKids`
- `containsSyntheticMedia`
- `firstComment`

## X or Twitter

Platform value: `twitter`

Options:

- `replySettings`: `everyone`, `mentionedUsers`, or `following`
- `firstComment`

## Pinterest

Platform value: `pinterest`

Options:

- `boardId`, `boardSectionId`
- `title`, `description`, `link`, `altText`
- `coverImageUrl`
- `isStandard`

Resolve a valid destination with `list_pinterest_boards`; never guess a board ID.

## Reddit

Platform value: `reddit`

`options.subreddit` is required. Other options:

- `kind`: `self`, `link`, `image`, `video`, or `videogif`
- `title`, `text`, `url`
- `flairId`, `flairText`
- `nsfw`, `spoiler`, `sendReplies`, `resubmit`
- `videoPosterUrl`

Use `search_reddit_subreddits`, then `get_reddit_restrictions` for the exact community. Respect allowed post types, title requirements, flair rules, and moderation restrictions.

## Mastodon

Platform value: `mastodon`

Options:

- `visibility`: `public`, `unlisted`, `private`, or `direct`
- `sensitive`
- `spoilerText`
- `language`
- `firstComment`

## Bluesky

Platform value: `bluesky`

The current options object is empty. Use common target fields only.
