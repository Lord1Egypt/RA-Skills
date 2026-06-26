---
name: navclaw
description: Smart driving — exhaustive route search, may outperform default navigation. 导航/自驾/极限避堵, dozens of routes. One-tap iOS/Android deep link. Supports 高德/Amap. 智能避堵，极限搜索绕行方案，一键跳转手机导航APP.
version: 1.0.3
icon: 🦀
---

# NavClaw 🦀 - 出行智能导航AI助手 / Smart Driving Navigator

## 概述 / Overview

**智能避堵导航 — 极限搜索数十条路线，可能比官方导航更优。一键跳转手机导航APP（iOS/Android）。**

**Smart congestion-avoidance navigator — exhaustive search of dozens of routes, may outperform default navigation. One-tap deep link to mobile nav apps.**

五阶段流水线规划（广撒网 → 精筛选 → 深加工 → 迭代优化 → 路线固化），导航 APP 通常只返回 2-3 条路线，NavClaw 短时间内探索数十种绕行组合。

5-phase pipeline (Wide Search → Fine Filter → Deep Processing → Iterative Optimization → Route Finalization). While navigation apps typically return 2-3 routes, NavClaw explores dozens of bypass combinations in seconds.

导航平台：目前支持高德，后续扩展更多平台。

Navigation platform: currently supports Amap (高德), more platforms coming soon.

---

**⚠️ 前置条件 / Prerequisites**：需要高德 Web 服务 API Key（免费申请）。获取优先级：

1. 从记忆中查找用户是否已提供过高德 API Key
2. 如果没有，询问用户是否有高德 API Key
3. 如果用户没有，引导获取：[高德开放平台](https://lbs.amap.com/) → 控制台 → 创建应用 → 添加 Key（Web 服务）

拿到 Key 后填入 `config.py` 的 `API_KEY` 字段：

```python
API_KEY = "你的高德API Key"
```

---

**触发方式 / Trigger**：

用户说"从 [起点] 到 [终点] 导航"、"导航从 [起点] 到 [终点]"或"navigate from [A] to [B]"即可自动执行。说"到家"时自动替换为 `config.py` 中的 `DEFAULT_DEST`。

Trigger when user says "navigate from [A] to [B]", "从 [起点] 到 [终点] 导航", or "drive to [destination]". Saying "到家" (go home) auto-substitutes `DEFAULT_DEST` from `config.py`.

---

**工作流程 / Workflow**：

调用 `wrapper.py --origin "起点" --dest "终点"`，经过五阶段规划（广撒网 → 精筛选 → 深加工 → 迭代优化 → 路线固化），生成大量路线方案（含绕行优化），自动发送 3 条消息到聊天平台 + 日志附件：

- 消息 1 — 完整对比表格
- 消息 2 — 快速导航链接
- 消息 3 — 最终推荐 + iOS/Android 一键深度链接

---

**输出格式 / Output**：

- **Mattermost（原生支持，推荐优先使用）**：

  需要先在 `config.py` 中配置 `MM_BASEURL`、`MM_BOT_TOKEN`、`MM_CHANNEL_ID`，然后直接运行 `wrapper.py --origin "起点" --dest "终点"`，自动发送 3 条消息 + 日志附件（优先采用Mattermost 消息和日志附件，如果不成功则用备份方案）。

### Mattermost 发文件附件

OpenClaw Mattermost 插件不支持原生附件，用 curl 直调 API：

1. POST /api/v4/files 上传文件，拿 file_id
2. POST /api/v4/posts 发帖，带 file_ids 字段

- **其他聊天工具（备份方案）**：

  运行 `wrapper.py --origin "起点" --dest "终点" --no-send`，结果输出到 stdout，OpenClaw 读取后转发给用户即可。

  OpenClaw 可读取 stdout 按 `📨 消息 1/2/3` 分段转发给用户。日志文件路径在末尾 `📝 日志: log/navclaw/...` 行中，不要发路径，要读取后发出来，如果不能发附件，给发原文内容。

  （一定要原样发给用户，各个消息，特别是链接要保留，不能舍弃）

**强烈建议先用原生方法 / Native method recommended**

---

**安装配置 / Setup**：

`pip install requests` → `cp config_example.py config.py` → 编辑填入高德 API Key、默认终点、Mattermost 配置（可选，包括MM_BASEURL，MM_BOT_TOKEN，MM_CHANNEL_ID，如果记忆或者配置没有，提示用户给出，如果用户没有就忽略。如果有，要写入config.py对应位置）。

---

**文件位置 / Files**：

- 调用入口：`wrapper.py`
- 核心引擎：`navclaw.py`
- 配置文件：`config.py`（需用户创建）
- 配置模板：`config_example.py`
- 日志目录：`log/`

---

**聊天平台 / Chat Platforms**：

目前内置支持 Mattermost（通过 `wrapper.py`），其他聊天工具 OpenClaw 帮我转发。

最简单的办法是直接聊天告诉 OpenClaw 运行并读取结果发送给你，支持任何聊天平台，稳定性和上下文长度取决于你的大模型 API。如果想节约 token、防止上下文截断、加快响应速度，可以自行扩展 `wrapper.py` 或让 OpenClaw AI 阅读现有 Mattermost 代码帮你适配新平台。

---

**性能参考 / Performance**：

- 短途无拥堵（迭代=0）：约 6 秒、15 次 API、10 条路线
- 长途有拥堵（迭代=1）：约 30 秒、150 次 API、40 条路线

首次使用建议 `MAX_ITER = 0` 验证配置正确，`MAX_ITER = 1` 深度优化可能找到比官方更快的路线。

---

**依赖 / Dependencies**：

- Python 3.8+
- `requests`（唯一第三方依赖）
- 高德 Web 服务 API Key

---

**作者 / Author**：

公益技能，免费开源。 / Community-driven, open-source, free for everyone.

- **Email**: nuaa02@gmail.com
- **小红书 / Xiaohongshu**: @深度连接
- **GitHub**: [AI4MSE](https://github.com/AI4MSE)
