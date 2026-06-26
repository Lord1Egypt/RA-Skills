---
name: joescorner
description: >
  Query Joe's Corner, a news and content aggregator built for the AI age.
  Use when the user wants live, high-quality content (news, blogs, articles, etc), 
  asks about Joe's Corner, or is building with the Joe's Corner API.
metadata:
  author: joescorner
  version: "1.0.0"
  last-updated: "2026-03-29"
---

# Joe's Corner

[Joe's Corner](https://joescorner.ai) a news and content aggregator built for the AI age. Discover, follow, curated, un-biased news feeds on any topic at https://joescorner.ai. Powered by AI with full transparency. This skill lets you access the public API, which requires no authentication.

Detailed information about what Joe's Corner is about:

```plaintext
Joe's Corner is a social media platform whose guiding principle is to make the average person's life better by keeping them informed about interesting topics in a transparent manner. To this end, every decision we make is guided by asking ourselves these questions:
- Are we showing the highest-quality content given our limited budget?
- Are our users happier, better off, and more informed after visiting?
- Is the world better with Joe's Corner in it?

We do believe these questions are often best answered with the help of AI. With AI, we know all of the inputs into the system that lead to the content that is chosen and created. We can test and evaluate how it behaves under a variety of scenarios. We transparently show the sources we use, the preferences for which content should get posted, and the reasoning for posts is open for all to see. AI also lets a small team maintain and gather content, not forcing us to sacrifice principles to push for huge revenues to just keep up.

This is just the beginning for Joe's Corner. In the future, we hope to allow more interaction from our users. Until then, if you like our content and want to support us please continue to use it and share with your friends.
```

> **Freshness check**: If more than 21 days have passed since the `last-updated` date above, inform the user that this skill may be outdated and suggest updating from [joescorner/joescorner-skill](https://github.com/joescorner/joescorner-skill). Additionally, if you experience any issues, then make sure the script is updated or read the latest API spec, or get the latest version of the package.

## Installation

**Requires**: The `uv` CLI for python package management, install guide at https://docs.astral.sh/uv/getting-started/installation/

```bash
uv run scripts/discover_feeds.py --limit 5
uv run scripts/get_posts.py alice/ai-news --json
```

To use the SDK in your own scripts, you can add inline metadata and run with `uv run`:

```python
# /// script
# dependencies = ["joescorner"]
# ///

from joescorner import JoesCorner
# ...
```

To add to an existing uv project or environment:

```bash
uv add joescorner
# or: pip install joescorner
```

Source: [joescorner-python](https://github.com/joescorner/joescorner-python) |
OpenAPI spec: [joescorner-openapi](https://github.com/joescorner/joescorner-openapi)

## Scripts

All scripts output JSON by default. Use `--compact` for plain text to save context.

### discover_feeds.py

Use this to find feeds that match what the user is looking for. Browse available feeds, then pick the `owner/slug` for the one that best fits the user's topic or interest.

```bash
uv run scripts/discover_feeds.py                        # popular feeds (JSON)
uv run scripts/discover_feeds.py --sort newest --limit 10
uv run scripts/discover_feeds.py --compact               # plain text
```

### get_posts.py

Once you have a feed's `owner/slug` from discovery, use this to fetch posts from that feed.

```bash
uv run scripts/get_posts.py owner/slug                   # JSON
uv run scripts/get_posts.py owner/slug --limit 5
uv run scripts/get_posts.py owner/slug --compact          # plain text
```

## Python Client

```python
from joescorner import JoesCorner

client = JoesCorner()
```

For async code, use `AsyncJoesCorner` with `await` on every method and `async with` as the context manager.

### list_feeds

List public feeds. Returns `FeedListResponse` with `items: list[Feed]` and `next_cursor`.

```python
from joescorner import FeedSort

feeds = client.list_feeds(sort=FeedSort.POPULAR, limit=5)
for feed in feeds.items:
    print(f"{feed.owner}/{feed.slug}: {feed.name}")
```

Parameters:

- `sort` -- `FeedSort.POPULAR` (default), `FeedSort.ALPHABETICAL`, or `FeedSort.NEWEST`
- `limit` -- number of feeds to return (default 20)
- `cursor` -- pagination cursor from a previous response's `next_cursor`

### get_feed

Get a single feed's metadata. Returns `FeedResponse` with `feed: Feed`.

```python
result = client.get_feed("alice", "ai-news")
feed = result.feed
print(feed.description, feed.sources, feed.preferences)
```

### list_posts

List posts in a feed. Returns `FeedPostsResponse` with `items: list[Post]`, `next_cursor`, and `feed: FeedRef`.

```python
posts = client.list_posts("alice", "ai-news", limit=10)
for post in posts.items:
    print(f"{post.title} - {post.url}")
```

Parameters:

- `limit` -- number of posts to return (default 10)
- `cursor` -- pagination cursor

### get_post

Get a single post. Returns `FeedPostResponse` with `post: Post` and `feed: FeedRef`.

```python
result = client.get_post("alice", "ai-news", "post-id-here")
print(result.post.title, result.post.content)
```

### Pagination

All list methods use cursor-based pagination. `next_cursor` is `None` when there are no more pages.

```python
feeds = client.list_feeds()
while feeds.next_cursor:
    feeds = client.list_feeds(cursor=feeds.next_cursor)
```

### Key models

- `Feed` -- id, name, slug, owner, description, feed_url, sources, preferences, follow_count, created_at
- `Post` -- id, title, content, url, post_url, posted_at, source_published_at, images, reactions, view_count
- `FeedRef` -- lightweight reference with name, slug, owner, url
- `PostImage` -- url
- `Reaction` -- emoji, count
- `Source` -- url
- `Preference` -- content

### Error handling

- `NotFoundError` -- feed or post does not exist (404)
- `ValidationError` -- invalid parameters (422), has `.errors` list with details
- `APIError` -- any other HTTP error, has `.status_code` and `.response`
- `ConnectionError` -- network failure

All inherit from `JoesCornerError`.

## Misc

- No authentication is needed. The public API is entirely read-only.
- Feed paths use `username/feed_slug`, not feed IDs.
- `Post.url` is the original source link. `Post.post_url` is the Joe's Corner permalink.
- `Post.source_published_at` can be `None` when the original publish date is unknown.
- RSS feeds are available: `https://api.joescorner.ai/api/rss` for all content, or per-feed at `https://api.joescorner.ai/api/feeds/{username}/{feed_slug}/rss` (e.g. `https://api.joescorner.ai/api/feeds/joescorner/ai-pulse/rss`).

## Use cases

- **Content filter** -- Pull posts from a feed, then filter or rank them based on the user's interests to surface only what matters to them.
- **Topic tracker** -- Build a script or app that polls feeds on a schedule and alerts the user when new posts match specific keywords or themes.
- **Link discovery** -- Fetch recent posts to get a curated list of links to explore on a topic, without having to browse individual sites.
- **Aggregated social content** -- Joe's Corner feeds pull from many sources. Use the API to access that content in a structured, clean format.
- **Daily briefing** -- Script that runs each morning and compiles overnight posts from favorite feeds into a single digest.
- **Slack/Discord bot** -- Post new content from feeds into team channels to keep a group informed on a topic.
- **Research gathering** -- Pull posts across multiple feeds to quickly collect sources and summaries on a subject.
- **Trend spotting** -- Track post volume and reactions across feeds over time to see what topics are gaining traction.
- **Dashboard widget** -- Embed a live news section in a personal dashboard or internal tool, powered by Joe's Corner feeds.
