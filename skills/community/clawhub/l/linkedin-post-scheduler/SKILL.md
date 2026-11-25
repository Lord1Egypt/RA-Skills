---
name: chime-scheduler
description: Schedule, publish, list, edit or cancel LinkedIn posts on the user's own profile with Chime Scheduler. Use when the user asks to post on LinkedIn, schedule a LinkedIn post for a time ("Tuesday at 9", "tomorrow morning"), see what is scheduled, move or change a post, cancel one, delete a post that is already live, or add images or a video to a post.
---

# Chime Scheduler

Every tool named below comes from Chime Scheduler's hosted MCP server, `https://schedule.getchime.co/mcp`,
which this plugin adds as `chime-scheduler`. Posts go only to the signed-in user's own LinkedIn
profile, never to a company page or anyone else's account.

If the tools are missing or a call says the user is not signed in, the server needs its one-time
sign-in: tell the user to connect or authenticate the `chime-scheduler` MCP server in their app's
MCP settings and sign in with LinkedIn. Do not try to sign in for them.

## When to use

- "Post this on LinkedIn", "schedule this for Tuesday at 9am", "save it as a draft".
- "What do I have scheduled this week?", "did my post go out?"
- "Move my hello post to Friday", "change the first comment", "cancel the Monday post".
- "Add these photos" or "add a video" to a post.

## Times

1. Times are always on the user's own clock. Turn what they say ("tomorrow at 9", "Tuesday
   morning", "in two hours") into `local_datetime` as `YYYY-MM-DDTHH:mm`. Never convert to UTC
   and never add a time zone offset.
2. If you need today's date, the user's local time or their time zone, call `get_status` first.
   Do not guess the date.
3. If the time is vague ("morning", "next week"), pick a sensible time only when the user is happy
   for you to; otherwise ask one short question.
4. After scheduling or editing, repeat the time line from the reply to the user word for word, so
   they can catch a wrong day or hour before anything goes live.

## Scheduling and posting

- Write or polish the text with the user first. Show the final text before you schedule it.
- `schedule_post` with `local_datetime` schedules it; without a time it saves a draft, if the user
  asked for one.
- `post_now` publishes immediately and cannot be undone from here. Ask the user to confirm before
  you call it, unless they have just said in plain words to post it now. If the reply says it is
  still posting, check `get_status` later; do not call `post_now` again.
- Show the user each reply's headline and table as they are.
- Talk about posts by their time and text, never by id. Ids are internal; take them from the
  reply's structured data when you call `edit_post` or `cancel_post`.

## Changing and cancelling

- `edit_post` changes the text, first comment, time or media of a post that has not gone out yet.
  Repeat the new time line back.
- `cancel_post` cancels a scheduled or held post, or deletes a draft. Confirm which post (by time
  and the start of its text) before cancelling. Called on a post that is already live on LinkedIn, it
  deletes that post from LinkedIn. That can't be undone, so ask the user to confirm first, showing the
  post's text and when it went out.
- Held or failed posts never go out on their own, even after a reconnect. Ask the user, then
  `post_now` with that post, `edit_post` with a new time, or `cancel_post`.
- A post marked unconfirmed counts as posted: LinkedIn did not confirm it, so ask the user to check
  their profile. Only if they checked, it is not there, and they ask for it, call `post_now` with
  `confirm_not_on_linkedin: true`.
- If the LinkedIn login has expired, give the user the reconnect link from `get_status`.

## Images and video

1. Call `get_upload_link` and give the user the link. They upload the files in their browser.
2. When they say they have uploaded, call `list_uploads` and show them the file names so they can
   confirm.
3. Pass `media: ["last"]` to `schedule_post` or `edit_post`.

Never invent files, file names, links or upload ids, and never claim an image is attached unless
`list_uploads` shows it. Limits: up to 9 images (JPG, PNG or GIF, 8 MB each) or one MP4 video
(50 MB). PDF carousels are not supported.

## Plain words

Reply in short, plain sentences. Say what happened and when the post goes out, not how the tools
work. Do not mention tool names, ids, UTC or JSON to the user.

## Done when

- The user has seen the final text and the echoed local time for every post scheduled or edited.
- Anything published now was confirmed first, and the user has the live link.
- Nothing was cancelled or posted without the user's say-so.
