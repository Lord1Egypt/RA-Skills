---
name: md-to-twitter
description: >
  Convert a Markdown article into an X (Twitter) thread, and optionally post it
  with its images attached. X renders no rich text and cannot carry an image in a
  paste, so the equivalent of a "paste payload" is a numbered thread script plus
  an API path that uploads each image and posts the thread in order. Counting
  follows X's weighted rules: 1 per character, 2 for CJK and emoji, 23 per URL.
  Use when the user wants to publish a markdown draft to X or Twitter, asks for a
  thread, asks how to get an article's images onto X, or wants a long article
  turned into posts.
---

# Skill: md-to-twitter

# md-to-twitter — Markdown into an X thread

X is the least file-friendly of the three targets. It renders no bold, no headings, no tables, no code blocks, and it has no way to carry an image in a paste — an image reaches X only by upload. So there is no "single file with the pictures in it" for X. The equivalent is a **thread script** you can copy from, plus `--post`, which uploads the images and posts the thread for you.

Policy: **degrade the formatting, keep the words.** Markers are stripped, links survive as text plus URL, and images become attachments on the post that mentions them. A long article becomes a long thread, and the script says how long.

## Run it

```sh
scripts/md2twitter.py docs/261111-skill-vs-mcp.md
```

From the repo root, prefix the skill directory: `.opencode/skills/md-to-twitter/scripts/md2twitter.py`. The bare `scripts/…` form assumes the skill directory is the working directory.

Output: `docs/261111-skill-vs-mcp-twitter.txt`, a numbered thread. Each post is separated by `---`, and any image the post carries is listed under it.

```
posts:   64  (1 image(s))
  1. 236 chars
  2. 154 chars
  ...
  4. 264 chars  images: 261111-skill-vs-mcp.png
```

`--print` sends the thread to stdout instead of a file.

## Posting it

```sh
scripts/md2twitter.py docs/261111-skill-vs-mcp.md --post
```

This uploads each image, then posts the thread in order, chaining each post as a reply to the one before. It prints the URL of every post as it goes. `--dry-run` shows what would be sent without touching the network.

Credentials come from the environment, or from `~/.config/md-to-twitter/keys.json`:

```sh
export X_CONSUMER_KEY=...
export X_CONSUMER_SECRET=...
export X_ACCESS_TOKEN=...
export X_ACCESS_TOKEN_SECRET=...
```

```json
{"consumer_key": "...", "consumer_secret": "...",
 "access_token": "...", "access_token_secret": "..."}
```

Signing is OAuth 1.0a HMAC-SHA1. Neither the JSON body nor the multipart body is signed, because OAuth 1.0a signs only the query and form parameters — which is what makes the same header work for both endpoints.

## Modes

| flag | what it does |
| --- | --- |
| *(default)* | thread at 280 weighted characters |
| `--limit N` | custom ceiling; `--limit 25000` produces a single long post |
| `--number` | prefix each post with `n/N` |
| `--at N` | act on post N only: print it, or with `--post`, send just that one |
| `--reply-to ID` | chain this post under an existing tweet |
| `--code image` | screenshot each code block to PNG and attach it |
| `--tables image` | screenshot each table to PNG and attach it |
| `--image-dir DIR` | where block PNGs go (default `imgs/twitter-blocks/` beside a `docs/` article) |

## Code and tables

X renders no code block and no table in a long post. The default flattens both to text: code keeps its words and stays copyable, tables become `a | b | c` rows.

If a table's grid matters, `--tables image` screenshots it to PNG and attaches it. If code's *look* matters more than its copyability, `--code image` does the same for code — but then the code is a picture, not text you can copy. That trade is usually not worth it: code is meant to be copied.

```sh
md2twitter.py docs/<article>.md --limit 25000 --tables image
```

For this article — one infographic and two tables — that is a single long post with three images. Code stays text.

**Native code blocks need X Articles.** A long post has no code frame. X Articles (Premium) does: its Insert menu has Code and Table, and each is an atomic block. The paste path fills prose, headings, quotes and lists; code and tables go in through the menu or a browser skill. This skill targets long posts and threads, where code can only be text or a picture.


## One at a time

`--post` sends the whole thread in one run. `--at N --post` sends exactly one post, and prints the command for the next:

```sh
md2twitter.py docs/<article>.md --at 1 --post
# posted 1/66: https://x.com/i/status/…
# next: --at 2 --post --reply-to 1234567890

md2twitter.py docs/<article>.md --at 2 --post --reply-to 1234567890
```

Each command uploads that post's images, posts it as a reply to the id you pass, and hands back the next command with the new id filled in. Nothing is remembered between runs — the tweet id is the state, which is why it is printed rather than stored.

`--at N` without `--post` prints just that post, for a manual copy:

```sh
md2twitter.py docs/<article>.md --at 4
```

`--limit 25000` is the Premium path: one long post up to 25,000 characters. It is the closest thing to the LinkedIn and Medium shape, and the only way a 2,300-word article arrives as one piece. Without Premium, 280 is the ceiling and the article becomes a long thread.

## What a long article costs

A 2,300-word article is about 13,500 characters, so at 280 per post it becomes **64 posts**. That is arithmetic, not a bug. A thread that long is rarely read end to end, so pick deliberately:

- **Premium** — `--limit 25000`, one post, four images at most.
- **Free** — accept the long thread, or write a shorter summary by hand and post the article link in the first post.
- **Neither** — the thread file is still a good scaffold: cut it down to the opening posts and append the article URL.

The script does not summarise. Condensing 13,500 characters into a readable thread is an editorial decision, and a converter that quietly dropped paragraphs would be worse than one that reports 64.

## Limits it enforces

| limit | value |
| --- | --- |
| characters per post | 280 weighted (274 when `--number` reserves room) |
| images per post | 4 |
| image size | 5 MB |
| image types | png, jpeg, webp, gif |

Weighted counting follows X's rules: most characters cost 1, CJK and emoji cost 2, and every URL costs 23 however long it is. A Chinese article therefore produces roughly twice as many posts as the same article in English.

## Known edges

- **Local images only.** A relative image path is resolved against the article's folder. A remote `http(s)` image is skipped, because X needs the bytes and this script does not download them. A `data:` URI is skipped too — it cannot be uploaded.
- **No formatting.** Bold, italics, headings and code markers are stripped. Backticks are kept around inline code, because they read as code in plain text.
- **Tables flatten.** A row becomes `a | b | c`, one line per row. X draws no table in a long post. `--tables image` screenshots each table instead, at the cost of four images per post.
- **Code stays text.** A fenced block becomes its lines, indented and copyable. `--code image` screenshots it instead, but then the code cannot be copied — the reason to prefer text unless the code's look is the point.
- **Frontmatter is dropped.** A leading `---` block is not posted.
- **The API path is untested against the live service.** The endpoints, the OAuth header and the multipart upload follow the published v2 API, but no credentials existed on this machine when it was written. The converter, the counting, the splitting, the dry run and the oversize refusal are all tested; the network calls are not. If a media upload is rejected, the first thing to check is whether the app has write permission and whether the account is allowed to post.
- **A failed post stops the thread.** The script prints the last id it posted and the `--reply-to` command to resume from there. It does not retry, because a retry after a partial failure is how duplicate posts happen.

## Relationship to the sibling skills

| | md-to-linkedin | md-to-medium | md-to-twitter |
| --- | --- | --- | --- |
| output | HTML paste payload | HTML paste payload | thread text |
| images | base64, inlined | hosted URL | uploaded by API |
| formatting | kept | kept | stripped |
| tables | PNG | PNG | flattened, or PNG with `--tables image` |
| delivery | paste | paste | `--post` or copy |

The first two produce a file you paste. X cannot take that file, so this one produces a script and, with credentials, sends it.
