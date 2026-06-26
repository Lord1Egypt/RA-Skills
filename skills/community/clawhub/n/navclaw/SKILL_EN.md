---
name: navclaw
description: Smart driving — exhaustive route search, may outperform default navigation. 导航/自驾/极限避堵, dozens of routes. One-tap iOS/Android deep link. Supports 高德/Amap. 智能避堵导航，极限搜索绕行方案，一键跳转手机导航APP.
version: 1.0.3
icon: 🦀
---

# NavClaw 🦀 - Smart Driving Navigator

## Overview

**Smart congestion-avoidance navigator — exhaustive search of dozens of routes, may outperform default navigation. One-tap deep link to mobile nav apps (iOS/Android).**

5-phase pipeline (Wide Search → Fine Filter → Deep Processing → Iterative Optimization → Route Finalization). While navigation apps typically return 2-3 routes, NavClaw explores dozens of bypass combinations in seconds.

Navigation platform: Currently supports Amap (高德), more platforms coming soon.

---

**⚠️ Prerequisites**:

Requires an Amap Web Services API Key (free to apply). Priority for obtaining the key:

1. Check memory for whether the user has previously provided an Amap API Key
2. If not, ask the user if they have an Amap API Key
3. If the user doesn't have one, guide them to obtain it: [Amap Open Platform](https://lbs.amap.com/) → Console → Create Application → Add Key (Web Services)

Once you have the key, fill it into the `API_KEY` field in `config.py`:

```python
API_KEY = "your_amap_api_key"
```

---

**Trigger**:

User says "navigate from [origin] to [destination]", "from [A] to [B] navigation", or the Chinese equivalents "从 [起点] 到 [终点] 导航".

When user says "go home" (or "到家"), automatically substitute with `DEFAULT_DEST` from `config.py`.

---

**Workflow**:

Calls `wrapper.py --origin "origin" --dest "destination"`, goes through a five-stage planning process (Wide Search → Fine Filter → Deep Processing → Iterative Optimization → Route Finalization), generates a large number of route options (including detour optimizations), and automatically sends 3 messages to the chat platform + log attachment:

- Message 1 — full comparison table
- Message 2 — quick navigation links
- Message 3 — final recommendation + iOS/Android one-tap deep links

---

**Output Format**:

- **Mattermost (native support, recommended as primary)**:

  First configure `MM_BASEURL`, `MM_BOT_TOKEN`, `MM_CHANNEL_ID` in `config.py`, then directly run `wrapper.py --origin "origin" --dest "destination"` to automatically send 3 messages + log attachment (prefer Mattermost messages and log attachments; fall back to backup method if unsuccessful).

### Mattermost File Attachments

The OpenClaw Mattermost plugin does not support native attachments. Use curl to call the API directly:

1. POST /api/v4/files to upload file and get file_id
2. POST /api/v4/posts to create post with file_ids field

- **Other chat tools (backup method)**:

  Run `wrapper.py --origin "origin" --dest "destination" --no-send`, output goes to stdout, and OpenClaw reads and forwards to the user.

  OpenClaw can read stdout and forward to user by splitting at `📨 Message 1/2/3` segments. The log file path is in the final `📝 Log: log/navclaw/...` line — do not send the path, read the file and send its content. If you cannot send attachments, send the raw text content instead.

  (Must forward to user as-is, all messages, especially links must be preserved and not omitted)

**Strongly recommend using native method first**

---

**Installation & Configuration**:

`pip install requests` → `cp config_example.py config.py` → Edit and fill in Amap API Key, default destination, Mattermost configuration (optional, including MM_BASEURL, MM_BOT_TOKEN, MM_CHANNEL_ID — if not found in memory or config, prompt user to provide; if user doesn't have them, skip. If available, write them into the corresponding fields in config.py).

---

**File Locations**:

- Entry point: `wrapper.py`
- Core engine: `navclaw.py`
- Config: `config.py` (user needs to create)
- Template: `config_example.py`
- Logs: `log/`

---

**Chat Platforms**:

Currently has built-in support for Mattermost (via `wrapper.py`); for other chat tools, OpenClaw handles forwarding.

The simplest approach is to directly tell OpenClaw in chat to run the command and read the results to send to you — this works with any chat platform, with stability and context length depending on your LLM API. To save tokens, prevent context truncation, and speed up responses, you can extend `wrapper.py` yourself or have OpenClaw AI read the existing Mattermost code to help you adapt to a new platform.

---

**Performance Reference**:

- Short trips without traffic (iterations=0): ~6 seconds, 15 API calls, 10 routes
- Long trips with traffic (iterations=1): ~30 seconds, 150 API calls, 40 routes

For first-time use, it's recommended to set `MAX_ITER = 0` to verify configuration is correct. `MAX_ITER = 1` enables deep optimization and may find routes faster than the default ones.

---

**Dependencies**:

- Python 3.8+
- `requests` (only third-party dependency)
- Amap Web Services API Key

---

**Author**:

Community-driven, open-source skill — free for everyone.

- **Email**: nuaa02@gmail.com
- **Xiaohongshu (小红书)**: @深度连接
- **GitHub**: [AI4MSE](https://github.com/AI4MSE)
