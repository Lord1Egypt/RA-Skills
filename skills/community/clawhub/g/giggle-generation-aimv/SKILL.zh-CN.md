---
name: giggle-generation-aimv
description: "当用户希望创建 AI 音乐视频（MV）时使用此技能——包括根据文字提示生成音乐或使用自定义歌词。触发词：生成 MV、音乐视频、为这首歌做视频、歌词视频、创建 MV、AI 音乐视频、音乐+视频、根据歌词生成视频。"
version: "0.0.10"
license: MIT
requires:
  bins: ["python3 (>=3.6)"]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3 (>=3.6)"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      }
  }
---

简体中文 | [English](./SKILL.md)

# MV Trustee 模式 API 技能

调用 MV trustee 模式 API 运行完整 MV 生成工作流。**项目创建与任务提交在脚本内合并为一步**——只需调用一次 `execute_workflow`；切勿分开调用 create 和 submit。

## ⚠️ 安装前请阅读

**安装前请确认以下内容。** 本技能将：

1. **网络请求** – 调用 Giggle.pro API 生成 MV

**依赖要求**：`python3 (>=3.6)`、`GIGGLE_API_KEY`（系统环境变量）、pip 包：`requests`

> **报错禁止重试**：调用脚本如果出现报错，**禁止重试**。直接将错误信息报告给用户并停止执行。

---

## 首次使用前的配置（必选）

**在执行任何操作前，确认用户已配置 API Key。**

**API Key**：登录 [Giggle.pro](https://giggle.pro/) 并在账号设置中获取 API Key。

**配置方式**：设置系统环境变量 `GIGGLE_API_KEY`
- `export GIGGLE_API_KEY=your_api_key`

**检查步骤**：
1. 确认用户已在系统环境变量中配置 `GIGGLE_API_KEY`
2. 若未配置，**引导用户**：
   > 你好！在使用 MV 生成功能前，需要先配置 API Key。请前往 [Giggle.pro](https://giggle.pro/) 获取 API Key，然后在终端执行 `export GIGGLE_API_KEY=your_api_key`。
3. 等待用户配置后再继续工作流

## 两种音乐生成模式

| 模式 | music_generate_type | 必填参数 | 说明 |
|------|---------------------|-----------------|-------------|
| **提示模式** | `prompt` | prompt、vocal_gender | 用文字描述音乐 |
| **自定义模式** | `custom` | lyrics、style、title | 提供歌词、风格和标题 |

### 所有模式共用参数（必填）

- **reference_image** 或 **reference_image_url**：参考图——至少提供其一（asset_id 或下载 URL）。该字段也支持 base64 编码图片，例如 `"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="`, base64 格式：请直接传递 Base64 编码字符串，勿添加 data:image/xxx;base64前缀
- **aspect**：画幅比例，`16:9` 或 `9:16`
- **scene_description**：视觉场景描述，**默认空**——仅当用户明确提及场景时设置（最多 200 字）
- **subtitle_enabled**：是否启用字幕，**默认 false**

### 模式专属参数

**提示模式**：
- `prompt`：音乐描述（必填）
- `vocal_gender`：人声性别 —— `male` / `female` / `auto`（可选，默认 `auto`）
- `instrumental`：仅乐器（可选，默认 false）

**自定义模式**：
- `lyrics`：歌词内容（必填）
- `style`：音乐风格（必填）
- `title`：歌曲标题（必填）

## 工作流函数

使用 `execute_workflow` 运行完整工作流——**调用一次并等待**。内部处理：创建项目 + 提交任务（合并）→ 轮询进度（每 3 秒）→ 检测并支付待支付项 → 等待完成（最长 1 小时）。

**重要**：
- 切勿分别调用 `create_project` 和 `submit_mv_task`——始终使用 `execute_workflow` 或 `create_and_submit`
- 调用后只需等待函数返回；所有中间步骤均自动处理

### 函数签名

```python
execute_workflow(
    music_generate_type: str,      # 模式：prompt / custom
    aspect: str,                   # 画幅比例：16:9 或 9:16
    project_name: str,             # 项目名称
    reference_image: str = "",     # 参考图 asset_id（与 reference_image_url 二选一）
    reference_image_url: str = "", # 参考图 URL 或 base64（与 reference_image 二选一）
    scene_description: str = "",   # 场景描述，默认空
    subtitle_enabled: bool = False,# 字幕开关，默认 False
    # 提示模式
    prompt: str = "",
    vocal_gender: str = "auto",
    instrumental: bool = False,
    # 自定义模式
    lyrics: str = "",
    style: str = "",
    title: str = "",
)
```

### 参数提取规则

1. **reference_image 与 reference_image_url**：至少需要其一。asset_id 用 `reference_image`，图片链接或 base64 用 `reference_image_url`。
2. **scene_description**：默认空——仅当用户明确提及「场景」「视觉描述」或「视觉风格」时填写。
3. **subtitle_enabled**：默认 False——仅当用户明确要求字幕时设为 True。
4. **aspect**：用户提及竖屏/垂直/9:16 时用 `9:16`；否则默认 `16:9`。
5. **模式选择**：「描述音乐 / 用提示」→ prompt；「这是我的歌词 / 歌词是」→ custom；

### 示例

**提示模式**：
```python
api = MVTrusteeAPI()
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="我的 MV",
    reference_image_url="https://example.com/ref.jpg",
    prompt="轻快流行乐，阳光海滩氛围",
    vocal_gender="female"
)
```

**自定义模式（用户提供歌词）**：
```python
result = api.execute_workflow(
    music_generate_type="custom",
    aspect="9:16",
    project_name="歌词 MV",
    reference_image="asset_xxx",
    lyrics="Verse 1: 春风拂面...",
    style="pop",
    title="春歌"
)
```

**带场景描述**（当用户明确描述场景时）：
```python
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="场景 MV",
    reference_image_url="https://...",
    prompt="电子舞曲",
    scene_description="城市夜景，霓虹闪烁，车流涌动"
)
```

### 提交任务 API 请求示例（提示模式）

提交接口（`/api/v1/trustee_mode/mv/submit`）请求体：

```json
{
  "project_id": "<your-project-id>",
  "music_generate_type": "prompt",
  "prompt": "A cheerful pop song",
  "vocal_gender": "female",
  "instrumental": false,
  "reference_image_url": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUT...(base64 image data)",
  "scene_description": "A romantic beach walk at sunset, waves gently lapping the shore, pink sky gradient",
  "aspect": "16:9",
  "subtitle_enabled": false
}
```

注意：`reference_image`（asset_id）与 `reference_image_url`（链接或 base64）二选一，互斥。

**自定义模式**：

```json
{
  "project_id": "<your-project-id>",
  "music_generate_type": "custom",
  "lyrics": "Verse 1:\nStanding by the sea watching the sunset\nMemories rush in like waves\n\nChorus:\nLet the sea breeze blow away all worries\nIn this golden moment\nWe found each other\n",
  "style": "pop ballad",
  "title": "Seaside Memories",
  "reference_image": "<asset_id>",
  "scene_description": "A couple walking on the beach at dusk, long shadows, orange-red sky gradient",
  "aspect": "9:16",
  "subtitle_enabled": false
}
```

### 查询进度 API 响应示例

查询接口（`/api/v1/trustee_mode/mv/query`）响应（所有步骤已完成）：

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "<response-uuid>",
  "data": {
    "project_id": "<your-project-id>",
    "video_asset": {
      "asset_id": "<asset_id>",
      "download_url": "https://assets.giggle.pro/private/...",
      "thumbnail_url": "https://assets.giggle.pro/private/...",
      "signed_url": "https://assets.giggle.pro/private/...",
      "duration": 0
    },
    "shot_count": 0,
    "current_step": "editor",
    "completed_steps": "music-generate,storyboard,shot,editor",
    "pay_status": "paid",
    "status": "completed",
    "err_msg": "",
    "steps": [...]
  }
}
```

注意：当 `pay_status` 为 `pending` 时，需调用支付接口。当所有 `steps` 完成后，`video_asset.download_url` 会有值——返回完整签名 URL。正确返回格式：
```json
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```
错误（仅未签名 URL）：
```json
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

### 支付 API 请求与响应

支付接口（`/api/v1/trustee_mode/mv/pay`）：

**请求体**：
```json
{
  "project_id": "<your-project-id>"
}
```

**响应**：
```json
{
  "code": 200,
  "msg": "success",
  "uuid": "<response-uuid>",
  "data": {
    "order_id": "<order-id>",
    "price": 580
  }
}
```

### 重试 API 请求示例

当某步骤失败时，引导用户调用重试接口从该步骤恢复：

```json
{
  "project_id": "<your-project-id>",
  "current_step": "shot"
}
```

注意：`current_step` 为重试的步骤名（如 `music-generate`、`storyboard`、`shot`、`editor`）。

### create_and_submit（可选）

若仅需创建项目并提交任务，不等待完成，可使用 `create_and_submit`。**切勿**分别调用 `create_project` 和 `submit_mv_task`：

```python
api = MVTrusteeAPI()
r = api.create_and_submit(
    project_name="我的 MV",
    music_generate_type="prompt",
    aspect="16:9",
    reference_image_url="https://...",
    prompt="轻快流行乐"
)
# 返回 project_id，供后续手动查询/支付
```

### 返回值

成功：
```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "project_id": "...",
        "download_url": "https://...",
        "video_asset": {...},
        "status": "completed"
    }
}
```

失败时返回错误信息。

## 常见问题排查

| 场景 | 原因 | 解决方案 |
|------|------|----------|
| `401 Unauthorized` 或 "invalid API key" | `GIGGLE_API_KEY` 未设置、已过期或不正确 | 前往 [Giggle.pro](https://giggle.pro/) 账号设置确认 Key，重新执行 `export GIGGLE_API_KEY=your_api_key` |
| `429 Too Many Requests` | 超出 API 速率限制 | 等待几分钟后重试；避免短时间内连续提交多个项目 |
| 网络超时 / 连接错误 | 网络不稳定或 API 服务暂时不可用 | 脚本会自动重试最多 5 次（间隔 5 秒）；若仍失败请检查网络连接 |
| `pay_status: pending` | 项目需要支付才能继续 | 工作流函数会自动处理支付；若手动操作，请调用支付接口并传入 `project_id` |
| 任务步骤失败（`status: failed`） | 某个生成步骤（如 `music-generate`、`shot`）出错 | 使用重试接口：`{"project_id": "<your-project-id>", "current_step": "<failed-step>"}` 从失败步骤恢复 |
| 工作流超时（超过 1 小时） | MV 生成耗时过长 | 使用 `project_id` 手动查询进度确认当前状态；若任务卡住请联系客服 |
