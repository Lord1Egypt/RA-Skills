---
name: giggle-generation-drama
description: "当用户希望生成视频、拍摄短片或查看可用视频风格时使用此技能。触发词：短片、制作视频、拍短片、AI视频、根据故事生成视频、拍视频、我有故事想法、短剧、解说视频、电影感视频、有哪些视频风格。"
version: "0.0.10"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      }
  }
---

简体中文 | [English](./SKILL.md)

## ⚠️ 安装前请阅读

**安装前请确认以下内容。** 本技能将：

1. **网络请求** – 调用 Giggle.pro API 生成视频

**依赖要求**：`python3`、`GIGGLE_API_KEY`（系统环境变量）、pip 包：`requests`

> **报错禁止重试**：调用脚本如果出现报错，**禁止重试**。直接将错误信息报告给用户并停止执行。

---

## 首次使用前的配置（必选）

在执行任何操作前，确认用户已配置 API Key，以免工作流因认证失败而中断。

- **API Key**：登录 [Giggle.pro](https://giggle.pro/) 并在账号设置中获取 API Key。
- **配置方式**：设置系统环境变量 `GIGGLE_API_KEY`
  - `export GIGGLE_API_KEY=your_api_key`

**检查步骤**：

1. 确认用户已在系统环境变量中配置 `GIGGLE_API_KEY`。
2. 若未配置，**引导用户**：
   > 你好！在使用视频生成功能前，需要先配置 API Key。请前往 [Giggle.pro](https://giggle.pro/) 获取 API Key，然后在终端执行 `export GIGGLE_API_KEY=your_api_key`。
3. 等待用户配置后再继续工作流。

## 生成模式

支持三种模式。**在启动工作流前请用户选择模式**；若用户未指定，默认使用**剧集模式**（`director`）。

| 模式 | project_type | 说明 |
|------|-------------|-------------|
| **剧集** | `director` | AI 导演分镜与镜头语言的短剧 |
| **解说** | `narration` | 以旁白为核心的解说类视频 |
| **短片** | `short-film` | 故事与视觉兼顾的电影感短片 |

## 主工作流：execute_workflow

使用 `execute_workflow` 一次性运行完整工作流：提交任务 + 轮询 + 自动支付（如需要）+ 等待完成。只需调用一次并等待返回。

1. 提交任务
2. 每 3 秒轮询进度
3. 检测待支付并自动支付（如需要）
4. 等待完成（最长 1 小时）
5. 返回视频下载链接或错误信息

### 函数签名

```python
execute_workflow(
    diy_story: str,                           # 故事/剧本内容（必填）
    aspect: str,                              # 画幅比例：16:9 或 9:16（必填）
    project_name: str,                        # 项目名称（必填）
    video_duration: str = "auto",             # 时长，默认 "auto"（可选）
    style_id: Optional[int] = None,           # 风格 ID（可选）
    project_type: str = "director",           # 模式，默认 "director"（可选）
    character_info: Optional[List[Dict]] = None  # 角色图片（可选）
)
```

### 参数说明

| 参数 | 必填 | 说明 |
|-----------|----------|-------------|
| diy_story | 是 | 故事或剧本内容 |
| aspect | 是 | 画幅比例：`16:9` 或 `9:16` |
| project_name | 是 | 项目名称 |
| video_duration | 否 | 可选值：`auto`、`30`、`60`、`120`、`180`、`240`、`300`；默认 `"auto"` |
| style_id | 否 | 风格 ID；未指定时可省略 |
| project_type | 否 | `director` / `narration` / `short-film`；默认 `"director"` |
| character_info | 否 | 角色图片列表，格式：`[{"name": "角色名", "url": "图片URL"}, ...]` |

### 使用流程

1. **介绍并选择生成模式**（必须）：在生成前，**必须先向用户介绍三种模式的特点**，再让用户选择。展示如下：

   > 我们支持三种视频生成模式，请选择：
   >
   > **🎬 剧集模式（director）**：AI 导演自动分镜、设计镜头语言，适合有角色对话和剧情推进的短剧。
   >
   > **🎙️ 解说模式（narration）**：以旁白为核心，配合画面素材，适合知识科普、新闻解读、产品介绍等解说类视频。
   >
   > **🎥 短片模式（short-film）**：故事与视觉兼顾，具有电影感的镜头与叙事节奏，适合情感短片、创意故事、艺术表达。

   等待用户明确选择后再继续。若用户未指定则默认剧集模式。

2. **若用户希望选择风格**：调用 `get_styles()` 获取风格列表，展示 ID、名称、分类、描述；等待用户选择后再继续。
3. **若用户提供了角色图片 URL**：构建 `character_info` 数组传入，每个角色包含 `name`（角色名）和 `url`（图片 URL）。
4. **运行工作流**：
   - 用故事内容、画幅比例、项目名称调用 `execute_workflow()`。
   - 根据用户选择的模式设置 `project_type`；若用户指定了时长则传入 `video_duration`（否则默认 `"auto"`）；若用户选择了风格则传入 `style_id`；若用户提供了角色图片则传入 `character_info`。
   - **调用一次并等待返回** — 函数内部完成创建、提交、轮询、支付和完成，最后返回下载链接或错误。

### 示例

**查看风格列表**：

```python
api = TrusteeModeAPI()
styles_result = api.get_styles()
# 向用户展示风格列表
```

**基础工作流（无时长、无风格）**：

```python
api = TrusteeModeAPI()
result = api.execute_workflow(
    diy_story="一个冒险故事...",
    aspect="16:9",
    project_name="我的视频项目"
)
# result 包含下载 URL 或错误信息
```

**指定时长，无风格**：

```python
result = api.execute_workflow(
    diy_story="一个冒险故事...",
    aspect="16:9",
    project_name="我的视频项目",
    video_duration="60"
)
```

**指定时长和风格**：

```python
result = api.execute_workflow(
    diy_story="一个冒险故事...",
    aspect="16:9",
    project_name="我的视频项目",
    video_duration="60",
    style_id=142
)
```

**解说模式**：

```python
result = api.execute_workflow(
    diy_story="今天我们来聊聊 AI 的发展...",
    aspect="16:9",
    project_name="解说视频",
    project_type="narration"
)
```

**短片模式**：

```python
result = api.execute_workflow(
    diy_story="夕阳西下，一位老渔夫独自划船归家，海面被染成一片通红...",
    aspect="16:9",
    project_name="短片",
    project_type="short-film"
)
```

**指定角色图片**（用户提供角色形象 URL 时）：

```python
result = api.execute_workflow(
    diy_story="小明和小红在公园偶遇，两人相视而笑...",
    aspect="16:9",
    project_name="角色定制视频",
    character_info=[
        {"name": "小明", "url": "https://xxx/xiaoming.jpg"},
        {"name": "小红", "url": "https://xxx/xiaohong.jpg"}
    ]
)
```

## 返回值

函数会阻塞直到任务完成（成功或失败）或超时（1 小时）。请等待其返回。

**成功**（包含下载链接）：

```json
{
    "code": 200,
    "msg": "success",
    "uuid": "...",
    "data": {
        "project_id": "...",
        "video_asset": {...},
        "status": "completed"
    }
}
```

请将**完整的签名 URL** 返回给用户（`data.video_asset.download_url`），例如：

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```

不要返回未带查询参数的未签名 URL，例如：

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

**失败**：

```json
{
    "code": -1,
    "msg": "Error message",
    "data": null
}
```
