# Provider-Specific Settings

The Mallary CLI supports platform-specific publishing settings through JSON file mode. Different platforms have different options and media rules, so the safest path is to use `mallary posts create --file payload.json` whenever you need `platform_options`.

Provider settings are independent of profiles. Omit `--profile-id` or `profile_id` to use the default profile. Use `mallary profiles list` to find the profile ID for a non-default profile, then pass `--profile-id` in flag mode or `profile_id` in file mode.

## How to Use Provider Settings

### Method 1: Command Line Flags

Use command-line flags for shared fields:

```bash
mallary posts create \
  --message "Your content" \
  --platform facebook \
  --profile-id AbC123xYz90 \
  --media ./launch.png
```

Flag mode covers the common payload only. If you need platform-specific settings like `boardId`, `visibility`, or `post_type`, switch to file mode.

### Method 2: JSON File

```bash
mallary posts create --file post-with-settings.json
```

In the JSON file, specify platform-specific settings under `platform_options`:

```json
{
  "profile_id": "AbC123xYz90",
  "message": "Post content",
  "platforms": ["reddit"],
  "platform_options": {
    "reddit": {
      "post_type": "text",
      "subreddit": "programming"
    }
  }
}
```

## Supported Platforms & Settings

### Reddit (`reddit`)

Settings:

- `post_type` (required): `text`, `link`, or `image`
- `subreddit` or `subredditName` (required): target subreddit name

Example:

```json
{
  "message": "Mallary now supports multi-surface publishing.",
  "platforms": ["reddit"],
  "platform_options": {
    "reddit": {
      "post_type": "text",
      "subreddit": "socialmedia"
    }
  }
}
```

### YouTube (`youtube`)

Settings:

- `post_type`: `regular` or `shorts`
- `title`: optional custom title
- `visibility`: `public`, `unlisted`, or `private`
- `categoryId`: optional YouTube category id
- `madeForKids`: optional boolean
- `thumbnail_url`: optional on the video media item for regular YouTube videos. Use `jpg`, `jpeg`, or `png` up to 2 MB. Recommended: `1280x720` 16:9. Shorts thumbnails are skipped.

Example:

```json
{
  "message": "Watch our latest product walkthrough",
  "platforms": ["youtube"],
  "media": [{ "url": "./walkthrough.mp4", "thumbnail_url": "./walkthrough-cover.jpg" }],
  "platform_options": {
    "youtube": {
      "post_type": "shorts",
      "title": "Mallary walkthrough",
      "visibility": "unlisted",
      "categoryId": "28",
      "madeForKids": false
    }
  }
}
```

### X / Twitter (`x`)

Settings:

- No additional platform-specific payload fields are currently consumed by the public Mallary CLI path

Example:

```json
{
  "message": "Shipping a new feature today.",
  "platforms": ["x"],
  "media": [{ "url": "./launch.png" }]
}
```

### LinkedIn (`linkedin`)

Settings:

- `author_urn` (optional): override the LinkedIn author or organization URN used for publishing

Example:

```json
{
  "message": "Company update from Mallary",
  "platforms": ["linkedin"],
  "media": [{ "url": "./update.png" }],
  "platform_options": {
    "linkedin": {
      "author_urn": "urn:li:organization:123456"
    }
  }
}
```

### Instagram (`instagram`)

Settings:

- `post_type` (required when needed): `feed`, `story`, `reel`, or `carousel`
- `thumbnail_url`: optional on video media items for Instagram video/Reels covers. Use a Mallary-hosted image that matches the video placement.

Example:

```json
{
  "message": "Behind the scenes",
  "platforms": ["instagram"],
  "media": [{ "url": "./reel.mp4", "thumbnail_url": "./reel-cover.jpg" }],
  "platform_options": {
    "instagram": {
      "post_type": "reel"
    }
  }
}
```

### TikTok (`tiktok`)

Settings:

- `post_type`: `video` or `photo`
- `post_mode`: `DIRECT_POST` or `MEDIA_UPLOAD`
- `source`: `FILE_UPLOAD` or `PULL_FROM_URL` for video posts
- `privacy_level`: optional direct-post override
- `disable_comment`
- `disable_duet`
- `disable_stitch`
- `video_cover_timestamp_ms`
- `thumbnail_url` on video media overrides Mallary's timestamp cover behavior. TikTok video posts do not accept arbitrary image thumbnails through Mallary.
- `title`
- `description`
- `auto_add_music`
- `brand_content_toggle`
- `brand_organic_toggle`
- `is_aigc`
- `photo_cover_index`
- `thumbnail_url` on photo media selects the cover only when it exactly matches one of the supplied photo URLs

Example:

```json
{
  "message": "New feature demo",
  "platforms": ["tiktok"],
  "media": [{ "url": "./demo.mp4", "thumbnail_url": "./demo-cover.jpg" }],
  "platform_options": {
    "tiktok": {
      "post_type": "video",
      "post_mode": "DIRECT_POST",
      "source": "FILE_UPLOAD",
      "privacy_level": "FOLLOWER_OF_CREATOR",
      "disable_comment": false,
      "disable_duet": false,
      "disable_stitch": false,
      "video_cover_timestamp_ms": 1000,
      "brand_content_toggle": false,
      "brand_organic_toggle": false,
      "is_aigc": false
    }
  }
}
```

### Facebook (`facebook`)

Settings:

- `post_type`: `feed` or `story`
- `link`: optional destination URL for feed-style link posts
- `pageId`: optional advanced override for a specific connected page
- `thumbnail_url`: optional on video media items. Mallary accepts `jpg`, `jpeg`, or `png` thumbnails up to 10 MB and retries without the thumbnail if Meta rejects it.

Example:

```json
{
  "message": "Read the full announcement",
  "platforms": ["facebook"],
  "platform_options": {
    "facebook": {
      "post_type": "feed",
      "link": "https://mallary.ai/blog"
    }
  }
}
```

### Pinterest (`pinterest`)

Settings:

- `post_type`: `image` or `video`
- `boardId` (required): board id to publish into
- `link`: optional destination URL
- `alt_text`: optional alt text for image pins

Example:

```json
{
  "message": "Product launch",
  "platforms": ["pinterest"],
  "media": [{ "url": "./launch.png" }],
  "platform_options": {
    "pinterest": {
      "post_type": "image",
      "boardId": "920740542650170734",
      "link": "https://mallary.ai/pricing",
      "alt_text": "Mallary pricing page preview"
    }
  }
}
```

### Threads (`threads`)

Settings:

- No additional platform-specific payload fields are currently required for the public CLI path

Example:

```json
{
  "message": "Posting to Threads from Mallary",
  "platforms": ["threads"]
}
```

### Snapchat (`snapchat`)

Settings:

- No additional platform-specific payload fields are currently required for the public CLI path

Example:

```json
{
  "message": "Mallary launch update",
  "platforms": ["snapchat"],
  "media": [{ "url": "./story.mp4" }]
}
```

## Platforms Without Specific Settings

These usually work with the standard Mallary post body alone:

- `x`
- `threads`
- `snapchat`

Alias notes:

- older data may still contain `twitter` as an alias for `x`
- older data may still contain `meta` as an alias for `facebook`

## Using JSON Files for Complex Settings

### Reddit Example

```json
{
  "message": "Mallary now supports agent-friendly workflows.",
  "platforms": ["reddit"],
  "platform_options": {
    "reddit": {
      "post_type": "text",
      "subreddit": "socialmedia"
    }
  }
}
```

Run it with:

```bash
mallary posts create --file ./reddit-post.json
```

### YouTube Example

```json
{
  "message": "Full video description goes here.",
  "platforms": ["youtube"],
  "media": [{ "url": "./launch.mp4" }],
  "platform_options": {
    "youtube": {
      "post_type": "regular",
      "title": "Mallary launch",
      "visibility": "public",
      "madeForKids": false
    }
  }
}
```

### Multi-Platform with Different Settings

```json
{
  "message": "Launch day is here.",
  "platforms": ["facebook", "instagram", "youtube", "pinterest"],
  "media": [{ "url": "./launch.mp4" }],
  "platform_options": {
    "facebook": {
      "post_type": "feed"
    },
    "instagram": {
      "post_type": "reel"
    },
    "youtube": {
      "post_type": "shorts",
      "title": "Launch day",
      "visibility": "public"
    },
    "pinterest": {
      "post_type": "video",
      "boardId": "920740542650170734"
    }
  }
}
```

## Tips

- Use `--file` whenever you need `platform_options`.
- Keep `platform_options` keys aligned with the values in `platforms`.
- Local media paths inside `media[].url` are uploaded automatically by the CLI before the post request is sent.
- Local thumbnail paths inside `media[].thumbnail_url` are also uploaded automatically by the CLI before the post request is sent.
- Remote media URLs must already be hosted on `https://files.mallary.ai/...`.
- Remote thumbnail URLs must also already be hosted on `https://files.mallary.ai/...`.

## Finding Your Platform Name

Use the platform names Mallary expects:

- `facebook`
- `instagram`
- `linkedin`
- `youtube`
- `tiktok`
- `pinterest`
- `reddit`
- `x`
- `threads`
- `snapchat`

In file mode, each `platform_options` key should match the related entry in `platforms`.

## Common Errors

### Missing Platform Options Key

If you specify platform-specific settings, the key must match the platform name:

```json
{
  "platforms": ["reddit"],
  "platform_options": {
    "reddit": {
      "post_type": "text",
      "subreddit": "socialmedia"
    }
  }
}
```

### Wrong Platform Name

```json
// Wrong
"platform_options": { "linkedin-page": { "author_urn": "urn:li:organization:123456" } }

// Correct
"platform_options": { "linkedin": { "author_urn": "urn:li:organization:123456" } }
```

### Invalid Settings for Platform

Examples:

- using `boardId` under `youtube`
- sending Pinterest without `boardId`
- sending TikTok photo posts with unsupported image types

## See Also

- [README.md](./README.md)
- [PROVIDER_SETTINGS_SUMMARY.md](./PROVIDER_SETTINGS_SUMMARY.md)
- [SKILL.md](./SKILL.md)
- `https://docs.mallary.ai/api-reference/endpoint/create#body-platform-options`
