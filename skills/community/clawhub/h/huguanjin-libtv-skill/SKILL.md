---
name: libtv-skill
description: >-
  agent-im 会话技能 - 通过 liblib.tv 的 AI 能力生成和编辑图片/视频，兼容 Gemini 文生图、Sora/Veo/Grok/豆包/Vidu 视频直连。
  覆盖：文生图、文生视频、图生视频、视频编辑、风格迁移、视频续写、MV生成、短剧生成、分镜设计。
  触发词：画、生成、做动画、改镜头、换风格、转绘、复刻、liblib、libtv、上传参考图。
  当用户明确指定 Gemini 时走文生图兼容路径；指定 Sora/Veo/Grok/豆包/Vidu 时走视频直连路径。
argument-hint: '输入创作需求，如"画一只戴墨镜的猫"'
user-invocable: true
license: Apache-2.0
metadata:
  version: "1.0.3"
  openclaw:
    emoji: "💬"
    requires:
      bins: ["python3"]
      env: ["LIBTV_ACCESS_KEY", "API_KEY"]
    primaryEnv: "LIBTV_ACCESS_KEY"
compatibility: "LibTV 会话 + Gemini + Sora/Veo/Grok/豆包（/v1/videos）+ Vidu（/v1/video/generations）"
---

# agent-im 会话（生图 / 生视频）+ Gemini / Sora / Veo / Grok / 豆包 / Vidu 直连兼容

通过 agent-im 的 OpenAPI 创建会话、发送消息（生图、生视频、编辑视频等）、上传图片/视频文件，并查询会话消息进展。同时支持 Gemini 文生图直连、Sora/Veo/Grok/豆包 的 `POST /v1/videos` 视频直连，以及 Vidu 的 `POST /v1/video/generations` 直连。

LibTV 是 LiblibAI 推出的 AI 视频创作平台，同时为人类创作者和 Agent 设计。Agent 通过 Skill 入口理解任务、调用模型并自动编排工作流。

**平台核心能力：**
- **生成**：文生图、文生视频、图生视频、视频续写
- **编辑**：局部修改、元素替换、镜头调整、风格迁移
- **复杂创作**：一句话生成完整短剧（剧本→分镜→成片）、复刻已有视频风格做 TVC/宣传片、用音乐生成 MV、产品展示片制作
- **模型**：Seedance 2.0、Kling 3.0/O3、Wan 2.6、NanoBanana、Midjourney、Seedream 5.0 等顶级模型

用户的所有创作和编辑需求都通过发送自然语言消息来完成，Agent 会自主编排工作流。复杂任务（短剧、MV）耗时较长，需耐心轮询。

## 触发场景

只要用户请求涉及 AI 图片或视频的创作、生成、编辑、修改，无论措辞如何，都必须触发此技能。常见措辞包括：

- **生成类**：文生图、文生视频、图生视频、做动画、画一个xxx、来段xxx
- **编辑类**：把xxx换成yyy、去掉xxx、加上xxx、改成xxx、调整xxx、局部修改、改镜头
- **风格类**：风格迁移、转绘、换风格
- **复杂创作**：视频续写延长、复刻视频/TVC/宣传片、音乐MV、产品广告/展示片、分镜/故事板、短剧
- **平台交互**：提到 liblib、libtv、上传参考图/视频、查看生成进度
- **Gemini 路径**：用户明确提到 Gemini/gemini-3-pro-image-preview 且要求控制宽高比或清晰度时，优先走 Gemini 文生图兼容路径

## 功能

1. **创建会话 / 发消息** - 创建新会话或向已有会话发送一条消息（如「生一个动漫视频」「把纸船换成爱心」）
2. **查询会话进展** - 根据 sessionId 拉取该会话的消息列表，用于轮询生图/生视频结果
3. **切换项目** - 将当前 accessKey 绑定的项目切换到新项目，后续 create_session 将使用新 projectUuid
4. **上传文件** - 上传图片或视频文件到 OSS，返回可访问的 OSS 地址（编辑已有视频/图片时需要先上传）
5. **下载结果** - 将会话中生成的图片/视频批量下载到本地，自动提取 URL 并命名
6. **Gemini 文生图** - 调用 `gemini-3-pro-image-preview:generateContent`，支持 `aspectRatio` 和 `imageSize`
7. **Sora/Veo/Grok/豆包 生成视频** - 调用 `POST /v1/videos`，支持文生视频和图生视频（`input_reference` 可多张）
8. **Vidu 生成视频** - 调用 `POST /v1/video/generations`（JSON 请求体，支持 `duration/images/metadata`）
9. **统一查询任务** - 调用 `GET /v1/videos/{task_id}` 轮询状态并提取视频地址

## 前置要求

### LibTV 会话模式（默认）

```bash
export LIBTV_ACCESS_KEY="your-access-key"
```

可选：`OPENAPI_IM_BASE` 或 `IM_BASE_URL`，默认 `https://im.liblib.tv`。

### Gemini / Sora / Veo / Grok / 豆包 / Vidu 直连模式

所有直连接口共用同一组 API 地址和密钥：

```bash
export API_KEY="your-api-key"           # 必填
export API_BASE_URL="https://your-api-host"  # 必填（只写域名，不带路径）
```

各 provider 可选模型参数详见 `.env` 文件或 [references/usage-guide.md](./references/usage-guide.md)。

无需安装额外依赖，仅使用 Python 标准库。

## 使用方法

### 1. 创建会话 / 发送消息

```bash
# 创建新会话并发送「生一个动漫视频」
python3 {baseDir}/scripts/create_session.py "生一个动漫视频"

# 向已有会话发送消息
python3 {baseDir}/scripts/create_session.py "再生成一张风景图" --session-id SESSION_ID

# 只创建/绑定会话，不发消息
python3 {baseDir}/scripts/create_session.py
```

### 2. 查询会话进展

```bash
# 查询会话消息列表
python3 {baseDir}/scripts/query_session.py SESSION_ID

# 增量拉取（只返回 seq 大于 N 的消息）
python3 {baseDir}/scripts/query_session.py SESSION_ID --after-seq 5

# 附带项目地址（传入 create_session 返回的 projectUuid，结果中带 projectUrl）
python3 {baseDir}/scripts/query_session.py SESSION_ID --project-id PROJECT_UUID
```

### 3. 切换项目

```bash
# 切换当前 accessKey 绑定的项目（后续创建会话将使用新项目）
python3 {baseDir}/scripts/change_project.py
```

### 4. 上传文件

当用户提供了参考的文件地址时，进行上传，仅支持图片、视频，文件大小必须在200M以下。

```bash
# 上传图片
python3 {baseDir}/scripts/upload_file.py /path/to/image.png

# 上传视频
python3 {baseDir}/scripts/upload_file.py /path/to/video.mp4
```

### 5. 下载结果

生成完成后，可以将会话中的所有图片/视频批量下载到本地。

```bash
# 从会话自动提取并下载所有结果
python3 {baseDir}/scripts/download_results.py SESSION_ID

# 指定输出目录
python3 {baseDir}/scripts/download_results.py SESSION_ID --output-dir ~/Desktop/my_project

# 指定文件名前缀（如 storyboard_01.png, storyboard_02.png ...）
python3 {baseDir}/scripts/download_results.py SESSION_ID --prefix "storyboard"

# 直接下载指定 URL 列表（不需要 session_id）
python3 {baseDir}/scripts/download_results.py --urls URL1 URL2 URL3 --output-dir ./output
```

### 6. Gemini 文生图

```bash
python3 {baseDir}/scripts/gemini_generate_image.py "赛博朋克风格的城市夜景海报" --aspect-ratio 16:9 --image-size 2K
```

### 7. 视频生成（Sora/Veo/Grok/豆包/Vidu）

```bash
# 文生视频
python3 {baseDir}/scripts/sora_generate_video.py "猫咪听歌摇头晃脑" --model sora-2 --seconds 10

# 图生视频
python3 {baseDir}/scripts/sora_generate_video.py "让角色开始微笑" --input-reference ./ref.jpg --seconds 10

# Vidu 文生视频
python3 {baseDir}/scripts/vidu_generate_video.py "一个美女在雨中跳舞" --seconds 5
```

各 provider 别名入口（`veo_generate_video.py`、`grok_generate_video.py`、`doubao_generate_video.py`）和更多示例见 [references/usage-guide.md](./references/usage-guide.md)。

### 8. 查询视频任务

```bash
# 单次查询
python3 {baseDir}/scripts/sora_query_video.py TASK_ID

# 轮询到完成
python3 {baseDir}/scripts/sora_query_video.py TASK_ID --wait --interval 5 --max-wait 900
```

别名查询入口：`veo_query_video.py`、`grok_query_video.py`、`doubao_query_video.py`、`vidu_query_video.py`。

## 典型工作流

详细工作流场景参见 references/workflows.md。

核心流程概要：
- **LibTV 会话模式**：create_session → 轮询 query_session（每 8 秒）→ 自动 download_results → 展示结果 + projectUrl
- **编辑/参考图**：先 upload_file 拿到 OSS URL → 拼入消息 → create_session
- **Gemini 文生图**：gemini_generate_image → 展示 saved 文件
- **Sora/Veo/Grok/豆包/Vidu 直连**：generate_video → query_video 轮询 → 展示 videoUrl

## 输出格式

各脚本的详细 JSON 输出格式参见 references/output-format.md。

## 最终向用户展示时（OpenClaw）

- **视频地址**：来自 `query_session` 返回的 `messages` 中 assistant 消息的 content 或结果里的视频/图片 URL，即「返回的结果」。
- **项目地址**：使用 `create_session` 返回的 `projectUrl`，或自行拼接 `https://www.liblib.tv/canvas?projectId=` + `projectUuid`。查询进展时若传入 `--project-id PROJECT_UUID`，`query_session` 会直接返回 `projectUrl`，便于一并展示。
- **Gemini 文生图**：展示 `gemini_generate_image.py` 输出中的 `saved` 文件列表（该流程没有 projectUrl）。
- **Sora/Veo/Grok/豆包/Vidu 直连视频**：展示 `sora_query_video.py` 或各别名查询脚本输出中的 `videoUrl`（该流程没有 projectUrl）。

在 **LibTV** 任务完成时，同时给出：**视频/图片结果链接** + **项目画布链接（projectUrl）**。
在 **Gemini** 任务完成时，只给出：**图片结果（saved 文件路径）**。
在 **Sora/Veo/Grok/豆包/Vidu** 任务完成时，只给出：**视频结果链接（videoUrl）**。
过程中，不要给出 **项目画布链接（projectUrl）**。

## 核心原则：用户侧不做创作，只做传话

该原则针对 LibTV 会话模式；Gemini 文生图直连模式为单次请求直接出图。

你（用户侧 Agent）的职责是**搬运工**，不是创作者。后端有专门的 Agent 负责理解需求、拆解分镜、编排工作流、选模型、写 prompt。你要做的只有三件事：

1. **上传**：用户给了本地文件 → `upload_file.py` 拿到 OSS URL
2. **传话**：把用户的原始描述 + OSS URL 原封不动发给 `create_session.py`
3. **取件**：轮询结果 → 下载到本地 → 展示给用户

**绝对不要做的事：**
- 不要替用户扩写、润色、翻译 prompt（用户说"帮我推演分镜"，就直接传"帮我推演分镜"，不要自己先写个分镜表再逐条发）
- 不要自行拆解任务步骤（如把"生成9张分镜图"拆成9次独立请求）
- 不要自行编排镜头描述、剧情推演、风格分析
- 不要在消息中添加自己编的 prompt（如"超写实风格，电影级光影，8K分辨率"之类的描述词）

后端 Agent 对模型能力、参数配置、prompt 工程远比用户侧更专业。用户侧越俎代庖只会降低生成质量，换个弱模型更是灾难。

**正确示例：**
```
用户说：「帮我推演后续的故事，来个分镜大爆炸，帮我出一个16:9的九宫格的图。新建一个任务。」
用户给了参考图：/path/to/ref.png

→ upload_file.py /path/to/ref.png  →  拿到 oss_url
→ create_session.py "帮我推演后续的故事，来个分镜大爆炸，帮我出一个16:9的九宫格的图。参考图：{oss_url}"
→ 轮询 → 下载 → 展示
```

**错误示例：**
```
❌ 用户侧自己先写了个九宫格分镜表（对峙、交锋、危机...）
❌ 然后把自己编的描述发给后端
❌ 或者拆成9次 create_session 分别发送
```

## 注意事项

- 鉴权方式为请求头 `Authorization: Bearer <LIBTV_ACCESS_KEY>`
- 创建会话时若不传 `message`，仅创建/绑定会话，不会调用 SendMessage
- 查询会话时可用 `--after-seq` 做增量拉取，便于轮询新消息（含 assistant 回复与生图/生视频结果）
- 项目画布地址固定为：`https://www.liblib.tv/canvas?projectId=` + projectUuid
- 切换项目后，Redis 缓存会更新，下次 create_session 将使用新的 projectUuid
- 上传文件仅支持图片（image/*）和视频（video/*）类型，其他类型会被拒绝，文件大小须在 200MB 以下
- 上传返回的 OSS 地址格式为 `https://libtv-res.liblib.art/claw/{projectUuid}/{uuid}{ext}`
- 生成过程中只告知用户"正在生成中"，不要提前给出 projectUrl；任务完成后再同时给出：**结果链接（图片/视频 URL）** + **项目画布链接（projectUrl）**
- Gemini 文生图接口路径：`/v1beta/models/gemini-3-pro-image-preview:generateContent`
- Gemini 请求需携带 query 参数 `key`；若中转接口要求，额外携带 `Authorization: Bearer <token>`
- Gemini 可通过 `generationConfig.imageConfig.aspectRatio` 控制宽高比，通过 `imageSize` 控制清晰度（如 `1K`、`2K`、`4K`）
- Sora/Veo/Grok/豆包 视频接口路径：`POST /v1/videos`，鉴权为 `Authorization: Bearer <*_API_KEY>`
- Sora/Veo/Grok/豆包 图生视频通过重复字段 `input_reference` 上传多张图片；查询优先使用 `GET /v1/videos/{task_id}`
- Veo 系列模型可使用 `VEO_*` 环境变量别名，常用模型如 `veo_3_1-fast`，并支持 `enable_upsample` 参数
- Grok 系列可使用 `GROK_*` 环境变量别名，常见 `size` 为 `720P/1080P`
- 豆包系列可使用 `DOUBAO_*` 环境变量别名，常见 `size` 为 `16:9/4:3/1:1/3:4/9:16/21:9/keep_ratio/adaptive`
- Vidu 提交路径是 `POST /v1/video/generations`（JSON）；图生/首尾帧使用 `--image-urls`，查询仍建议 `GET /v1/videos/{task_id}`
