---
name: drafting-social-posts
description: "Writes a platform-ready social media post and saves it as a Postify draft for a connected LinkedIn, X (Twitter), Instagram, Facebook, TikTok, or other channel, then suggests posting times. Use when the user asks to 'draft a LinkedIn post about our release', 'write a tweet' or a thread, 'prepare an Instagram caption', 'write a launch announcement', 'turn this into a social post', 'create a post for my channels', or 'when should I post this'. Saves drafts only; never publishes."
---

# Draft a post in Postify

Turn the user's idea into a platform-ready draft saved in Postify. The user reviews it in the Postify composer before anything is scheduled or published.

## Connecting and calling the tools

Every tool in this skill comes from the `postify` MCP server, the Postify connector, and is written here as `postify:<tool>`.

- **Tools listed by name:** call them directly, for example `postify:list_posts`.
- **Only `postify:search_tools` and `postify:execute_typescript` listed (Code Mode, the default):** call `postify:search_tools` first, then call each tool inside `postify:execute_typescript` as `external_<tool>` (for example `external_list_posts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `postify:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Postify and approves that scope.
- **No `postify` tools at all:** Postify is not connected yet. Install the Postify power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `postify:list_channels`: find the channel to target and its platform.
- `postify:search_media_library`: find an image or video the user already uploaded, when the post needs media.
- `postify:suggest_optimal_time`: up to three suggested posting times per platform, computed from this workspace's own publish history.
- `postify:create_draft`: save the post with status `draft`. Returns the new post id.

## Workflow

1. Call `postify:list_channels`. If the user named a platform with more than one connected account, ask which one.
2. Write the copy for that platform:
   - X: under 280 characters, one idea, no hashtag pile.
   - LinkedIn: hook in the first line, short paragraphs, up to three hashtags at the end.
   - Instagram, TikTok: caption first, hashtags on their own line, mention that media is required.
   - Facebook: conversational, a question or call to action at the end.
3. If media is wanted, call `postify:search_media_library` with two or three keywords and offer the matches by name. Do not invent media ids.
4. Show the draft to the user and ask for changes once.
5. Call `postify:create_draft` with the final text, the channel id, and the media id if chosen. Report the post id and that it is saved as a draft.
6. Offer a time: call `postify:suggest_optimal_time` for the platform and present the suggestions. Scheduling itself happens in the Postify composer or through the `managing-content-calendar` skill's reschedule step.

## Rules

- Never call `postify:publish_now`. Drafting is the whole job of this skill.
- Do not fabricate links, statistics, or product claims. Ask for the URL when the post needs one.
- Keep the user's voice. If they pasted earlier posts, match their tone and length.
