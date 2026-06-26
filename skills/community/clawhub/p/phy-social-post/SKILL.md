---
name: social-post
description: Post to social media platforms using the multi-provider social posting API. Use when user wants to post to Twitter, LinkedIn, Instagram, Facebook, TikTok, Threads, or Bluesky. Triggers on "post to twitter", "post to instagram", "social media post", "share on linkedin", "publish to social", or any social posting request.
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "📱", "os": ["darwin", "linux"]}}
---

# Social Posting Skill

Post to multiple social media platforms via the unified social posting API with automatic provider fallback.

---

## Setup

**Location:** `[your-project-root]/social-posting-api/`

**Environment:**
```bash
cd [your-project-root]/social-posting-api
source venv/bin/activate
```

**Required env vars in `.env`:**
- `POSTFORME_API_KEY` - Primary provider (PostForMe)
- `LATE_API_KEY` - Fallback provider (LATE)

---

## Quick Commands

### Check Connected Accounts
```python
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()

client = SocialPostingClient()
print("Providers:", client.available_providers)
for acc in client.get_accounts():
    print(f"  {acc.platform}: {acc.username}")
```

### Post Text Only
```python
result = client.post(
    content="Your post content here",
    platforms=["twitter", "linkedin"]
)
print(f"Success: {result.success}, Provider: {result.provider}")
```

### Post with Images
```python
result = client.post(
    content="Check out these photos!",
    platforms=["instagram"],
    media_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
)
```

### Schedule a Post
```python
from datetime import datetime

result = client.post(
    content="Scheduled post",
    platforms=["linkedin"],
    scheduled_for=datetime(2025, 1, 15, 9, 0)  # UTC
)
```

---

## Supported Platforms

| Platform | Text Only | With Media | Notes |
|----------|-----------|------------|-------|
| Twitter/X | ✅ | ✅ | 280 char limit |
| LinkedIn | ✅ | ✅ | Best for professional content |
| Instagram | ❌ | ✅ | **Requires media** |
| Facebook | ✅ | ✅ | |
| TikTok | ❌ | ✅ | Video preferred |
| Threads | ✅ | ✅ | |
| Bluesky | ✅ | ✅ | |
| Pinterest | ❌ | ✅ | Requires media |
| YouTube | ❌ | ✅ | Video only |

---

## Complete Posting Script

```python
#!/usr/bin/env python
"""Post to social media platforms."""

import sys
sys.path.insert(0, '[your-project-root]/social-posting-api')

from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv('[your-project-root]/social-posting-api/.env')

def post_to_social(content: str, platforms: list, media_urls: list = None):
    """Post content to specified platforms."""
    client = SocialPostingClient()

    # Check which platforms are connected
    accounts = client.get_accounts()
    connected = [a.platform for a in accounts]

    # Filter to only connected platforms
    valid_platforms = [p for p in platforms if p in connected]

    if not valid_platforms:
        print(f"No connected accounts for: {platforms}")
        print(f"Connected: {connected}")
        return None

    # Post
    result = client.post(
        content=content,
        platforms=valid_platforms,
        media_urls=media_urls
    )

    if result.success:
        print(f"Posted via {result.provider}")
        print(f"   Post ID: {result.post_id}")
    else:
        print(f"Failed: {result.error}")

    return result

# Example usage
if __name__ == "__main__":
    post_to_social(
        content="Hello from the social posting API!",
        platforms=["instagram"],
        media_urls=["https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080"]
    )
```

---

## Workflow for Posting

### Step 1: Check Connected Accounts

Always check what's connected first:
```bash
cd [your-project-root]/social-posting-api
source venv/bin/activate && python -c "
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()
client = SocialPostingClient()
for acc in client.get_accounts():
    print(f'{acc.platform}: {acc.username}')
"
```

### Step 2: Prepare Content

- **Twitter**: Keep under 280 chars
- **LinkedIn**: Can be longer, professional tone
- **Instagram**: Needs at least 1 image
- **小红书**: Use xiaohongshu-gtm skill for Chinese content

### Step 3: Execute Post

```bash
source venv/bin/activate && python -c "
from social_posting import SocialPostingClient
from dotenv import load_dotenv
load_dotenv()

client = SocialPostingClient()
result = client.post(
    content='''Your content here''',
    platforms=['platform1', 'platform2'],
    media_urls=['https://example.com/image.jpg']  # Optional
)
print(f'Success: {result.success}')
print(f'Provider: {result.provider}')
print(f'Post ID: {result.post_id}')
"
```

---

## Connecting New Accounts

To connect Twitter or other platforms:

### Via PostForMe (Primary)
1. Go to https://postforme.dev/dashboard
2. Click "Connect Account"
3. Select platform and authorize

### Via LATE (Fallback)
1. Go to https://getlate.dev/dashboard
2. Connect social accounts
3. API key in `.env` will auto-detect new accounts

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|---------|
| "No connected accounts" | Platform not linked | Connect via provider dashboard |
| "Instagram requires media" | Text-only post | Add at least 1 image URL |
| "HTTP 401" | Invalid API key | Check `.env` file |
| "All providers failed" | Both providers down | Try again later |

---

## Cross-Posting Strategy

**For open source announcements:**
```python
# Post to developer platforms
result = client.post(
    content="Just open-sourced my multi-provider social posting API!\n\nFeatures:\n- Automatic fallback between providers\n- Supports 9+ platforms\n- Simple Python interface\n\nGitHub: https://github.com/[your-username]/social-posting-api",
    platforms=["twitter", "linkedin"]
)
```

**For visual content:**
```python
# Instagram carousel
result = client.post(
    content="Behind the scenes of building [Your Product]",
    platforms=["instagram"],
    media_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
    ]
)
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
