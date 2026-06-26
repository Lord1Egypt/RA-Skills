---
name: imou-device-video
description: >
  imou / Imou / 乐橙 / lechange 设备视频与录像技能。支持实时预览 live HLS、本地/云录像片段查询、录像回放 HLS。
  Imou/Lechange device video skill for live HLS, local/cloud record clips, and playback HLS.
  Use when: imou live hls, Imou playback hls, lechange video stream, 乐橙 实时预览, 乐橙 录像回放, 乐橙 云录像片段.
metadata:
  openclaw:
    emoji: "📹"
    requires:
      env: ["IMOU_APP_ID", "IMOU_APP_SECRET", "IMOU_BASE_URL"]
      pip: ["requests"]
    primaryEnv: "IMOU_APP_ID"
    install:
      - id: "python-requests"
        kind: "pip"
        package: "requests"
        label: "Install requests"
---

# Imou Device Video（乐橙设备视频）

Get device live HLS URL, local/cloud record clips, and record playback HLS URL by device channel. For OpenClaw download, play, and record.

## Search Aliases

- imou
- Imou
- 乐橙
- lechange
- easy4ip
- imou-device-video
- 乐橙直播
- 乐橙回放
- 乐橙云录像
- 乐橙本地录像

## Quick Start

Install dependency:
```bash
pip install requests
```

Set environment variables (required):
```bash
export IMOU_APP_ID="your_app_id"
export IMOU_APP_SECRET="your_app_secret"
export IMOU_BASE_URL="your_base_url"
```

**API Base URL (IMOU_BASE_URL)** (required; no default—must be set explicitly):
- **Mainland China**: Register a developer account at [open.imou.com](https://open.imou.com) and use the base URL below. Get `appId` and `appSecret` from [App Information](https://open.imou.com/consoleNew/myApp/appInfo).
- **Overseas**: Register a developer account at [open.imoulife.com](https://open.imoulife.com) and use the base URL for your data center (view in [Console - Basic Information - My Information](https://open.imoulife.com/consoleNew/basicInfo/myInfo)). Get `appId` and `appSecret` from [App Information](https://open.imoulife.com/consoleNew/myApp/appInfo). See [Development Specification](https://open.imoulife.com/book/http/develop.html).

| Region         | Data Center     | Base URL |
|----------------|-----------------|----------|
| Mainland China | —               | `https://openapi.lechange.cn` |
| Overseas       | East Asia       | `https://openapi-sg.easy4ip.com:443` |
| Overseas       | Central Europe  | `https://openapi-fk.easy4ip.com:443` |
| Overseas       | Western America | `https://openapi-or.easy4ip.com:443` |

Run:
```bash
# Get live HLS URL for a device channel (creates live if needed; if LV1001, fetches from live list)
python3 {baseDir}/scripts/device_video.py live DEVICE_ID CHANNEL_ID [--stream-id 0|1]

# Get local or cloud record clips in a time range
python3 {baseDir}/scripts/device_video.py record-clips DEVICE_ID CHANNEL_ID --begin "yyyy-MM-dd HH:mm:ss" --end "yyyy-MM-dd HH:mm:ss" [--local|--cloud] [--count 100] [--query-range 1-100]

# Get record playback HLS URL for a time range (local or cloud)
python3 {baseDir}/scripts/device_video.py playback-hls DEVICE_ID CHANNEL_ID --begin "yyyy-MM-dd HH:mm:ss" --end "yyyy-MM-dd HH:mm:ss" --record-type localRecord|cloudRecord [--stream-id 0|1]
```

## Capabilities

1. **Live HLS**: Select device + channel, get real-time preview HLS URL. Supports OpenClaw download, play, record. If bind returns LV1001 (live already exists), the skill queries live list to return the existing HLS URL.
2. **Record clips**: Select device + channel, get local or cloud record clip list in a time range (begin/end).
3. **Playback HLS**: Select device + channel, get HLS URL for a given time range for local or cloud record; supports OpenClaw download, play, record. Playback URL has limited validity—use soon after obtaining.

## Request Header

All requests to Imou Open API include the header `Client-Type: OpenClaw` for platform identification.

## API References

| API | Doc |
|-----|-----|
| Dev spec | https://open.imou.com/document/pages/c20750/ |
| Get accessToken | https://open.imou.com/document/pages/fef620/ |
| Create device live (bindDeviceLive) | https://open.imou.com/document/pages/1bc396/ |
| Create device record HLS | https://open.imou.com/document/pages/185646/ |
| Get live list (liveList) | https://open.imou.com/document/pages/b0e047/ |
| Query local records | https://open.imou.com/document/pages/396dce/ |
| Query cloud records | https://open.imou.com/document/pages/8e0e35/ |

See `references/imou-video-api.md` for request/response formats.

## Tips

- **Token**: Fetched automatically per run; valid 3 days.
- **Live**: Use `--stream-id 0` (main stream) or `1` (sub stream). If API returns LV1001, the script falls back to liveList to find the existing HLS for the same device/channel/streamId.
- **Record clips**: `--local` uses queryLocalRecords (param `count`, max 100; some devices limit to 32). `--cloud` uses queryCloudRecords (param `queryRange` e.g. `1-100`). Paginate by using the last clip’s endTime as next beginTime.
- **Playback HLS**: Time format `yyyy-MM-dd HH:mm:ss`; no cross-day range. Record type `localRecord` or `cloudRecord`. Use the URL promptly; it expires.

## Data Outflow

| Data | Sent to | Purpose |
|------|---------|--------|
| appId, appSecret | Imou Open API | Obtain accessToken |
| accessToken, deviceId, channelId, etc. | Imou Open API | Live, record clips, playback HLS |

All requests go to the configured `IMOU_BASE_URL`. No other third parties.
