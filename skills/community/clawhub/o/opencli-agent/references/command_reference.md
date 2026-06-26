# OpenCLI Command Reference

## General Commands

| Command | Description |
|---------|-------------|
| `opencli list` | List all available commands and adapters |
| `opencli doctor` | Check extension and daemon connectivity |
| `opencli explore <url> --site <name>` | Auto-analyze a website's API and auth strategy |
| `opencli synthesize <site>` | Auto-generate adapter code for a site |
| `opencli register <cli>` | Register a local CLI tool |
| `opencli plugin install github:user/repo` | Install a community plugin |
| `opencli plugin list` | List installed plugins |

## Twitter/X Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli twitter post` | `"<text>"` | Publish a new tweet |
| `opencli twitter reply` | `<tweet_id> "<text>"` | Reply to a tweet |
| `opencli twitter reply-dm` | `<user> "<text>"` | Reply to a DM |
| `opencli twitter like` | `<tweet_id>` | Like a tweet |
| `opencli twitter delete` | `<tweet_id>` | Delete a tweet |
| `opencli twitter search` | `"<keyword>" [--limit N]` | Search tweets |
| `opencli twitter timeline` | `[--limit N]` | View home timeline |
| `opencli twitter trending` | | Get trending topics |
| `opencli twitter profile` | `<username>` | View user profile |
| `opencli twitter follow` | `<username>` | Follow a user |
| `opencli twitter unfollow` | `<username>` | Unfollow a user |
| `opencli twitter block` | `<username>` | Block a user |
| `opencli twitter unblock` | `<username>` | Unblock a user |
| `opencli twitter bookmark` | `<tweet_id>` | Bookmark a tweet |
| `opencli twitter unbookmark` | `<tweet_id>` | Remove bookmark |
| `opencli twitter bookmarks` | `[--limit N]` | List bookmarks |
| `opencli twitter followers` | `<username> [--limit N]` | List followers |
| `opencli twitter following` | `<username> [--limit N]` | List following |
| `opencli twitter likes` | `<username> [--limit N]` | List liked tweets |
| `opencli twitter notifications` | `[--limit N]` | View notifications |
| `opencli twitter thread` | `<tweet_id>` | View a tweet thread |
| `opencli twitter article` | `<url>` | Read a Twitter article |
| `opencli twitter download` | `<tweet_id> [--output DIR]` | Download media |
| `opencli twitter hide-reply` | `<reply_id>` | Hide a reply |

## Reddit Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli reddit hot` | `[--limit N]` | Get hot posts |
| `opencli reddit search` | `"<keyword>" [--limit N]` | Search posts |
| `opencli reddit post` | `<subreddit> "<title>" "<body>"` | Create a post |
| `opencli reddit comment` | `<post_id> "<text>"` | Comment on a post |

## Bilibili Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli bilibili hot` | `[--limit N]` | Get trending videos |
| `opencli bilibili search` | `"<keyword>" [--limit N]` | Search videos |
| `opencli bilibili download` | `<BV_ID> [--output DIR]` | Download a video (requires yt-dlp) |

## Xiaohongshu (小红书) Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli xiaohongshu hot` | `[--limit N]` | Get trending notes |
| `opencli xiaohongshu search` | `"<keyword>" [--limit N]` | Search notes |
| `opencli xiaohongshu download` | `<note_id> [--output DIR]` | Download note (images/videos) |

## Zhihu (知乎) Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli zhihu hot` | `[--limit N]` | Get trending questions |
| `opencli zhihu search` | `"<keyword>" [--limit N]` | Search questions/answers |

## Weibo Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli weibo hot` | `[--limit N]` | Get trending topics |
| `opencli weibo search` | `"<keyword>" [--limit N]` | Search posts |

## YouTube Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli youtube search` | `"<keyword>" [--limit N]` | Search videos |
| `opencli youtube download` | `<video_id> [--output DIR]` | Download a video (requires yt-dlp) |
| `opencli youtube trending` | `[--limit N]` | Get trending videos |

## HackerNews Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli hackernews top` | `[--limit N]` | Get top stories |
| `opencli hackernews new` | `[--limit N]` | Get newest stories |

## Facebook Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli facebook feed` | `[--limit N]` | Get news feed |
| `opencli facebook post` | `"<text>"` | Create a post |

## Instagram Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli instagram feed` | `[--limit N]` | Get feed |
| `opencli instagram profile` | `<username>` | View profile |

## LinkedIn Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli linkedin feed` | `[--limit N]` | Get feed |
| `opencli linkedin profile` | `<username>` | View profile |

## Bluesky Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli bluesky feed` | `[--limit N]` | Get feed |
| `opencli bluesky post` | `"<text>"` | Create a post |

## Douyin (抖音) Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli douyin hot` | `[--limit N]` | Get trending videos |
| `opencli douyin search` | `"<keyword>" [--limit N]` | Search videos |

## Product Hunt Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli producthunt top` | `[--limit N]` | Get top products |

## Desktop App Control (Electron via CDP)

| Command | Arguments | Description |
|---------|-----------|-------------|
| `opencli cursor chat` | `"<message>"` | Send message in Cursor IDE |
| `opencli chatgpt send` | `"<message>"` | Send message to ChatGPT desktop |
| `opencli notion search` | `"<keyword>"` | Search in Notion |
| `opencli discord-app send` | `"<message>"` | Send message in Discord |

## External CLI Hub

OpenCLI can proxy any locally installed CLI. If the tool is not installed, it auto-installs via the system package manager.

| Command | Description |
|---------|-------------|
| `opencli gh <subcommand>` | GitHub CLI |
| `opencli docker <subcommand>` | Docker CLI |
| `opencli obsidian <subcommand>` | Obsidian CLI |
| `opencli vercel <subcommand>` | Vercel CLI |

## Global Options

| Option | Short | Values | Description |
|--------|-------|--------|-------------|
| `--format` | `-f` | `table`, `json`, `yaml`, `md`, `csv` | Output format (default: table) |
| `--limit` | | integer | Limit number of results |
| `-v` | | | Verbose/debug output |
| `--output` | `-o` | path | Output directory for downloads |

## Supported Platforms (Full List)

36kr, antigravity, apple-podcasts, arxiv, band, barchart, bbc, bilibili, bloomberg, bluesky, boss, chaoxing, chatgpt, chatwise, codex, coupang, ctrip, cursor, devto, dictionary, discord-app, douban, doubao-app, doubao, douyin, facebook, google, grok, hackernews, hf (HuggingFace), imdb, instagram, jd, jike, jimeng, linkedin, linux-do, lobsters, medium, notebooklm, notion, ones, paperreview, pixiv, producthunt, reddit, reuters, sinablog, sinafinance, smzdm, spotify, stackoverflow, steam, substack, tieba, tiktok, twitter, v2ex, web, weibo, weixin, weread, wikipedia, xiaohongshu, xiaoyuzhou, xueqiu, yahoo-finance, yollomi, youtube, zhihu, zsxq
