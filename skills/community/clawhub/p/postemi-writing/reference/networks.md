# Writing for each network

What tends to work on each network, and what Postemi does there. Postemi's
rules (character limits, required settings, the X rules) come from the
account's schema and the main `postemi` skill; when this file and the schema
disagree, the schema wins.

The networks below are the ones Postemi publishes to today. Pinterest, Google
Business Profile and LinkedIn company pages are coming soon and cannot be
scheduled yet. Never plan posts for a network Postemi does not offer.

## X

- **Shape:** short posts of one idea; a thread for anything with steps or a
  story; a longer single post only when the account's limit allows it (read
  the limit from the schema; never assume the account has a paid tier).
- **Hook:** the first line. In a thread, the first entry must work on its own.
- **Links:** Postemi removes links from X posts and their threads, because X
  charges for every post with a link. Put the user's link in their X bio, or
  tell the user to post a link on X directly. Name sources in words.
- **Allowance:** the account has a monthly number of X posts in Postemi; every
  thread entry counts as one. Check what is left before planning a busy X
  calendar; when it runs out, X posts can only be saved as drafts until it
  resets.
- **One X channel per post.** Two X accounts need two separate posts with
  different text.
- **Media:** text plus a picture or a short video tends to beat text alone.
- **Settings:** who can reply is required (see the main skill).

## LinkedIn

- **Shape:** one post a day at most is plenty; long text with an image, or an
  image carousel (`post_as_images_carousel`), does well. Pure text works when
  the writing is strong.
- **Hook:** the first two or three lines, before "see more". Put the promise
  there, not a greeting.
- **Paragraphs:** one or two sentences each; most people read on a phone.
- **Two kinds of post work together:** insight posts about the user's field
  (most of them) and human posts: a lesson learned the hard way, a funny
  moment, a challenge (about one in three).
- **Comments:** comments are what spreads a post beyond the user's network.
  End with a question that is easy to answer, and remind the user to reply to
  comments in the first hours.
- **Links:** a link in the post can pull people off the feed. A common pattern
  is the post on its own and the link in the first comment; in Postemi that is
  the second entry of `postsAndComments`, which LinkedIn shows as a comment.
- **Today:** personal profiles only; company pages are coming soon.

## Instagram

- **Shape:** the picture or the Reel carries the post. Feed post, carousel,
  Reel or Story (`post_type` is required).
- **Caption:** the first sentence (about 125 characters show) is the hook;
  then two or three useful lines that keep its promise; then one call to
  action (save, share, comment, the link in the bio).
- **Reels:** vertical 9:16 video; the hook in the first one to three seconds;
  on-screen text for people watching without sound.
- **Hashtags:** a few relevant ones; they help people find the post.
- **Links:** captions do not make links clickable; point to the link in the
  bio.

## Threads and Bluesky

- **Shape:** short, conversational posts; threads for longer ideas; replies
  matter. Bluesky's limit is short, so read it from the schema.
- **Links:** allowed.

## Mastodon (beta)

- **Shape:** conversational; people value plain, useful posts and dislike
  marketing tone. About 500 characters on mastodon.social; other servers set
  their own limit (read it from the schema).

## Facebook

- **Shape:** a friendly, local voice; photos and short videos; questions
  people can answer in a word. Links are fine.
- **Comments:** entries after the first are comments in Postemi, useful for a
  link or a follow-up detail.
- **Story:** `post_type: "story"` with a picture or a video.

## TikTok

- **Shape:** the video is the post; the caption adds context and a question.
- **Hook:** the first one to three seconds of the video.
- **Volume:** TikTok accepts about 15 posts per account in 24 hours; spread
  bigger batches over more days.
- **Settings:** privacy and posting method are required.

## YouTube

- **Shape:** a title, a description and the video; Shorts are 9:16.
- **Title:** clear promise, specific, front-load the topic words people
  search for. The thumbnail is the user's.
- **Settings:** a title and a type are required; ask the user about privacy.

## Telegram, Discord, Slack, Google Chat, Microsoft Teams

- **Shape:** messages to a community the user already has. Be direct: what
  is new, why it matters to them, what to do. Discord and Slack need a channel
  id from their `channels` tool.

## WordPress, Ghost, Dev.to, Tumblr (beta)

- **Shape:** the long version: a title that makes a promise, an opening line,
  section headings that tell the story, a takeaway. A title is required on
  WordPress, Ghost and Dev.to.
- **Use:** republish the user's best long posts and threads here as articles,
  so they keep working and can be found by search.

## Pixelfed (beta)

- **Shape:** picture first, like Instagram; a picture is required.
