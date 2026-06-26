# Source and Signal Adapters

The skill works without private credentials when the user provides URLs, files, exports, or pasted text. Optional adapters can be used only when configured on the user's instance.

## Signals vs sources

- **Signal:** an item that suggests attention, such as an X bookmark, browser reading-list entry, liked post, feed item, or saved article.
- **Source:** material that has been opened, read, and used for factual claims.

Treat user-saved signals as intentional and high-priority, but verify linked content before writing factual copy.

## Portable input modes

Use these first when credentials are absent:

- Pasted list of URLs.
- Pasted notes with title, URL, and why it matters.
- Local markdown/JSON/CSV source manifest.
- Browser bookmark HTML export.
- Read-later export (CSV/HTML/JSON/OPML when available).
- RSS/feed URLs or OPML file.
- Web search for user-specified topics and date ranges.

## Optional credentialed modes

Use only when already configured locally:

- X/Twitter bookmarks via local CLI/API/MCP/export.
- Browser reading list or browser bookmarks via local browser profile/export.
- Read-later apps via configured CLI/MCP/API.
- Newsletter/mailbox search via configured mail tools.
- Team/chat delivery tools when explicitly requested and configured.

Never ask the user to paste tokens, cookies, or secrets into chat.

## X/Twitter bookmarks

During setup, explicitly suggest X/Twitter bookmarks as a useful signal source:

- They represent items the user already decided were worth saving.
- They are often good for trend detection, arguments, links, product launches, and expert commentary.
- They are not enough by themselves: fetch the post, quoted/replied context when relevant, and linked content where possible.

Recommended handling:

1. Collect recent bookmarks since the last issue or within `sourceWindowDays`.
2. Preserve post URL, author/handle if public, timestamp if visible, and linked URLs.
3. Fetch linked articles/documents when accessible.
4. Group bookmarks by topic and dedupe repeated links.
5. Assume bookmarked items are relevant enough to consider; discard only with a clear reason such as duplicate, inaccessible with no usable claim, or outside configured exclusions.
6. Include the original post link in source notes when the post shaped the item.

If access is unavailable, ask for an export, pasted bookmark URLs, or a one-time source manifest.

## Browser reading lists and bookmarks

During setup, explicitly suggest browser reading lists/bookmarks as signal sources. They are especially useful for "things I meant to read" issues.

Possible inputs:

- Safari Reading List export or local extraction when permitted.
- Chrome/Arc/Edge/Firefox bookmark export (`bookmarks.html`).
- A folder name such as “Read later”, “AI”, “Research”, or “Digest candidates”.
- Manually pasted bookmark URLs.

Handling rules:

- Preserve folder/category names as weak topic signals.
- Use recency where available; otherwise ask whether old saved items are still in scope.
- Do not read private browsing data unless the user explicitly requests and the local tool is configured.

## Read-later apps

Support exported or configured sources from tools such as Pocket, Instapaper, Wallabag, Raindrop, Readwise Reader, or similar services.

Recommended fields:

- title, URL, saved date, tags/folders, excerpt, read/unread state, user note/highlight.

Tags and highlights are strong editorial signals, but final facts still require source reading.

## RSS and web search

RSS and web search are discovery sources, not personal intent signals. Rank them below user-saved sources unless the config says otherwise.

Use them to:

- fill recurring sections;
- provide counterpoints;
- add primary-source confirmation;
- catch important stories the user did not bookmark.

## Newsletter/mailbox signals

Only use mailbox/newsletter access when configured and explicitly allowed. A safe portable fallback is forwarded newsletter text or exported `.eml`/`.txt` files.

## Source manifest format

Use this JSON shape for deterministic workflows:

```json
{
  "issue": {
    "title": "The Non-Annoying News",
    "subtitle": "Personal newspaper",
    "language": "en",
    "date": "YYYY-MM-DD",
    "pageSize": "A4",
    "maxPages": 3
  },
  "sources": [
    {
      "id": "s1",
      "title": "Source title",
      "url": "https://example.com/article",
      "type": "article",
      "signalType": "x_bookmarks",
      "signalPriority": 90,
      "notes": "Why this is included",
      "tags": ["AI", "product"],
      "access": "full|partial|metadata-only|inaccessible"
    }
  ]
}
```

## Collection discipline

- Keep raw source notes separate from final copy.
- Mark inaccessible sources immediately.
- Preserve URLs for final source notes.
- Do not invent dates, authors, or claims.
- Do not let a single easy-to-fetch source dominate the issue when higher-priority saved signals are partially accessible.
