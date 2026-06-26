---
name: miaoyin-ai-music
description: 妙音AI 音乐创作助手，生成歌曲、查询任务、续写音乐、生成歌词。当用户需要 AI 作曲或音乐生成时调用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - MIAOYIN_API_TOKEN
    primaryEnv: MIAOYIN_API_TOKEN
    emoji: "🎵"
---

# 🎵 妙音AI 音乐助手

通过 HTTP REST API 调用音乐生成服务。

---

## ⛔ 强制规则（违反任何一条即为错误）

1. **只能使用下方定义的 HTTP REST API**。绝对不要尝试 MCP JSON-RPC、WebSocket 或任何其他协议。
2. **所有 API 调用必须使用 HTTP 请求**（POST），Base URL 固定为 https://ai.growingth.com/api，不要猜测或尝试其他端点。
3. **严禁编造 API 响应**。如果 API 调用失败，直接告诉用户"调用失败"并附上错误信息，不要编造结果或提供"手动操作指南"。
4. **严禁改写 API 返回的内容**。歌词、歌曲标题等必须原样展示，不要总结、翻译、改写或省略。
5. **严禁在 API 调用失败时建议用户去网页手动操作**。只需报告错误，让用户检查 API Token 或稍后重试。
6. **不要使用 web_fetch、curl 或任何网页抓取工具来调用这些 API**。只使用标准 HTTP 请求工具。
7. **严禁对 API Token 进行任何格式校验**（包括长度、字符类型、结构等）。无论 token 看起来多么"奇怪"，都必须直接调用 API 验证。
8. **严禁添加 skill 文档中未提及的"优化"或"帮助"**。不要自行重试、不要自行解释错误原因、不要提供文档未规定的建议。

---

## 第一步：配置 API Token

设置环境变量 `MIAOYIN_API_TOKEN`：

- **Linux/macOS**: `export MIAOYIN_API_TOKEN=your-token`
- **Windows PowerShell**: `$env:MIAOYIN_API_TOKEN="your-token"`
- **Windows CMD**: `set MIAOYIN_API_TOKEN=your-token`
- **Docker**: `-e MIAOYIN_API_TOKEN=your-token`
- **.env 文件**: 写入 `MIAOYIN_API_TOKEN=your-token`

⚠️ 任何能设置环境变量的方式都可以，不依赖特定平台。

### 获取 API Token

1. 访问 https://ai.growingth.com/api-service
2. 登录后获取您的 API Token
3. 复制 Token 并保存
4. ⚠️ 请妥善保管您的 Token，不要泄露给他人

---

## 第二步：开始创作

对话示例：
- 「帮我生成一首关于夏天的流行歌曲」
- 「查一下刚才的歌好了吗」
- 「显示我最近的音乐列表」
- 「获取这首歌的歌词」

---

## API 调用规范

**Base URL**: `https://ai.growingth.com/api`

**请求方法**: POST（所有接口统一使用 POST）

**认证 Header**: `api-token: ${MIAOYIN_API_TOKEN}`

**格式**: JSON

**编码**: UTF-8（请求体必须使用 UTF-8 编码，中文直接传入）

**网络**: 自动使用系统代理（HTTP_PROXY/HTTPS_PROXY）

**超时**: 默认 30 秒，查询任务状态可延长至 60 秒

### 请求结构（重要）

⚠️ **所有接口统一使用以下格式**：

```json
{
  "name": "操作名称",
  "data": {
    // 具体请求参数
  }
}
```

**Header 示例**：
```json
{
  "api-token": "Your API Token",
  "Content-Type": "application/json; charset=utf-8"
}
```

⚠️ 注意：
1. 所有接口都是 POST 请求到 `https://ai.growingth.com/api`
2. 操作名称通过 `name` 字段指定（也可以写在 query 参数上）
3. 具体请求数据必须放在 `data` 对象中
4. 认证使用 `api-token` Header，不是 `Authorization`

---

## ⚠️ 调用前自检（每次对话必须逐项确认）

在调用任何 API 之前，请在心中默念：

- [ ] 我有 MIAOYIN_API_TOKEN 吗？
  → 没有：引导用户获取，不要尝试调用 API
  
- [ ] 用户的要求能用现有 API 实现吗？
  → 不能：直接说"抱歉，当前不支持此功能"，不要编造
  
- [ ] 我知道每个参数的含义和必填性吗？
  → 不确定：查阅 API 文档，不要猜测
  
- [ ] 我准备好处理可能的错误了吗？
  → 没有：先阅读"错误处理流程"章节

任何一项为"否"，都不要继续调用 API。

---

## 错误提示模板（必须原样使用，不准修改）

| 错误类型 | 提示语 |
|---------|--------|
| 余额不足 | "❌ 余额不足\n\n您当前的余额不足，无法继续创作。\n请访问 https://ai.growingth.com/api-service 进行额度购买。" |
| 未获取Token | "❌ 未配置 API Token\n\n您当前尚未获得凭证（token）。\n请前往 https://ai.growingth.com/api-service 创建获取，以开始您的创作。\n\n🎁 创建后您将获得 10 首歌的免费体验额度！" |
| 版权保护 | "❌ 转换失败\n\n该音频与现有作品匹配，触发了版权保护机制，无法转换为 WAV 格式。\n\n建议：尝试转换其他原创歌曲。" |
| 401/403 | "API Token 无效或已过期，请检查 MIAOYIN_API_TOKEN 配置" |
| 5xx | "请求服务器异常，请稍后重试" |
| 超时 | "请求超时，请稍后重试" |
| 网络错误 | "网络连接失败，请检查网络或代理设置" |

⚠️ 禁止使用其他表述，禁止添加"可能原因"、"建议检查"等额外内容。

### 错误类型判断规则

根据 API 返回的错误信息，按以下优先级判断错误类型：

1. **余额不足**：响应消息包含"余额不足"、"balance"、"insufficient"等关键词
2. **未获取Token**：响应消息包含"token"、"凭证"、"未获得"等关键词（且不是 401/403 状态码）
3. **版权保护**：响应消息包含"matches existing work of art"、"版权"、"copyright"等关键词
4. **401/403**：HTTP 状态码为 401 或 403
5. **5xx**：HTTP 状态码为 500-599
6. **超时**：请求超时
7. **网络错误**：网络连接失败

---

## 详细错误日志输出（必须执行）

**任何 HTTP 请求失败时，除了展示上述用户友好的提示外，还必须输出详细的技术日志供排查问题。**

### 日志输出格式

```
=== 错误详情 ===
请求：POST https://ai.growingth.com/api
操作：{{操作名称}}
状态码：{{状态码}}
错误：{{错误信息}}

--- 请求头 ---
Content-Type: application/json
api-token: ********

--- 请求体 ---
{
  "name": "{{操作名称}}",
  "data": { ... }
}

--- 响应头 ---
{{响应头信息}}

--- 响应体 ---
{{响应体内容}}
```

### 敏感信息隐藏规则

- `api-token: xxx` → `api-token: ********`
- `MIAOYIN_API_TOKEN` 环境变量的完整值 → `********`

---

## 版本声明

- **Skill 版本**: 1.0.0
- **API 版本**: 以实际 API 响应为准
- **兼容性**: 不假设 API 格式固定，以实际响应为准

如果 API 响应包含未预期的字段，原样展示，不要报错。

---

## API 接口列表

### API 1：生成歌曲

用途：用户想创作/生成音乐时调用。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=generateCustom
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "prompt": "歌词内容",
    "tags": "歌曲风格，如 Chinese, Piano, Guitar",
    "negative_tags": "排除风格（可选）",
    "model": "chirp-v5",
    "desc": "描述信息（可选）",
    "title": "歌曲标题（可选）",
    "make_instrumental": false
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | String | ✅ 是 | 歌词内容 |
| tags | String | ❌ 否 | 歌曲风格，如 Chinese, Piano, Guitar |
| negative_tags | String | ❌ 否 | 排除风格 |
| model | String | ❌ 否 | 模型版本：chirp-v5-5, chirp-v5, chirp-v4-5, chirp-v4, chirp-v3-5，默认 chirp-v5 |
| desc | String | ❌ 否 | 描述信息 |
| title | String | ❌ 否 | 歌曲标题 |
| make_instrumental | Boolean | ❌ 否 | 是否纯音乐，默认 false |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": [
    {
      "taskId": "c13975cda17449da2261"
    }
  ]
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Array | 任务数据数组 |
| data[].taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [生成歌曲] [创作音乐] [写首歌] [做首曲子] 等意图时：

步骤 1：确认需求
  IF 用户提供了歌词：
    prompt = 用户提供的完整歌词
  ELSE IF 用户描述了音乐风格（如"夏天的流行歌"）：
    prompt = 用户的描述
    tags = 根据描述提取风格标签
  ELSE:
    询问用户："请提供歌词，或描述您想要的音乐风格（例如：帮我生成一首关于夏天的流行歌曲）"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=generateCustom
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "prompt": "步骤 1 中确定的歌词或描述",
        "tags": "用户指定的风格（可选）",
        "title": "用户指定的标题（可选）",
        "model": "chirp-v5",
        "make_instrumental": 用户要求纯音乐则为 true，否则为 false
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data[0].taskId
    说："✅ 提交成功！任务编号：{taskId}，正在生成中，请稍候..."
    → 转到查询任务状态流程（待补充）
  ELSE:
    说："❌ 生成失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：用户提供歌词

```
用户：我想用这首歌词生成音乐：
[Verse]
阳光洒在海面
微风吹拂着脸

[Chorus]
这是我们的夏天
永远不变的画面

AI: 收到！我将用您提供的歌词生成音乐。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    [请求体] {
      "data": {
        "prompt": "[Verse]\n阳光洒在海面\n微风吹拂着脸\n\n[Chorus]\n这是我们的夏天\n永远不变的画面",
        "model": "chirp-v5"
      }
    }
    
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中，请稍候...
```

#### 示例 2：用户描述风格

```
用户：帮我生成一首关于夏天的流行歌曲，要有钢琴和吉他

AI: 好的，我来帮您创作一首夏天主题的流行歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    [请求体] {
      "data": {
        "prompt": "关于夏天的流行歌曲",
        "tags": "Piano, Guitar",
        "model": "chirp-v5"
      }
    }
    
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中，请稍候...
```

#### 示例 3：生成纯音乐

```
用户：生成一首中国风的纯音乐

AI: 好的，我来为您创作一首中国风纯音乐。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    [请求体] {
      "data": {
        "prompt": "中国风纯音乐",
        "tags": "Chinese",
        "model": "chirp-v5",
        "make_instrumental": true
      }
    }
    
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中，请稍候...
```

### ⚠️ 关键注意事项

1. **编码要求**
   - 请求体必须使用 UTF-8 编码
   - 中文歌词直接传入，不要转义

2. **模型版本选择**
   - 默认使用 `chirp-v5`
   - 可选版本：chirp-v5-5（最新）, chirp-v5, chirp-v4-5, chirp-v4, chirp-v3-5
   - 除非用户明确指定，否则使用默认版本

3. **风格标签（tags）**
   - 多个风格用逗号分隔，如 "Chinese, Piano, Guitar"
   - 常见风格：Pop, Rock, Jazz, Classical, Electronic, Chinese, Piano, Guitar 等

4. **任务编号保存**
   - 生成成功后，必须保存 taskId 用于后续查询
   - 在对话上下文中记住最近的 taskId

---

### API 2：查询歌曲状态

用途：查询生成进度和结果。

⚠️ **重要警告**：请勿过于频繁调用此接口，建议查询间隔不低于 10 秒，否则可能会被禁用。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=getMusic
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "ids": "c13975cda17449da2261,0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | String | ✅ 是 | 歌曲 id 列表（也可以是 taskId），以英文逗号分隔多个 |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": [
    {
      "id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
      "title": "Through the Fog",
      "image_url": "https://cdn2.suno.ai/image_0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f.jpeg",
      "lyric": "[Instrumental]",
      "audio_url": "https://cdn1.suno.ai/0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f.mp3",
      "video_url": "https://cdn1.suno.ai/0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f.mp4",
      "created_at": "2024-08-30T07:46:22.206Z",
      "model_name": "chirp-v4",
      "status": "complete"
    }
  ]
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Array | 歌曲数据数组 |
| data[].id | String | 歌曲唯一标识 |
| data[].title | String | 歌曲标题 |
| data[].image_url | String | 封面图片链接 |
| data[].lyric | String | 歌词内容 |
| data[].audio_url | String | 音频播放链接 |
| data[].video_url | String | 视频播放链接 |
| data[].created_at | String | 创建时间 |
| data[].model_name | String | 使用的模型名称 |
| data[].status | String | 生成状态：complete（完成）/ processing（处理中）/ queued（排队中）/ failed（失败） |

### 调用决策树（严格按此流程执行）

```
当需要查询歌曲状态时（生成后自动查询 / 用户主动询问）：

步骤 1：确定要查询的任务编号
  IF 是刚生成的任务：
    taskId = 上一步生成歌曲返回的 taskId
  ELSE IF 用户提供了编号（如"查一下 c13975cda17449da2261 的状态"）：
    taskId = 用户提供的编号
  ELSE IF 用户说"刚才的歌/最近的任务"：
    taskId = 最近一次提交的任务编号（需要从上下文记忆）
  ELSE:
    询问用户："请问要查询哪个任务？请提供任务编号"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=getMusic
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "ids": taskId
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    FOR EACH song IN response.data:
      status = song.status
      
      IF status == "complete":
        展示：
          🎵 歌曲名：{song.title}
          🎼 歌词：{song.lyric}
          ▶️ 音频播放：{song.audio_url} | 下载：{song.audio_url}
          🎬 视频播放：{song.video_url} | 下载：{song.video_url}
          🖼️ 封面图片：{song.image_url}
          📅 创建时间：{song.created_at}
          🤖 模型：{song.model_name}
      
      ELSE IF status == "processing" 或 "queued":
        说：
          ⏳ 音乐还在生成中，当前状态：{status}
          请您过 10 秒以上再问我"好了吗"，我会继续为您查询。
        → 停止，不要再调用 API
      
      ELSE IF status == "failed":
        说：
          ❌ 生成失败
          任务编号：{song.id}
        → 停止，不要重试
      
      ELSE:
        说：
          ⚠️ 未知状态：{status}
  ELSE:
    说："❌ 查询失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：生成后自动查询（完成）

```
用户：帮我生成一首关于夏天的流行歌曲

AI: [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中，请稍候...
    
    [等待 10 秒后执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "c13975cda17449da2261"
      }
    }
    
    🎵 生成完成！
    歌曲名：夏日微风
    歌曲id:1231465
    🎼 歌词：
    [Verse]
    阳光洒在海面
    微风吹拂着脸
    ...
    
    ▶️ 音频播放：https://cdn1.suno.ai/c13975cda17449da2261.mp3 | 下载：https://cdn1.suno.ai/c13975cda17449da2261.mp3
    🎬 视频播放：https://cdn1.suno.ai/c13975cda17449da2261.mp4 | 下载：https://cdn1.suno.ai/c13975cda17449da2261.mp4
    🖼️ 封面图片：https://cdn2.suno.ai/image_c13975cda17449da2261.jpeg
```

#### 示例 2：用户主动询问（处理中）

```
用户：刚才那首歌好了吗

AI: [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "c13975cda17449da2261"
      }
    }
    
    ⏳ 音乐还在生成中，当前状态：processing
    请您过 10 秒以上再问我"好了吗"，我会继续为您查询。
```

#### 示例 3：批量查询多个任务

```
用户：帮我查一下这三个任务的状态：c13975cda17449da2261,0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f,d57dba20-e63d-4c99-ab43-9469d2944f9f

AI: [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "c13975cda17449da2261,0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f,d57dba20-e63d-4c99-ab43-9469d2944f9f"
      }
    }
    
    任务 1：✅ 已完成
      歌曲名：夏日微风
      ▶️ 播放：https://cdn1.suno.ai/c13975cda17449da2261.mp3 | 下载：https://cdn1.suno.ai/c13975cda17449da2261.mp3
    
    任务 2：✅ 已完成
      歌曲名：Through the Fog
      ▶️ 播放：https://cdn1.suno.ai/0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f.mp3 | 下载：https://cdn1.suno.ai/0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f.mp3
    
    任务 3：⏳ 生成中（processing）
      请稍后再问
```

### ⚠️ 关键注意事项

1. **查询频率限制（非常重要）**
   - **最小查询间隔：10 秒**
   - 违反此规则可能导致接口被禁用
   - 生成后第一次查询：建议等待 10-15 秒
   - 用户再次询问：确保距离上次查询至少 10 秒

2. **轮询限制**（必须严格遵守）
   - ✅ 允许：生成后等待 10 秒查询 1 次
   - ✅ 允许：用户询问时再查询 1 次（间隔 10 秒以上）
   - ❌ 禁止：自己循环调用查询接口
   - ❌ 禁止：在 10 秒内连续查询
   - ❌ 禁止：在任务未完成时频繁查询

3. **状态处理优先级**
   ```
   complete → 立即展示播放链接和完整信息
   failed → 展示失败信息，不要重试
   processing/queued → 告知用户稍后再问（至少 10 秒），然后停止
   ```

4. **歌词展示**
   - 必须完整原样展示 lyric 字段内容
   - 不要总结、翻译、改写或省略
   - 纯音乐的歌词通常是 "[Instrumental]"

5. **批量查询**
   - 支持一次查询多个任务
   - 多个 id 用英文逗号分隔
   - 最多建议一次查询不超过 10 个

---

### API 3：续写歌曲

用途：如果歌曲效果不错，但时长不足，可通过此接口进行续写。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=generateContinue
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "audio_id": "歌曲 clipId",
    "continue_clip_id": "歌曲 clipId",
    "continue_at": 7,
    "prompt": "歌词内容（可选）",
    "tags": "歌曲风格（可选）",
    "negative_tags": "排除风格（可选）",
    "model": "chirp-v5",
    "desc": "描述信息（可选）",
    "title": "歌曲标题（可选）",
    "make_instrumental": false
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audio_id | String | ✅ 是 | 续写歌曲的 clipId |
| continue_clip_id | String | ✅ 是 | 续写歌曲的 clipId（与 audio_id 相同） |
| continue_at | Number | ✅ 是 | 续写时间点，单位秒 |
| prompt | String | ❌ 否 | 歌词内容 |
| tags | String | ❌ 否 | 歌曲风格，如 Chinese, Piano, Guitar |
| negative_tags | String | ❌ 否 | 排除风格 |
| model | String | ❌ 否 | 模型版本：chirp-v5, chirp-v4-5, chirp-v4, chirp-v3-5，默认 chirp-v5 |
| desc | String | ❌ 否 | 描述信息 |
| title | String | ❌ 否 | 歌曲标题 |
| make_instrumental | Boolean | ❌ 否 | 是否纯音乐，默认 false |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": [
    {
      "taskId": "xxx"
    }
  ]
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Array | 任务数据数组 |
| data[].taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [续写] [继续创作] [延长歌曲] [接着写] 等意图时：

步骤 1：确认续写需求
  IF 用户提供了歌曲 ID 和续写时间点：
    audio_id = 用户提供的歌曲 ID
    continue_at = 用户指定的时间点（秒）
  ELSE IF 用户提供了歌曲 ID 但未指定时间点：
    audio_id = 用户提供的歌曲 ID
    询问用户："请问从第几秒开始续写？（例如：从第 7 秒开始）"
    → 停止，等待用户回复
  ELSE IF 用户说"续写刚才的歌"：
    audio_id = 最近一次生成的歌曲 ID（从查询结果中获取）
    询问用户："请问从第几秒开始续写？（例如：从第 7 秒开始）"
    → 停止，等待用户回复
  ELSE:
    询问用户："请提供要续写的歌曲 ID 和续写时间点（例如：续写歌曲 xxx，从第 7 秒开始）"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=generateContinue
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "audio_id": audio_id,
        "continue_clip_id": audio_id,
        "continue_at": continue_at,  // 必须明确指定续写时间点（秒）
        "prompt": "用户指定的歌词（可选）",
        "tags": "用户指定的风格（可选）",
        "model": "chirp-v5",  // 固定使用 chirp-v5 模型
        "make_instrumental": 用户要求纯音乐则为 true，否则为 false
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data[0].taskId
    说："✅ 续写提交成功！任务编号：{taskId}，正在生成中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ 续写失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：续写指定歌曲

```
用户：帮我续写歌曲 0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f，从第 7 秒开始

AI: 好的，我将从第 7 秒开始续写这首歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateContinue]
    [请求体] {
      "data": {
        "audio_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "continue_clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "continue_at": 7,
        "model": "chirp-v5"
      }
    }
    
    ✅ 续写提交成功！任务编号：d57dba20-e63d-4c99-ab43-9469d2944f9f，正在生成中，请稍候...
```

#### 示例 2：续写最近的歌曲

```
用户：续写刚才那首歌

AI: 请问从第几秒开始续写？（例如：从第 7 秒开始）

用户：从第 10 秒开始

AI: 好的，我将从第 10 秒开始续写。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateContinue]
    [请求体] {
      "data": {
        "audio_id": "c13975cda17449da2261",
        "continue_clip_id": "c13975cda17449da2261",
        "continue_at": 10,
        "model": "chirp-v5"
      }
    }
    
    ✅ 续写提交成功！任务编号：xxx，正在生成中，请稍候...
```

#### 示例 3：续写并指定新歌词

```
用户：续写歌曲 0e66d6dd，从第 10 秒开始，加上这段歌词：
[Bridge]
时光流转不停
回忆永远鲜明

AI: 好的，我将从第 10 秒开始续写，并使用您提供的歌词。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateContinue]
    [请求体] {
      "data": {
        "audio_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "continue_clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "continue_at": 10,
        "prompt": "[Bridge]\n时光流转不停\n回忆永远鲜明",
        "model": "chirp-v5"
      }
    }
    
    ✅ 续写提交成功！任务编号：xxx，正在生成中，请稍候...
```

### ⚠️ 关键注意事项

1. **歌曲 ID 获取**
   - 歌曲 ID（clipId）从 API 2 查询歌曲状态的响应中获取
   - 响应字段中的 `id` 就是 clipId
   - 必须先查询歌曲状态，确认歌曲已完成（status = complete）后才能续写

2. **续写时间点（continue_at）**
   - 单位：秒
   - **必须明确指定具体的秒数**（例如：7、10、15 等）
   - 不能使用 0 或空值
   - 建议续写时间点不要超过原歌曲时长
   - 如果用户未指定，必须询问用户具体从第几秒开始

3. **audio_id 和 continue_clip_id**
   - 这两个字段必须相同
   - 都填写要续写的歌曲 clipId

4. **续写后的查询**
   - 续写成功后会返回新的 taskId
   - 使用 API 2 查询新任务的状态
   - 续写生成的是一首新歌曲，不会覆盖原歌曲

5. **模型版本**
   - **固定使用 chirp-v5 模型**
   - 不要使用其他模型版本

---

### API 4：翻唱模式（Cover）

用途：在保持主旋律的前提下，对歌曲进行翻唱改编或提升音质。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=generateCover
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "continue_clip_id": "歌曲 clipId",
    "prompt": "歌词内容（可选）",
    "tags": "歌曲风格（可选）",
    "negative_tags": "排除风格（可选）",
    "model": "chirp-v5",
    "title": "歌曲标题（可选）",
    "make_instrumental": false,
    "persona_id": "音色 persona_clip_id（可选）",
    "artist_clip_id": "音色 root_clip_id（可选）"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| continue_clip_id | String | ✅ 是 | 需要翻唱的歌曲 clipId |
| prompt | String | ❌ 否 | 歌词内容 |
| tags | String | ❌ 否 | 歌曲风格，如 Chinese, Piano, Guitar |
| negative_tags | String | ❌ 否 | 排除风格 |
| model | String | ❌ 否 | 模型版本：chirp-v5, chirp-v4-5, chirp-v4, chirp-v3-5，默认 chirp-v5 |
| title | String | ❌ 否 | 歌曲标题 |
| make_instrumental | Boolean | ❌ 否 | 是否纯音乐，默认 false |
| persona_id | String | ❌ 否 | 音色参数（通过 makePersona 任务获取的 persona_clip_id） |
| artist_clip_id | String | ❌ 否 | 音色参数（通过 makePersona 任务获取的 root_clip_id） |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": [
    {
      "taskId": "xxx"
    }
  ]
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Array | 任务数据数组 |
| data[].taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [翻唱] [改编] [Cover] [换个风格] [提升音质] 等意图时：

步骤 1：确认翻唱需求
  IF 用户提供了歌曲 ID：
    continue_clip_id = 用户提供的歌曲 ID
  ELSE IF 用户说"翻唱刚才的歌"：
    continue_clip_id = 最近一次生成的歌曲 ID（从查询结果中获取）
  ELSE:
    询问用户："请提供要翻唱的歌曲 ID"
    → 停止，等待用户回复
  
  可选确认：
  - tags = 用户指定的新风格
  - prompt = 用户指定的新歌词
  - persona_id / artist_clip_id = 用户指定的音色参数

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=generateCover
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "continue_clip_id": continue_clip_id,
        "prompt": "用户指定的歌词（可选）",
        "tags": "用户指定的风格（可选）",
        "model": "chirp-v5",
        "title": "用户指定的标题（可选）",
        "make_instrumental": 用户要求纯音乐则为 true，否则为 false
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data[0].taskId
    说："✅ 翻唱提交成功！任务编号：{taskId}，正在生成中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ 翻唱失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：翻唱指定歌曲

```
用户：帮我翻唱歌曲 0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f

AI: 好的，我将为您翻唱这首歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCover]
    [请求体] {
      "data": {
        "continue_clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "model": "chirp-v5"
      }
    }
    
    ✅ 翻唱提交成功！任务编号：xxx，正在生成中，请稍候...
```

#### 示例 2：翻唱并改变风格

```
用户：把刚才那首歌改成爵士风格

AI: 好的，我将把这首歌改编成爵士风格。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCover]
    [请求体] {
      "data": {
        "continue_clip_id": "c13975cda17449da2261",
        "tags": "Jazz",
        "model": "chirp-v5"
      }
    }
    
    ✅ 翻唱提交成功！任务编号：xxx，正在生成中，请稍候...
```

#### 示例 3：翻唱并修改歌词

```
用户：翻唱歌曲 0e66d6dd，用这段新歌词：
[Verse]
夜色温柔如水
星光点点相随

AI: 好的，我将使用新歌词翻唱这首歌。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCover]
    [请求体] {
      "data": {
        "continue_clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "prompt": "[Verse]\n夜色温柔如水\n星光点点相随",
        "model": "chirp-v5"
      }
    }
    
    ✅ 翻唱提交成功！任务编号：xxx，正在生成中，请稍候...
```

### ⚠️ 关键注意事项

1. **歌曲 ID 获取**
   - 歌曲 ID（clipId）从 API 2 查询歌曲状态的响应中获取
   - 响应字段中的 `id` 就是 clipId
   - 必须先查询歌曲状态，确认歌曲已完成（status = complete）后才能翻唱

2. **翻唱与原创的区别**
   - 翻唱会保持原歌曲的主旋律
   - 可以改变风格、歌词、音色等元素
   - 适合用于改编、提升音质、换风格等场景

3. **音色参数（高级功能）**
   - `persona_id` 和 `artist_clip_id` 用于指定特定音色
   - 这些参数需要通过 makePersona 任务预先获取
   - 如果不指定，系统会使用默认音色

4. **翻唱后的查询**
   - 翻唱成功后会返回新的 taskId
   - 使用 API 2 查询新任务的状态
   - 翻唱生成的是一首新歌曲，不会覆盖原歌曲

5. **推荐使用场景**
   - 改变歌曲风格（如流行改爵士）
   - 提升老歌音质
   - 使用不同音色演唱
   - 修改部分歌词但保持旋律

---

### API 5：合并续写歌曲

用途：续写歌曲生成后，通过此接口将续写片段与父歌曲合并成完整歌曲。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=concat
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "clip_id": "1c51baab-5085-4e2e-a1d8-c6a103a55488"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| clip_id | String | ✅ 是 | 续写歌曲的 id（通过 API 3 续写后生成的歌曲 id） |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": [
    {
      "taskId": "xxx"
    }
  ]
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Array | 任务数据数组 |
| data[].taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [合并] [拼接] [合成完整歌曲] 等意图时：

步骤 1：确认合并需求
  IF 用户提供了续写歌曲的 ID：
    clip_id = 用户提供的续写歌曲 ID
  ELSE IF 用户说"合并刚才续写的歌"：
    clip_id = 最近一次续写生成的歌曲 ID（从 API 3 的响应中获取）
  ELSE:
    询问用户："请提供要合并的续写歌曲 ID"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=concat
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "clip_id": clip_id
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data[0].taskId
    说："✅ 合并提交成功！任务编号：{taskId}，正在处理中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ 合并失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：续写后立即合并

```
用户：帮我续写歌曲 0e66d6dd，从第 7 秒开始

AI: [执行：POST https://ai.growingth.com/api/song/proxy?name=generateContinue]
    ✅ 续写提交成功！任务编号：1c51baab-5085-4e2e-a1d8-c6a103a55488，正在生成中...
    
    [等待生成完成后]
    🎵 续写完成！
    
用户：把续写的部分和原歌曲合并

AI: 好的，我将把续写片段与原歌曲合并成完整歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=concat]
    [请求体] {
      "data": {
        "clip_id": "1c51baab-5085-4e2e-a1d8-c6a103a55488"
      }
    }
    
    ✅ 合并提交成功！任务编号：xxx，正在处理中，请稍候...
```

#### 示例 2：合并指定的续写歌曲

```
用户：合并续写歌曲 1c51baab-5085-4e2e-a1d8-c6a103a55488

AI: 好的，我将合并这首续写歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=concat]
    [请求体] {
      "data": {
        "clip_id": "1c51baab-5085-4e2e-a1d8-c6a103a55488"
      }
    }
    
    ✅ 合并提交成功！任务编号：xxx，正在处理中，请稍候...
    
    [等待 10 秒后查询]
    🎵 合并完成！
    歌曲名：夏日微风（完整版）
    ▶️ 音频播放：https://cdn1.suno.ai/xxx.mp3 | 下载：https://cdn1.suno.ai/xxx.mp3
```

#### 示例 3：完整的续写+合并流程

```
用户：续写刚才那首歌，然后合并成完整版

AI: 好的，我先为您续写歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateContinue]
    ✅ 续写提交成功！任务编号：1c51baab，正在生成中...
    
    [等待生成完成]
    🎵 续写完成！现在开始合并...
    
    [执行：POST https://ai.growingth.com/api/song/proxy?name=concat]
    [请求体] {
      "data": {
        "clip_id": "1c51baab-5085-4e2e-a1d8-c6a103a55488"
      }
    }
    
    ✅ 合并提交成功！正在处理中...
    
    [等待合并完成]
    🎵 合并完成！完整歌曲已生成。
    ▶️ 音频播放：https://cdn1.suno.ai/xxx.mp3 | 下载：https://cdn1.suno.ai/xxx.mp3
```

### ⚠️ 关键注意事项

1. **合并前提条件**
   - 必须先通过 API 3 续写歌曲
   - 续写任务必须已完成（status = complete）
   - 使用续写生成的歌曲 ID（不是原歌曲 ID）

2. **clip_id 获取**
   - clip_id 是续写歌曲的 ID
   - 从 API 3 续写接口的响应中获取 taskId
   - 然后通过 API 2 查询该任务，获取生成的歌曲 id

3. **合并结果**
   - 合并会生成一首新的完整歌曲
   - 返回新的 taskId，需要通过 API 2 查询
   - 原歌曲和续写片段不会被删除

4. **推荐工作流程**
   ```
   1. 生成原歌曲（API 1）
   2. 续写歌曲（API 3）
   3. 查询续写状态（API 2）确认完成
   4. 合并歌曲（API 5）
   5. 查询合并结果（API 2）
   ```

5. **合并后的查询**
   - 合并成功后会返回新的 taskId
   - 使用 API 2 查询合并任务的状态
   - 合并完成后可以获取完整歌曲的播放链接

---

### API 6：生成视频

用途：为已生成的歌曲创建视频。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=generateVideo
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "title": "歌曲标题",
    "clip_id": "需生成视频的 clip id"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | String | ✅ 是 | 歌曲标题 |
| clip_id | String | ✅ 是 | 需生成视频的歌曲 clip id |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": {
    "taskId": "MBENVP5DFKOSPJHO"
  }
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Object | 任务数据对象 |
| data.taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [生成视频] [创建视频] [做个视频] [视频版] 等意图时：

步骤 1：确认视频生成需求
  IF 用户提供了歌曲 ID：
    clip_id = 用户提供的歌曲 ID
  ELSE IF 用户说"给刚才的歌生成视频"：
    clip_id = 最近一次生成的歌曲 ID（从查询结果中获取）
  ELSE:
    询问用户："请提供要生成视频的歌曲 ID"
    → 停止，等待用户回复
  
  获取歌曲标题：
  IF 已知歌曲标题（从之前的查询结果中）：
    title = 已知的歌曲标题
  ELSE:
    先调用 API 2 查询歌曲信息，获取标题

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=generateVideo
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "title": title,
        "clip_id": clip_id
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data.taskId
    说："✅ 视频生成提交成功！任务编号：{taskId}，正在生成中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ 视频生成失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：为指定歌曲生成视频

```
用户：帮我给歌曲 0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f 生成视频

AI: 好的，我先查询一下这首歌的信息。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f"
      }
    }
    
    查询到歌曲：Through the Fog
    
    现在开始生成视频...
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateVideo]
    [请求体] {
      "data": {
        "title": "Through the Fog",
        "clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f"
      }
    }
    
    ✅ 视频生成提交成功！任务编号：MBENVP5DFKOSPJHO，正在生成中，请稍候...
```

#### 示例 2：为刚才生成的歌曲创建视频

```
用户：给刚才那首歌生成一个视频

AI: 好的，我将为《夏日微风》生成视频。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateVideo]
    [请求体] {
      "data": {
        "title": "夏日微风",
        "clip_id": "c13975cda17449da2261"
      }
    }
    
    ✅ 视频生成提交成功！任务编号：MBENVP5DFKOSPJHO，正在生成中，请稍候...
    
    [等待 10 秒后查询]
    [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "c13975cda17449da2261"
      }
    }
    
    🎬 视频生成完成！
    歌曲id:123465
    歌曲名：夏日微风
    🎬 视频播放：https://cdn1.suno.ai/c13975cda17449da2261.mp4 | 下载：https://cdn1.suno.ai/c13975cda17449da2261.mp4
```

#### 示例 3：生成歌曲后立即创建视频

```
用户：帮我生成一首关于夏天的流行歌曲，然后做成视频

AI: 好的，我先为您创作歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中...
    
    [等待生成完成]
    🎵 歌曲生成完成！
    歌曲名：夏日微风
    歌曲id:123465
    现在开始生成视频...
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateVideo]
    [请求体] {
      "data": {
        "title": "夏日微风",
        "clip_id": "c13975cda17449da2261"
      }
    }
    
    ✅ 视频生成提交成功！正在处理中...
    
    [等待视频生成完成]
    🎬 视频生成完成！
    🎬 视频id:123465
    🎬 视频播放：https://cdn1.suno.ai/c13975cda17449da2261.mp4 | 下载：https://cdn1.suno.ai/c13975cda17449da2261.mp4
```

### ⚠️ 关键注意事项

1. **前提条件**
   - 必须先有已生成完成的歌曲（status = complete）
   - 需要知道歌曲的 clip_id 和 title

2. **clip_id 获取**
   - clip_id 从 API 2 查询歌曲状态的响应中获取
   - 响应字段中的 `id` 就是 clip_id

3. **title 参数**
   - 必须提供歌曲标题
   - 如果不知道标题，先调用 API 2 查询歌曲信息

4. **视频生成时间**
   - 视频生成通常需要较长时间
   - 建议等待 15-30 秒后再查询状态
   - 查询间隔仍然遵守 10 秒以上的规则

5. **查询视频结果**
   - 使用 API 2（getMusic）查询任务状态
   - 视频生成完成后，响应中会包含 `video_url` 字段
   - 如果 `video_url` 为空或不存在，说明视频还在生成中

6. **推荐使用场景**
   - 为已生成的歌曲创建视频版本
   - 分享到社交媒体时需要视频格式
   - 制作音乐MV

---

### API 7：生成 WAV 格式

用途：将歌曲转换为 WAV 无损音频格式。

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=makeWav
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "clipId": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| clipId | String | ✅ 是 | 歌曲 id（clip id） |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": {
    "taskId": "MBENVP5DFKOSPJHO"
  }
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Object | 任务数据对象 |
| data.taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [生成 WAV] [转换 WAV] [无损格式] [WAV 格式] 等意图时：

步骤 1：确认 WAV 生成需求
  IF 用户提供了歌曲 ID：
    clipId = 用户提供的歌曲 ID
  ELSE IF 用户说"把刚才的歌转成 WAV"：
    clipId = 最近一次生成的歌曲 ID（从查询结果中获取）
  ELSE:
    询问用户："请提供要转换的歌曲 ID"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=makeWav
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "clipId": clipId
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data.taskId
    说："✅ WAV 格式生成提交成功！任务编号：{taskId}，正在转换中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ WAV 格式生成失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：为指定歌曲生成 WAV 格式

```
用户：帮我把歌曲 0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f 转成 WAV 格式

AI: 好的，我将为这首歌生成 WAV 无损格式。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=makeWav]
    [请求体] {
      "data": {
        "clipId": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f"
      }
    }
    
    ✅ WAV 格式生成提交成功！任务编号：MBENVP5DFKOSPJHO，正在转换中，请稍候...
```

#### 示例 2：为刚才生成的歌曲转换格式

```
用户：把刚才那首歌转成 WAV 格式

AI: 好的，我将为《夏日微风》生成 WAV 无损格式。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=makeWav]
    [请求体] {
      "data": {
        "clipId": "c13975cda17449da2261"
      }
    }
    
    ✅ WAV 格式生成提交成功！任务编号：MBENVP5DFKOSPJHO，正在转换中，请稍候...
    
    [等待 10 秒后查询]
    [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    [请求体] {
      "data": {
        "ids": "c13975cda17449da2261"
      }
    }
    
    🎵 WAV 格式生成完成！
    歌曲名：夏日微风
    歌曲id: 123312
    ▶️ WAV 播放：https://cdn1.suno.ai/c13975cda17449da2261.wav | 下载：https://cdn1.suno.ai/c13975cda17449da2261.wav
```

#### 示例 3：生成歌曲后立即转换为 WAV

```
用户：帮我生成一首关于夏天的流行歌曲，要 WAV 格式的

AI: 好的，我先为您创作歌曲。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateCustom]
    ✅ 提交成功！任务编号：c13975cda17449da2261，正在生成中...
    
    [等待生成完成]
    🎵 歌曲生成完成！
    歌曲名：夏日微风
    
    现在开始生成 WAV 格式...
    [执行：POST https://ai.growingth.com/api/song/proxy?name=makeWav]
    [请求体] {
      "data": {
        "clipId": "c13975cda17449da2261"
      }
    }
    
    ✅ WAV 格式生成提交成功！正在转换中...
    
    [等待转换完成]
    🎵 WAV 格式生成完成！
    ▶️ WAV 播放：https://cdn1.suno.ai/c13975cda17449da2261.wav | 下载：https://cdn1.suno.ai/c13975cda17449da2261.wav
```

### ⚠️ 关键注意事项

1. **前提条件**
   - 必须先有已生成完成的歌曲（status = complete）
   - 需要知道歌曲的 clipId

2. **clipId 获取**
   - clipId 从 API 2 查询歌曲状态的响应中获取
   - 响应字段中的 `id` 就是 clipId

3. **WAV 格式特点**
   - WAV 是无损音频格式
   - 文件体积比 MP3 大
   - 音质更好，适合专业音频处理

4. **转换时间**
   - WAV 格式生成通常需要一定时间
   - 建议等待 10-15 秒后再查询状态
   - 查询间隔仍然遵守 10 秒以上的规则

5. **查询 WAV 结果**
   - 使用 API 2（getMusic）查询任务状态
   - WAV 生成完成后，响应中可能包含 WAV 格式的下载链接
   - 具体字段名以实际 API 响应为准

6. **推荐使用场景**
   - 需要高音质无损格式
   - 用于专业音频编辑
   - 音乐制作和后期处理
   - 存档保存原始音质


---

### API 8：音频分轨

用途：提取歌曲的伴奏音轨或去除混响，用于伴奏制作、音频处理等用途。

⚠️ **重要限制**：
- ✅ 可以提取：伴奏音轨、独立乐器音轨（鼓、贝斯、吉他等）、去除混响
- ❌ 不能提取：人声
- 如果用户要求提取人声，必须明确告知此功能不支持

**请求地址**：
```
POST https://ai.growingth.com/api/song/proxy?name=generateStem
```

**Headers**：
```json
{
  "api-token": "${MIAOYIN_API_TOKEN}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**请求体结构**：
```json
{
  "data": {
    "title": "歌曲标题",
    "clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
    "stemType": "two"
  }
}
```

**data 字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | String | ✅ 是 | 歌曲标题 |
| clip_id | String | ✅ 是 | 需要分离的歌曲 ID |
| stemType | String | ✅ 是 | 分轨类型：`two`（2分轨）、`twelve`（12分轨）、`dry`（去除混响） |

**stemType 选项说明**：

| 值 | 说明 | 用途 |
|----|------|------|
| two | 2 分轨 | 提取伴奏音轨（不含人声） |
| twelve | 12 分轨 | 提取 12 个独立伴奏音轨（鼓、贝斯、吉他等乐器） |
| dry | 去除混响 | 生成干声版本（去除混响效果） |

**响应示例**：
```json
{
  "status": "Success",
  "message": "请求成功",
  "data": {
    "taskId": "MBENVP5DFKOSPJHO"
  }
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | String | 请求状态：Success / Error |
| message | String | 响应消息 |
| data | Object | 任务数据对象 |
| data.taskId | String | 任务编号，用于后续查询 |

### 调用决策树（严格按此流程执行）

```
当用户表达 [分轨] [提取伴奏] [去混响] [干声] 等意图时：

⚠️ 重要：如果用户要求提取人声，必须明确告知：
  "抱歉，此功能只能提取伴奏音轨，不支持提取人声。"
  → 停止，不要调用 API

步骤 1：确认分轨需求
  IF 用户提供了歌曲 ID：
    clip_id = 用户提供的歌曲 ID
  ELSE IF 用户说"给刚才的歌分轨"：
    clip_id = 最近一次生成的歌曲 ID（从查询结果中获取）
  ELSE:
    询问用户："请提供要分轨的歌曲 ID"
    → 停止，等待用户回复
  
  获取歌曲标题：
  IF 已知歌曲标题（从之前的查询结果中）：
    title = 已知的歌曲标题
  ELSE:
    先调用 API 2 查询歌曲信息，获取标题
  
  确定分轨类型：
  IF 用户说"提取伴奏" 或 "只要伴奏"：
    stemType = "two"
  ELSE IF 用户说"12 分轨" 或 "详细分轨" 或 "分离所有乐器"：
    stemType = "twelve"
  ELSE IF 用户说"去混响" 或 "干声"：
    stemType = "dry"
  ELSE:
    询问用户："请选择分轨类型：
      1. 2 分轨（提取伴奏音轨）
      2. 12 分轨（提取 12 个独立乐器音轨）
      3. 去除混响（干声版本）"
    → 停止，等待用户回复

步骤 2：构建请求
  POST https://ai.growingth.com/api/song/proxy?name=generateStem
  Headers:
    api-token: ${MIAOYIN_API_TOKEN}
    Content-Type: application/json; charset=utf-8
  请求体:
    {
      "data": {
        "title": title,
        "clip_id": clip_id,
        "stemType": stemType
      }
    }

步骤 3：发送请求并处理响应
  IF response.status == "Success":
    taskId = response.data.taskId
    说："✅ 音频分轨提交成功！任务编号：{taskId}，正在处理中，请稍候..."
    → 转到 API 2 查询任务状态流程
  ELSE:
    说："❌ 音频分轨失败：{response.message}"
    → 转到 "错误处理流程"
```

### 完整对话示例

#### 示例 1：2 分轨（提取伴奏）

```
用户：帮我把歌曲 0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f 提取伴奏

AI: 好的，我先查询一下这首歌的信息。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=getMusic]
    查询到歌曲：Through the Fog
    
    现在开始提取伴奏音轨...
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateStem]
    [请求体] {
      "data": {
        "title": "Through the Fog",
        "clip_id": "0e66d6dd-7a55-4cd3-bc03-2ea11324ce3f",
        "stemType": "two"
      }
    }
    
    ✅ 音频分轨提交成功！任务编号：MBENVP5DFKOSPJHO，正在处理中，请稍候...
    
    [等待 10 秒后查询]
    🎵 伴奏提取完成！
    ▶️ 伴奏音轨 - 播放：https://cdn1.suno.ai/xxx-instrumental.mp3 | 下载：https://cdn1.suno.ai/xxx-instrumental.mp3
```

#### 示例 2：12 分轨（详细分离乐器）

```
用户：给刚才那首歌做 12 分轨

AI: 好的，我将为《夏日微风》进行 12 分轨处理，提取 12 个独立乐器音轨。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateStem]
    [请求体] {
      "data": {
        "title": "夏日微风",
        "clip_id": "c13975cda17449da2261",
        "stemType": "twelve"
      }
    }
    
    ✅ 音频分轨提交成功！任务编号：MBENVP5DFKOSPJHO，正在处理中...
    
    ⚠️ 注意：12 分轨处理时间较长，建议等待 30 秒以上再查询。
    
    [等待处理完成]
    🎵 12 分轨完成！
    已生成 12 个独立伴奏音轨：
    1. 鼓组
    2. 贝斯
    3. 吉他
    4. 钢琴
    5. 合成器
    6. 弦乐
    ... (共 12 个乐器音轨)
```

#### 示例 3：去除混响

```
用户：把这首歌的混响去掉，我要干声版本

AI: 好的，我将生成干声版本（去除混响）。
    [执行：POST https://ai.growingth.com/api/song/proxy?name=generateStem]
    [请求体] {
      "data": {
        "title": "夏日微风",
        "clip_id": "c13975cda17449da2261",
        "stemType": "dry"
      }
    }
    
    ✅ 音频分轨提交成功！任务编号：MBENVP5DFKOSPJHO，正在处理中，请稍候...
    
    [等待处理完成]
    🎵 干声版本生成完成！
    ▶️ 播放：https://cdn1.suno.ai/xxx-dry.mp3 | 下载：https://cdn1.suno.ai/xxx-dry.mp3
```

#### 示例 4：用户不确定分轨类型

```
用户：帮我给这首歌分轨

AI: 好的，请选择分轨类型：
    1. 2 分轨（提取伴奏音轨）- 适合制作伴奏
    2. 12 分轨（提取 12 个独立乐器音轨）- 适合专业混音和编曲
    3. 去除混响（干声版本）- 适合后期处理

用户：2 分轨

AI: 好的，我将提取伴奏音轨。
    [执行分轨流程...]
```

### ⚠️ 关键注意事项

1. **重要限制**
   - ⚠️ **此接口只能提取伴奏相关内容，不能提取人声**
   - 如果用户要求提取人声，请明确告知此功能不支持

2. **前提条件**
   - 必须先有已生成完成的歌曲（status = complete）
   - 需要知道歌曲的 clip_id 和 title

3. **clip_id 和 title 获取**
   - clip_id 从 API 2 查询歌曲状态的响应中获取
   - title 也从 API 2 的响应中获取
   - 如果不知道，先调用 API 2 查询

4. **分轨类型选择建议**
   - **2 分轨（two）**：
     - 最快速，适合大多数场景
     - 用途：提取伴奏音轨
   - **12 分轨（twelve）**：
     - 处理时间最长，文件最多
     - 用途：提取 12 个独立乐器音轨（鼓、贝斯、吉他等）
   - **去混响（dry）**：
     - 生成去除混响的版本
     - 用途：后期添加自定义混响、音频处理

5. **处理时间**
   - 2 分轨：建议等待 15-20 秒
   - 12 分轨：建议等待 30-60 秒（时间较长）
   - 去混响：建议等待 15-20 秒
   - 查询间隔仍然遵守 10 秒以上的规则

6. **查询分轨结果**
   - 使用 API 2（getMusic）查询任务状态
   - 2 分轨：返回伴奏音轨
   - 12 分轨：返回 12 个乐器音轨
   - 去混响：返回去除混响的版本
   - 具体返回结构以实际 API 响应为准

7. **推荐使用场景**
   - **2 分轨**：
     - 制作伴奏音轨
     - 简单的音频编辑
   - **12 分轨**：
     - 专业音乐制作
     - 重新混音
     - 学习编曲和配器
     - 提取特定乐器音轨
   - **去混响**：
     - 后期音频处理
     - 添加自定义效果
     - 音频修复和优化

8. **文件管理**
   - 12 分轨会生成大量文件，注意存储空间
   - 建议下载后妥善管理各个音轨文件
   - 每个音轨都有独立的下载链接
