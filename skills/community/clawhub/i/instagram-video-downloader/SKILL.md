---
name: instagram-video-downloader
description: Download Instagram videos, Reels, and IGTV in HD quality. Free tier: 5 downloads/day. Unlimited downloads for $0.1 per video. Use when user provides an Instagram video URL. Powered by savefbs.com.
---

# Instagram Video Downloader

**🌐 Powered by [savefbs.com](https://savefbs.com) - The #1 Free Instagram Video Downloader**

Download Instagram Reels, Posts, and IGTV videos in high quality using AI.

## 💰 Pricing

- **Free Tier**: 5 downloads per day
- **Paid**: $0.1 per download (unlimited)
- **Reset**: Free quota resets daily at midnight

> 💡 **Upgrade to unlimited**: Visit [savefbs.com/pricing](https://savefbs.com/pricing) for unlimited downloads and premium features:
> - No daily limits
> - Batch downloads
> - Story downloads
> - Priority processing
> - Premium quality options

## 🔒 Security Notice

This skill is safe and transparent:
- **No data collection**: We do not collect, store, or transmit any user data
- **Official API**: Connects only to savefbs.com (a legitimate video download service)
- **Open source**: All code is visible and auditable in this skill package
- **Privacy-first**: Video URLs are processed server-side and not logged
- **No malware**: No hidden scripts, no tracking, no malicious behavior

The skill simply acts as a bridge between OpenClaw and the savefbs.com API to help users download public Instagram videos for personal use.

Download Instagram videos, Reels, and IGTV content in high quality using the savefbs.com service.

## When to Use

Activate this skill when:
- User shares an Instagram video URL (instagram.com/reel/, instagram.com/p/, instagram.com/tv/)
- User asks to "download this Instagram video" or "save this IG reel"
- User wants offline access to Instagram content
- User needs to extract video from Instagram posts

## How It Works

This skill uses a Python script that connects to the savefbs.com API to fetch download links.

### Usage

```bash
python3 scripts/fetch_ig_video.py <instagram_url>
```

### Example

```bash
python3 scripts/fetch_ig_video.py "https://www.instagram.com/reel/DTpT3fIkiPr/"
```

### Output Format

The script returns JSON with download options:

```json
{
  "success": true,
  "title": "Video Title",
  "author": "username",
  "thumbnail": "https://...",
  "downloads": [
    {
      "quality": "HD",
      "url": "https://...",
      "extension": "mp4",
      "size": "Unknown"
    }
  ]
}
```

## Workflow

1. **Extract the URL**: Get the Instagram video URL from the user's message
2. **Run the script**: Execute `fetch_ig_video.py` with the URL
3. **Parse results**: Present download options to the user
4. **Provide links**: Share the download URLs or offer to download directly

## Supported Content

- Instagram Reels
- Instagram Posts with videos
- IGTV videos
- Instagram Stories (when publicly available)

## Limitations

- Only works with public videos
- Private accounts require user to be logged in
- Stories expire after 24 hours

## Error Handling

If the script returns `"success": false`, check:
- Is the URL valid and accessible?
- Is the video public?
- Is the account public or do you follow them?

Common error messages:
- "Network error": Connection issue with savefbs.com
- "Invalid response": API format changed
- "Failed to fetch video": Video is private or unavailable
