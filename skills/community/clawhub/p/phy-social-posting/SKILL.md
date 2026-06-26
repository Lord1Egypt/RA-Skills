---
name: social-posting
description: Multi-platform social media posting service with automatic provider failover. Handles posting to 9 platforms (Twitter/X, LinkedIn, Instagram, Facebook, TikTok, Threads, Bluesky, YouTube, Pinterest) with per-user credential management, OAuth flow, media upload, scheduling, and post history tracking. Triggers on "post to social media", "publish to platforms", "schedule a post", "social post", or any cross-platform publishing request.
metadata: {"category": "social-media", "platforms": ["twitter", "linkedin", "instagram", "facebook", "tiktok", "threads", "bluesky", "youtube", "pinterest"], "providers": ["PostForMe", "LATE"], "features": ["oauth", "scheduling", "media-upload", "failover", "post-history"]}
---

# Social Posting Skill

Multi-platform social media posting with automatic provider failover. Users connect their own social accounts via OAuth — credentials are encrypted at rest. Supports immediate posting, scheduling, and media attachments.

---

## Supported Platforms

| Platform | Enum Value |
|----------|-----------|
| Twitter / X | `twitter` |
| LinkedIn | `linkedin` |
| Instagram | `instagram` |
| Facebook | `facebook` |
| TikTok | `tiktok` |
| Threads | `threads` |
| Bluesky | `bluesky` |
| YouTube | `youtube` |
| Pinterest | `pinterest` |

---

## Provider Architecture

Two providers with automatic failover:

| Provider | Role | API Base |
|----------|------|----------|
| **PostForMe** | Primary (cheaper) | `https://api.postforme.dev/v1` |
| **LATE** | Fallback (reliable) | `https://getlate.dev/api/v1` |

Failover order:
1. Try user's PostForMe credentials
2. Try user's LATE credentials
3. Fall back to global env-var credentials (PostForMe → LATE)

---

## Core Data Structures

```python
class Platform(Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    THREADS = "threads"
    BLUESKY = "bluesky"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"

@dataclass
class PostResult:
    success: bool
    post_id: Optional[str] = None
    platform_post_ids: Optional[Dict[str, str]] = None
    platform_post_urls: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    provider: Optional[str] = None
    scheduled_for: Optional[datetime] = None

@dataclass
class AccountInfo:
    id: str
    platform: str
    username: str
    profile_id: Optional[str] = None
```

---

## Provider Interface

Both providers implement the same abstract interface:

```python
class SocialPostingProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def get_accounts(self) -> List[AccountInfo]: ...

    @abstractmethod
    def upload_media(self, image_url: str) -> Optional[str]: ...

    @abstractmethod
    def post(
        self,
        content: str,
        platforms: List[str],
        media_urls: Optional[List[str]] = None,
        scheduled_for: Optional[datetime] = None
    ) -> PostResult: ...
```

---

## PostForMe Provider (Primary)

**Authentication:** `Authorization: Bearer {api_key}`

### OAuth URL Generation

```python
POST /social-accounts/auth-url
{
  "platform": "twitter",
  "redirect_url": "https://your-app.com/callback"
}
# Returns: {"url": "..."} or {"data": {"auth_url": "..."}}
```

### Get Connected Accounts

```python
GET /social-accounts
# Returns: {"data": [{"id": "...", "platform": "twitter", "username": "..."}]}
```

### Media Upload (Presigned URL Flow)

```python
# 1. Get presigned URL
POST /media/create-upload-url
{"content_type": "image/jpeg"}
# Returns: {"upload_url": "...", "media_url": "..."}

# 2. PUT image bytes to upload_url
# 3. Use returned media_url in post payload
```

### Create Post

```python
POST /social-posts
{
  "caption": "Post content here",
  "social_accounts": ["account_id_1", "account_id_2"],
  "media": [{"url": "https://..."}],        # optional
  "scheduled_at": "2025-01-01T09:00:00"     # optional ISO datetime
}
# Returns: {"id": "post_id"} or {"data": {"id": "post_id"}}
```

**Note:** PostForMe normalizes `twitter` platform to both `"twitter"` and `"x"` internally.

---

## LATE Provider (Fallback)

**Authentication:** `Authorization: Bearer {api_key}`

### Get Connected Accounts

```python
GET /accounts
# Returns: {"accounts": [{"_id": "...", "platform": "...", "username": "...", "profileId": "..."}]}
```

### Media Upload (Presigned URL Flow)

```python
# 1. Get presigned URL
POST /media/presign
{"filename": "media.jpg", "contentType": "image/jpeg"}
# Returns: {"uploadUrl": "...", "publicUrl": "..."}

# 2. PUT image bytes to uploadUrl (wait 1s for CDN propagation)
# 3. Use publicUrl in post payload
```

### Create Post

```python
POST /posts
{
  "content": "Post content here",
  "platforms": [
    {"platform": "twitter", "accountId": "...", "profileId": "..."}
  ],
  "mediaItems": [{"url": "https://...", "type": "image"}],  # optional
  "scheduledFor": "2025-01-01T09:00:00"                      # optional
}
# Returns: {"post": {"_id": "...", "platforms": [{"platform": "twitter", "platformPostId": "...", "platformPostUrl": "..."}]}}
```

---

## Service Layer (SocialPostingService)

The service layer wraps both providers and adds database integration.

### Environment Variables Required

```bash
# Provider API keys (for global fallback if user has no personal creds)
POSTFORME_API_KEY=your_postforme_key
LATE_API_KEY=your_late_key

# Encryption for stored credentials
ENCRYPTION_KEY=your_fernet_key  # Generate: Fernet.generate_key()
```

### Credential Management

```python
service = SocialPostingService()
service.init(supabase_client)

# Save user credentials
service.save_credentials(
    user_id="user-uuid",
    provider="postforme",  # or "late"
    api_key="sk-...",
    connected_platforms=["twitter", "linkedin"]
)

# Get credentials (auto-decrypted)
creds = service.get_credentials(user_id="user-uuid", provider="postforme")

# Delete credentials
service.delete_credentials(user_id="user-uuid", provider="postforme")
```

Credentials are encrypted using **Fernet symmetric encryption** before database storage. Set `ENCRYPTION_KEY` environment variable to a valid Fernet key.

### OAuth Flow

```python
# Generate OAuth URL for user to connect a platform
oauth_url = service.get_oauth_url(
    user_id="user-uuid",
    platform="twitter",
    redirect_url="https://your-app.com/oauth/callback"
)
# Returns: URL string or None
```

### Posting

```python
# Immediate post
result = service.create_post(
    user_id="user-uuid",
    content="Your post content",
    platforms=["twitter", "linkedin"],
    media_urls=["https://cdn.example.com/image.jpg"],  # optional
    scheduled_for=None,
    campaign_id="campaign-uuid",   # optional, for tracking
    batch_number=1                 # optional, for tracking
)

# Scheduled post
from datetime import datetime, timezone
result = service.create_post(
    user_id="user-uuid",
    content="Scheduled post content",
    platforms=["linkedin"],
    scheduled_for=datetime(2025, 6, 1, 9, 0, 0, tzinfo=timezone.utc)
)

# result.success → bool
# result.post_id → provider post ID
# result.platform_post_ids → {"twitter": "tweet_id", ...}
# result.platform_post_urls → {"twitter": "https://...", ...}
# result.error → error message if failed
# result.provider → "PostForMe" or "LATE"
```

### Publish from Campaign Calendar

```python
result = service.publish_batch(
    user_id="user-uuid",
    campaign_id="campaign-uuid",
    batch_number=3,
    platforms=["twitter", "instagram"],
    media_urls=["https://..."],    # selected images for this batch
    scheduled_for=None             # or datetime for scheduling
)
```

Looks up `campaigns.creative_calendar.batches[n].caption` from database and posts it.

### Account Management

```python
# Get connected platforms for a user
accounts = service.get_connected_accounts(user_id="user-uuid")
# Returns: [{"id": "...", "platform": "twitter", "username": "@handle"}]

# Refresh connected_platforms field in credentials table
service.refresh_connected_platforms(user_id="user-uuid")
```

### Post History

```python
# Get all posts
history = service.get_post_history(user_id="user-uuid", limit=50)

# Filter by status: "posted", "scheduled", "failed"
scheduled = service.get_post_history(user_id="user-uuid", status="scheduled")

# Get single post
post = service.get_post(post_id="post-uuid")
```

---

## Database Schema

### user_social_credentials

```sql
CREATE TABLE user_social_credentials (
    user_id         UUID NOT NULL,
    provider        TEXT NOT NULL,  -- 'postforme' | 'late'
    encrypted_api_key TEXT NOT NULL,
    connected_platforms TEXT[],
    updated_at      TIMESTAMPTZ,
    PRIMARY KEY (user_id, provider)
);
```

### social_posts

```sql
CREATE TABLE social_posts (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id             UUID NOT NULL,
    provider            TEXT,
    provider_post_id    TEXT,
    platforms           TEXT[],
    platform_post_ids   JSONB,
    platform_post_urls  JSONB,
    content             TEXT,
    media_urls          TEXT[],
    scheduled_for       TIMESTAMPTZ,
    posted_at           TIMESTAMPTZ,
    status              TEXT,  -- 'posted' | 'scheduled' | 'failed'
    error_message       TEXT,
    campaign_id         UUID,
    batch_number        INTEGER,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Failover Logic

```
User requests post to platforms X, Y, Z
         ↓
Check: user has PostForMe creds?
    YES → PostForMeProvider(user_key)
    NO  → Check: user has LATE creds?
              YES → LateProvider(user_key)
              NO  → Check: POSTFORME_API_KEY env var?
                        YES → PostForMeProvider(global_key)
                        NO  → Check: LATE_API_KEY env var?
                                  YES → LateProvider(global_key)
                                  NO  → Return error: no credentials configured
         ↓
Call provider.post(content, platforms, media_urls, scheduled_for)
         ↓
Track result in social_posts table
         ↓
Return PostResult
```

---

## Usage Example (Standalone)

```python
import os
from datetime import datetime
from social_posting_service import (
    SocialPostingService,
    PostForMeProvider,
    LateProvider
)

# Option A: Use PostForMe directly
provider = PostForMeProvider(api_key=os.getenv("POSTFORME_API_KEY"))
result = provider.post(
    content="Hello from the API!",
    platforms=["twitter", "linkedin"],
    media_urls=["https://example.com/image.jpg"]
)
print(result.success, result.post_id)

# Option B: Use service with database
from supabase import create_client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

service = SocialPostingService()
service.init(supabase)
result = service.create_post(
    user_id="user-uuid",
    content="Post via service",
    platforms=["twitter"]
)
```

---

## Error Handling

All methods return structured results — they do not raise exceptions to the caller.

| Error Condition | Result |
|-----------------|--------|
| No credentials configured | `PostResult(success=False, error="No social posting credentials configured...")` |
| No connected account for platform | `PostResult(success=False, error="No connected accounts for: [...]")` |
| Provider HTTP error | `PostResult(success=False, error="HTTP 4xx: ...")` |
| Network timeout | `PostResult(success=False, error="...")` |
| DB tracking failure | Logs error, still returns posting result |

---

## Integration Checklist

- [ ] Install `requests`, `cryptography` packages
- [ ] Set `ENCRYPTION_KEY` env var (generate with `Fernet.generate_key()`)
- [ ] Set at least one provider key: `POSTFORME_API_KEY` or `LATE_API_KEY`
- [ ] Create `user_social_credentials` table in database
- [ ] Create `social_posts` table in database
- [ ] Initialize service: `service.init(supabase_client)`
- [ ] Guide users through OAuth flow before first post
