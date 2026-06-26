---
name: hilight-video-generate
description: >-
  电商视频生成技能。通过 MCP（mcporter）调用远程视频生成 API，
  自动为用户生成营销短视频。支持任务创建、进度查询、视频下载。
---

# Hilight Video Generator Skill

## 触发条件

用户出现以下意图时触发：

- 生成视频、制作视频、做视频、创建视频
- 电商视频、营销视频、产品视频、短视频
- video, generate video, marketing video
- 查询视频进度、视频状态
- 下载视频

## 绝对禁止

- **绝对禁止** 在回复中明文输出 API Key。
- **绝对禁止** 把 API Key 写入日志、命令历史、聊天记录中。
- **绝对禁止** 在未实际调用 MCP 的情况下声称"已生成"或"已完成"。
- **绝对禁止** 伪造视频 URL 或任务状态。

## 前置条件

本技能依赖 mcporter 连接本地 MCP server（`http://localhost:10620/mcp`）。

通过 `clawhub install hilight-video-generate` 安装，clawhub hook 自动读取 `clawhub.json` 完成 mcporter 注册与 API Key 配置。

## MCP 可用工具

通过 mcporter 连接的 `hilight-video-generate` MCP server 提供以下工具（tool）：

> 具体工具名和参数以 MCP server 实际暴露为准。以下为典型接口模式。

### 1. 创建视频任务

- **工具**: `create_video` / `generate_video`
- **参数**:
  - `title`：视频标题
  - `description`：视频描述 / 脚本文案
  - `image_url`：商品封面图 URL（可选）
  - `style`：视频风格（可选）
  - `duration`：时长偏好（可选）
- **返回**: `task_id`、初始状态

### 2. 查询任务状态

- **工具**: `get_task_status` / `query_task`
- **参数**:
  - `task_id`：任务 ID
- **返回**: 状态（pending / processing / completed / failed）、进度百分比、预计剩余时间

### 3. 下载 / 获取视频

- **工具**: `get_video` / `download_video`
- **参数**:
  - `task_id`：任务 ID
- **返回**: 视频下载 URL、文件大小、时长

### 4. 列出历史任务

- **工具**: `list_tasks`
- **参数**:
  - `page`：页码（默认 1）
  - `page_size`：每页数量（默认 20）
  - `status`：按状态筛选（可选）
- **返回**: 任务列表

## 执行流程

### 流程 A：生成新视频

```
用户："帮我生成一个 XX 产品的电商视频"
```

1. 确认用户需求（标题、描述、风格）
2. 通过 MCP 调用 `create_video` 工具
3. 拿到 `task_id`，告知用户任务已提交
4. 自动查询一次状态
5. 如果还在处理中，告知预计时间，后续用户可随时问进度

**输出模板**：

```
🎬 视频生成任务已提交！

- 任务 ID：task_abc123  ← 保存此 ID
- 标题：XX 产品营销视频
- 状态：processing（生成中）
- 预计完成：约 3-5 分钟

⏳ 稍后对我说"查一下视频进度"即可获取最新状态。
```

### 流程 B：查询进度

```
用户："查一下视频进度" / "task_abc123 好了吗"
```

1. 通过 MCP 调用 `get_task_status`
2. 返回当前状态

**输出模板（处理中）**：

```
⏳ 任务 task_abc123 状态：processing
   进度：68% ｜ 预计剩余：约 1 分钟
```

**输出模板（已完成）**：

```
✅ 视频已生成完成！

- 任务 ID：task_abc123
- 时长：00:30
- 文件大小：12.5 MB
- 下载链接：https://cdn.example.com/video/abc123.mp4

💡 说"下载这个视频"我帮你保存到本地。
```

### 流程 C：下载视频

```
用户："下载视频 task_abc123"
```

1. 通过 MCP 获取下载 URL
2. 使用 `exec curl` 下载到本地

```bash
exec curl -L -o ~/Downloads/video_task_abc123.mp4 "VIDEO_DOWNLOAD_URL"
```

3. 确认文件大小

```bash
exec ls -lh ~/Downloads/video_task_abc123.mp4
```

**输出模板**：

```
📥 视频已下载！

- 文件：~/Downloads/video_task_abc123.mp4
- 大小：12.5 MB

💡 可以直接用 QuickTime 播放，或拖到剪辑软件中使用。
```

## 错误处理

| 错误码 | 含义 | 处理方式 |
|--------|------|----------|
| 401/403 | API Key 无效或过期 | 提示用户检查 `.env` 文件中的 `VIDEO_API_KEY` |
| 404 | 任务不存在 | 提示检查 task_id 是否正确 |
| 429 | 请求频率限制 | 等待后重试，提示用户稍候 |
| 500+ | 服务端错误 | 告知用户服务暂时不可用，建议稍后重试 |
| MCP 连接失败 | mcporter 未启动或配置错误 | 提示检查 mcporter 状态和 `mcporter.json` 配置 |

## API Key 管理

- **存储位置**: `~/.openclaw/workspace/skills/hilight-video-generate/.env`
- **文件权限**: 600（仅当前用户可读写）
- **更新方式**: 直接编辑 `.env` 文件
- **安全保证**: `.env` 不会被提交到版本控制（gitignore 排除）
