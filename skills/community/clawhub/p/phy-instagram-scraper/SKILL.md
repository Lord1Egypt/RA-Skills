---
name: instagram-scraper
description: Scrape public Instagram profile data including follower counts, bio, recent posts, and engagement metrics without login or browser. Use when you want to analyze an Instagram account's profile stats and recent content for competitive research or audience intelligence.
metadata: {"requires": ["python3", "httpx"], "env": [], "tags": ["instagram", "social-media", "scraper", "profile", "research"]}
---

# Instagram Public Profile Scraper

Fetches public Instagram profile data using Instagram's internal API. No login required, no browser needed, no Playwright overhead. Returns structured profile stats and recent post data.

## Requirements

```bash
pip install httpx
```

## Usage

```bash
python instagram_scraper.py <username>
python instagram_scraper.py google
python instagram_scraper.py nike
```

## What It Returns

### Profile Data
| Field | Description |
|-------|-------------|
| `id` | Instagram user ID |
| `username` | Handle |
| `full_name` | Display name |
| `biography` | Bio text |
| `external_url` | Link in bio |
| `is_verified` | Blue check status |
| `is_private` | Account privacy |
| `is_business_account` | Business profile flag |
| `business_category_name` | Business category |
| `followers_count` | Follower count |
| `following_count` | Following count |
| `posts_count` | Total post count |
| `profile_pic_url` | HD profile photo URL |

### Recent Posts (up to 12)
| Field | Description |
|-------|-------------|
| `id` | Post ID |
| `shortcode` | Post shortcode |
| `url` | Full post URL |
| `display_url` | Full-resolution image |
| `thumbnail_url` | Thumbnail image |
| `is_video` | Video post flag |
| `caption` | Post caption text |
| `likes_count` | Like count |
| `comments_count` | Comment count |
| `timestamp` | Unix timestamp |

## Output

Results are saved to `./storage/instagram/<username>.json`:

```json
{
  "profile": {
    "username": "google",
    "full_name": "Google",
    "followers_count": 12500000,
    ...
  },
  "recent_posts": [
    {
      "url": "https://www.instagram.com/p/ABC123/",
      "likes_count": 45230,
      "caption": "...",
      ...
    }
  ]
}
```

## Implementation

The scraper uses Instagram's internal web API endpoint (`i.instagram.com/api/v1/users/web_profile_info/`) with a standard browser User-Agent and the public Instagram app ID. This is the same endpoint the Instagram web client calls on first page load.

```python
class InstagramScraper:
    BASE_URL = "https://i.instagram.com/api/v1"
    APP_ID = "936619743392459"  # Public Instagram web app ID

    async def get_profile(self, username: str) -> dict:
        """Fetch a user's public profile data."""
        ...

    def parse_profile(self, raw_data: dict) -> dict:
        """Extract key information from raw profile data."""
        ...

    async def get_recent_posts(self, raw_profile: dict, limit: int = 12) -> list:
        """Extract recent posts from profile data."""
        ...
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: User not found` | Username doesn't exist or is misspelled | Verify the handle |
| `PermissionError: Instagram blocked` | IP rate-limited or flagged | Use a VPN or residential proxy |
| HTTP 401 | Request rejected | Rotate User-Agent or wait before retrying |

## Rate Limiting

- Instagram's internal API is not publicly rate-limited, but aggressive scraping triggers IP blocks.
- Add a 2-5 second delay between requests when scraping multiple accounts.
- Private accounts return only public metadata (follower count, bio) but no posts.

## Limitations

- Only works on public profiles
- Returns up to 12 most recent posts (Instagram's default page size)
- Does not return Stories, Reels metadata beyond what appears in the timeline grid
- Video view counts are not included in the internal API response

## Use Cases

- Competitive analysis: track follower growth over time by running daily
- Influencer vetting: check engagement rate (likes+comments / followers) before partnerships
- Content research: analyze which post formats drive highest engagement for a niche
- Brand monitoring: track competitor posting frequency and content themes
