---
name: imou-multimodal-analysis
description: >
  对指定账号下设备通道的实时抓图地址进行AI智能场景分析。AI scene analysis for device channel snapshot URLs under an Imou account.
  支持：人形检测、抽烟检测、玩手机检测、工装检测与离岗检测（需预先配置工装模板）、货架检测、垃圾检测、热力图数据统计、人脸检测；检测目标库的创建/分页查询/删除及库内目标注册/查询/删除。
  Capabilities: human detection, smoking detection, phone-using detection, workwear detection and absence detection (workwear template required), shelf detection, trash detection, heatmap statistics, face analysis; create/list/delete detect repositories and add/list/delete targets in repository.
  Use when: 乐橙/Imou AI分析、人形检测、抽烟检测、玩手机检测、工装离岗检测、货架检测、垃圾检测、热力图、人脸检测、检测目标库、device snapshot AI analysis.
  Requires Imou developer account; set IMOU_APP_ID, IMOU_APP_SECRET, optional IMOU_BASE_URL.
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "env": ["IMOU_APP_ID", "IMOU_APP_SECRET"], "pip": ["requests"] },
        "primaryEnv": "IMOU_APP_ID",
        "install":
          [
            { "id": "python-requests", "kind": "pip", "package": "requests", "label": "Install requests" }
          ]
      }
  }
---

# Imou Multimodal Analysis

AI scene analysis for device channel snapshot URLs (or any image URL) under an Imou account: human detection, smoking detection, phone-using detection, workwear and absence detection (with pre-configured workwear repository), shelf detection, trash detection, heatmap statistics, and face analysis. Also manage detect repositories and targets (create/list/delete repository; add/list/delete targets).

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

**Note**: AI APIs are value-added; apply for access via Imou if needed.

Run analysis on an image URL (e.g. device channel snapshot from live `coverUrl` or any accessible URL):
```bash
# Human detection
python3 {baseDir}/scripts/multimodal_analysis.py analyze HUMAN "https://example.com/snapshot.jpg"

# Smoking detection
python3 {baseDir}/scripts/multimodal_analysis.py analyze SMOKING "https://example.com/snapshot.jpg"

# Phone-using detection
python3 {baseDir}/scripts/multimodal_analysis.py analyze PHONE "https://example.com/snapshot.jpg"

# Workwear detection (optional repositoryId and threshold)
python3 {baseDir}/scripts/multimodal_analysis.py analyze WEAR "https://example.com/snapshot.jpg" [--repository-id REPO_ID] [--threshold 0.8]

# Absence detection (requires workwear repositoryId)
python3 {baseDir}/scripts/multimodal_analysis.py analyze ABSENCE "https://example.com/snapshot.jpg" --repository-id REPO_ID [--threshold 0.8]

# Shelf detection
python3 {baseDir}/scripts/multimodal_analysis.py analyze SHELF "https://example.com/snapshot.jpg"

# Trash detection
python3 {baseDir}/scripts/multimodal_analysis.py analyze TRASH "https://example.com/snapshot.jpg"

# Heatmap (threshold required; optional exclude repository IDs)
python3 {baseDir}/scripts/multimodal_analysis.py analyze HEATMAP "https://example.com/snapshot.jpg" --threshold 0.8 [--exclude-repos ID1,ID2]

# Face analysis
python3 {baseDir}/scripts/multimodal_analysis.py analyze FACE "https://example.com/snapshot.jpg"
```

Repository and target management:
```bash
# Create detect repository (face | human for workwear)
python3 {baseDir}/scripts/multimodal_analysis.py repo create "MyWorkwearLib" human

# List repositories (paginated)
python3 {baseDir}/scripts/multimodal_analysis.py repo list [--page 1] [--page-size 20]

# Delete repository
python3 {baseDir}/scripts/multimodal_analysis.py repo delete REPOSITORY_ID

# Add target to repository (image URL or base64 type)
python3 {baseDir}/scripts/multimodal_analysis.py target add REPOSITORY_ID "TargetName" "https://image.url" [--type url]
python3 {baseDir}/scripts/multimodal_analysis.py target add REPOSITORY_ID "TargetName" "BASE64_DATA" --type base64

# List targets in repository
python3 {baseDir}/scripts/multimodal_analysis.py target list REPOSITORY_ID [--page 1] [--page-size 20]

# Delete target from repository
python3 {baseDir}/scripts/multimodal_analysis.py target delete REPOSITORY_ID TARGET_ID
```

## Capabilities

1. **Human detection**: Detect whether the image contains human figure(s).
2. **Smoking detection**: Detect whether someone is smoking in the image.
3. **Phone-using detection**: Detect whether someone is using a phone.
4. **Workwear detection**: Detect whether personnel are in compliance with workwear (optional workwear repository and threshold).
5. **Absence detection**: Detect absence from post (requires pre-configured workwear repository).
6. **Shelf detection**: Detect shelf status (e.g. empty/full).
7. **Trash detection**: Detect trash overflow.
8. **Heatmap**: Get heatmap statistics for regions (threshold required; optional exclude repository IDs to filter by workwear).
9. **Face analysis**: Face detection/analysis.
10. **Detect repository**: Create (face/human), list by page, delete.
11. **Target in repository**: Add (URL or Base64), list by page, delete.

## Request Header

All requests to Imou Open API must include the header `Client-Type: OpenClaw` for platform identification.

## API References

| API | Doc |
|-----|-----|
| AI overview | https://open.imou.com/document/pages/f1b9a3/ |
| Dev spec | https://open.imou.com/document/pages/c20750/ |
| Get accessToken | https://open.imou.com/document/pages/fef620/ |
| humanDetect | https://open.imou.com/document/pages/93rflk/ |
| smokingDetect | https://open.imou.com/document/pages/kf70sq/ |
| phoneUsingDetect | https://open.imou.com/document/pages/jf78o9/ |
| workwearDetect | https://open.imou.com/document/pages/2jisd8/ |
| absenceDetect | https://open.imou.com/document/pages/29dicv/ |
| shelfStatusDetect | https://open.imou.com/document/pages/2oud87/ |
| trashOverflowDetect | https://open.imou.com/document/pages/cdmfd6/ |
| heatmapDetect | https://open.imou.com/document/pages/fdjfg9/ |
| faceAnalysis | https://open.imou.com/document/pages/28d7ug/ |
| createAiDetectRepository | https://open.imou.com/document/pages/34ff11/ |
| listAiDetectRepositoryByPage | https://open.imou.com/document/pages/5e8222/ |
| deleteAiDetectRepository | https://open.imou.com/document/pages/5esi8a/ |
| addAiDetectTarget | https://open.imou.com/document/pages/ikdf78/ |
| listAiDetectTarget | https://open.imou.com/document/pages/278dkj/ |
| deleteAiDetectTarget | https://open.imou.com/document/pages/odty82/ |

See `references/imou-ai-api.md` for request/response formats.

## Tips

- **Token**: Fetched automatically per run; valid 3 days. Do not cache across runs unless you implement expiry handling.
- **Image input**: Use `type` "0" for image URL, "1" for Base64. Snapshot URL can be device channel live cover URL (e.g. from imou-open-device-video skill `liveList` / `bindDeviceLive` streams[].coverUrl) or any accessible image URL.
- **Workwear / Absence**: Create a human-type repository first, add workwear target images, then pass `repositoryId` to workwearDetect and absenceDetect.
- **Heatmap**: `threshold` in (0,1]. Use `excludeRepositoryIds` to exclude matched workwear persons (e.g. staff) and count only valid customers.
- **detectRegion**: Optional; up to 3 regions, each 3–6 points (normalized 0–1). Omit to analyze full image.

## Data Outflow

| Data | Sent to | Purpose |
|------|---------|--------|
| appId, appSecret | Imou Open API | Obtain accessToken |
| accessToken, image URL or Base64, repositoryId, threshold, etc. | Imou Open API | AI detection and repository/target management |

All requests go to the configured `IMOU_BASE_URL`. No other third parties.
