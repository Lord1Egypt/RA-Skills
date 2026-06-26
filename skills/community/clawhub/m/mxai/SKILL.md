---
name: mxai
description: mxai 创作助手，聚合多种 AI 图片和视频生成模型，以及 MJ（MidJourney）绘画。关键词：AI绘画、图片生成、视频生成、AI创作、mxai、MJ、MidJourney
version: 1.4.3
metadata:
  openclaw:
    requires:
      env:
        - MX_AI_API_KEY
    primaryEnv: MX_AI_API_KEY
    emoji: "🎬"
---

# 🎬 mxai 创作助手

通过 HTTP REST API 调用 mxai 服务（不是 MCP 协议）。所有交互都是标准的 HTTP 请求（GET/POST），返回 JSON 响应。

---

## ⛔ 强制规则（违反任何一条即为错误）

1. **只能使用下方定义的 HTTP REST API**。绝对不要尝试 MCP JSON-RPC、WebSocket 或任何其他协议
2. **禁止编造模型**：model 参数只能使用下方表格中列出的 slug 值，不得编造、猜测或组合任何不存在的 slug
3. **禁止编造参数值**：所有参数只能使用工具 schema 中定义的可选值，不确定时省略该参数让系统使用默认值
4. **禁止伪造结果**：任务结果必须来自 get_task_status 的真实返回，绝不能编造 URL、serial_no 或状态
5. **禁止跳过轮询**：提交生成任务后，必须调用 get_task_status 轮询直到 status=2（完成）或 status=3（失败），不得假装任务已完成
6. **展示规则**：图片完成时用 ![描述](真实URL) 内联展示；视频完成时提供可点击链接
7. **不确定时查询**：不确定用哪个模型时，先调用 list_models 获取真实列表，不要凭记忆回答
8. **严禁编造 API 响应**。如果 API 调用失败，直接告诉用户"调用失败"并附上错误信息，不要编造结果或提供"手动操作指南"
9. **严禁在 API 调用失败时建议用户去网页手动操作**。只需报告错误，让用户检查 API Key 或稍后重试
10. **严禁对 API Key 进行任何格式校验**（包括长度、字符类型、结构等）。无论 key 看起来多么"奇怪"，都必须直接调用 API 验证
11. **严禁添加 skill 文档中未提及的"优化"或"帮助"**。不要自行重试、不要自行解释错误原因、不要提供文档未规定的建议

---

## ⚠️ 调用前自检（每次对话必须逐项确认）

在调用任何 API 之前，请在心中默念：

- [ ] 我有 MX_AI_API_KEY 吗？
  → 没有：引导用户获取，不要尝试调用 API

- [ ] 用户的要求能用现有 API 实现吗？
  → 不能：直接说"抱歉，当前不支持此功能"，不要编造

- [ ] 我知道每个参数的含义和必填性吗？
  → 不确定：查阅下方 API 文档，不要猜测

- [ ] 我准备好处理可能的错误了吗？
  → 没有：先阅读"错误处理"章节

任何一项为"否"，都不要继续调用 API。

---

## 第一步：配置 API Key

设置环境变量 MX_AI_API_KEY：

- **Linux/macOS**: export MX_AI_API_KEY=nb_xxx
- **Windows PowerShell**: $env:MX_AI_API_KEY="nb_xxx"
- **Windows CMD**: set MX_AI_API_KEY=nb_xxx
- **Docker**: -e MX_AI_API_KEY=nb_xxx
- **.env 文件**: 写入 MX_AI_API_KEY=nb_xxx

⚠️ 任何能设置环境变量的方式都可以，不依赖特定平台。

### 获取 API Key

1. 访问 https://www.mxai.cn/home/#/mcp
2. 注册登录后创建密钥（nb_ 开头）
3. 复制密钥
4. ⚠️ 立刻保存，关闭后无法再查看

OpenClaw 配置：在 Skills 中找到 mxai，填入 MX_AI_API_KEY

---

## 第二步：开始创作

对话示例：
- 「帮我画一只在月光下奔跑的猫」→ 自动调用图片生成
- 「用 seedance 模型生成一段海浪视频」→ 自动调用视频生成
- 「帮我把这张照片变成视频」→ 图生视频（需提供图片）
- 「查一下刚才的图好了吗」→ 查询任务状态
- 「我还剩多少积分」→ 查询账户信息
- 「显示我最近的作品」→ 查看历史记录
- 「用MJ画一只猫」→ 调用 MJ 绘画（mj_draw）
- 「怎么使用MJ」→ 介绍 MJ 绘画功能和使用方法
- 「放大第2张图」→ MJ 后续操作（mj_action U2）
- 「把这张图做成MJ视频」→ MJ 视频生成（mj_video）
- 「分析一下这张图的描述词」→ MJ 图生文（mj_describe）
- 「把这两张图混合」→ MJ 混图（mj_blend）

---

## 图片输入说明

用户提供图片的三种方式，后端都支持：
- 在对话中直接发送/粘贴图片 → LLM 收到 base64 数据，直接传入 input_images / reference_image
- 提供图片 URL（如 https://example.com/photo.jpg）→ 直接传入 input_images / reference_image
- 先调用 upload 接口上传 → 拿到 key 后传入（适合同一张图多次使用）

当用户请求需要图片的功能（如图生视频）但未提供图片时，必须主动提示：
"这个功能需要一张图片，请发送图片或提供图片链接。"
不要在没有图片的情况下强行调用 generate 接口。

---

## 工具调用流程

生成图片：generate_image → 循环调用 get_task_status（间隔5秒）→ 展示结果
生成视频：generate_video → 循环调用 get_task_status（间隔10秒）→ 展示结果
查询信息：get_user_info（积分余额）、list_models（可用模型）、get_my_tasks（历史记录）

### MJ（MidJourney）绘画

MJ 是一套独立的绘画工具，与上面的 generate_image/generate_video 并列。当用户明确提到"MJ"、"MidJourney"时使用 MJ 工具。

**MJ 工具一览：**

| 工具 | 用途 | 最简调用 |
|------|------|----------|
| mj_draw | MJ 风格绘画 | 只需 prompt |
| mj_action | 四宫格后续操作（放大/变幻/重绘等） | serial_no + action |
| mj_video | MJ 视频生成 | prompt + image（首帧） |
| mj_describe | 图生文（分析图片生成描述词） | image |
| mj_blend | 混图（多图融合） | images（至少2张） |

**MJ 绘画流程：**
1. mj_draw（传 prompt）→ 返回 serial_no → 轮询 get_task_status → 得到四宫格图片
2. 用户选择喜欢的图 → mj_action（传 serial_no + "U1"~"U4" 放大）→ 轮询 → 得到高清大图
3. 不满意？→ mj_action（传 serial_no + "REROLL" 重新生成）

**MJ 积分参考：**
- 普通模式：非VIP 4积分，普通VIP 1积分，高级VIP 免费
- 快速模式：4积分
- 极速模式：8积分（仅 MJ 7.0）
- 草稿模式：2积分（仅 MJ 7.0）
- MJ 视频：普通 20积分/个，快速 40积分/个

**MJ 模型：**
- 模型列表从后端动态获取，使用 list_models(type="mj") 或 /mcp/api/models?type=mj 查看
- model 参数直接传后端返回的模型名称或 ID 即可
- 常用：V7.0(细节优化)（ID:7）、V6.1(真实纹理)（ID:8，默认）、NJ7.0（ID:10，卡通）
- 也支持简写：MJ 7.0、NJ 6.0 等

**当用户问"怎么使用MJ"时，回答：**
MJ（MidJourney）是一款高质量 AI 绘画工具。使用方法很简单：
1. 告诉我你想画什么，比如"用MJ画一只在星空下奔跑的猫"
2. 我会生成一张四宫格图片（4张候选图）
3. 选择你喜欢的那张，说"放大第X张"即可获得高清大图
4. 不满意可以说"重新生成"

高级玩法：可以调整比例（16:9横版、9:16竖版）、速度模式、风格化程度等参数。

---

## 图片模型（model 参数只能填 slug 列的值）

默认模型：seedream-5.0-pro

| slug | 名称 | 积分 |
|------|------|------|
| `seedream-3.0` | 即梦3.0 | 2积分（VIP）/ 4积分 |
| `seedream-4.0` | 即梦4.0 | 4-6积分（VIP） |
| `seedream-4.5` | 即梦4.5 | 4-6积分（VIP） |
| `seedream-5.0` | 即梦5.0标准版 | 4积分（VIP）/ 8积分 |
| `seedream-5.0-pro` | 即梦5.0Pro | 6-20积分（VIP） |
| `nano-1.0` | Nano 1.0 | 3积分（VIP）/ 6积分 |
| `nano-2.0` | Nano 2.0 | 4-8积分（VIP） |
| `nano-2.0-pro` | Nano 2.0 Pro | 4-12积分（VIP） |

## 视频模型（model 参数只能填 slug 列的值）

默认模型：seedance-3.5-pro

| slug | 名称 | 积分 |
|------|------|------|
| `seedance-3.0` | 即梦视频3.0标准版 | 4-12积分 |
| `seedance-3.0-pro` | 即梦视频3.0Pro | 5-40积分 |
| `seedance-3.5` | 即梦视频3.5标准版 | 10-25积分 |
| `seedance-3.5-pro` | 即梦视频3.5Pro | 10-80积分 |
| `sora-2` | Sora 2 基础版 | 10-15积分 |
| `sora-2-emergency` | Sora 2 应急版 | 20积分 |
| `sora-2-economy` | Sora 2 特价官转 | 20-60积分 |
| `sora-2-stable` | Sora 2 稳定官转 | 50-150积分 |
| `sora-2-pro` | Sora 2 Pro | 60-65积分 |
| `kling-1.5` | KLING 1.5 | 40-140积分 |
| `kling-1.6` | KLING 1.6 | 40-140积分 |
| `kling-2.1-master` | KLING 2.1大师版 | 200-400积分 |
| `kling-2.1-lite` | KLING 2.1精简版 | 40-140积分 |
| `kling-2.5` | KLING 2.5 | 50-100积分 |
| `kling-2.6` | KLING 2.6 | 30-200积分 |

---

## API 调用规范

**Base URL**: https://mcp.mxai.cn

**认证 Header**: Authorization: Bearer ${MX_AI_API_KEY} 或 Query ?key=${MX_AI_API_KEY}

**格式**: JSON

**编码**: UTF-8（请求体必须使用 UTF-8 编码，中文直接传入）

**网络**: 自动使用系统代理（HTTP_PROXY/HTTPS_PROXY）

**超时**: 默认 30 秒，查询任务状态可延长至 60 秒

⚠️ 重要：这是标准 HTTP REST API，不是 MCP JSON-RPC。直接发 HTTP 请求即可。

---

### API 1：查询账户信息

用途：用户询问积分、余额、会员状态时调用。

GET /mcp/api/user

返回字段：昵称、会员状态、积分余额、积分参考

---

### API 2：查看可用模型

用途：用户想了解有哪些模型时调用。

GET /mcp/api/models?type={image|video}

- type（可选）：image 或 video，不填返回所有
- 返回字段：models 数组（含 name/slug/type/description/cost_hint）、total

---

### API 3：生成图片（核心接口）

用途：用户想生成图片时调用。

#### 调用决策树

当用户表达 [生成图片] [画一张] [帮我画] 等意图时：

步骤 1：确认需求
  IF 用户提供了描述（如"帮我画一只猫"）：
    prompt = 用户的描述
  ELSE：
    询问用户："请描述您想要生成的图片内容"
    → 停止，等待用户回复

  IF 用户想用参考图但未提供图片：
    询问用户："请发送参考图片或提供图片链接"
    → 停止，等待用户回复

步骤 2：构建请求
  POST /mcp/api/generate/image

步骤 3：发送请求并处理响应
  IF response 成功：
    serialNo = response.serial_no
    说："✅ 提交成功！正在生成中，请稍候..."
    转到 "API 5：查询任务状态" 流程
  ELSE：
    转到 "错误处理" 流程

#### 请求体字段

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | 是 | 图片描述 |
| model | 否 | 模型 slug（默认 seedream-5.0-pro），只能使用上方图片模型表格中的 slug |
| aspect_ratio | 否 | 1:1 / 16:9 / 9:16 / 4:3 / 3:4 / 3:2 / 2:3 / auto |
| resolution | 否 | 1K / 2K（默认）/ 4K |
| input_images | 否 | 参考图片数组（URL / base64 / 已上传的 key） |

#### 响应字段

| 字段 | 说明 |
|------|------|
| serial_no | 任务编号（用于轮询） |
| model | 使用的模型 |
| message | 提交结果消息 |

提交后必须立即轮询 get_task_status 直到完成。

---

### API 4：生成视频（核心接口）

用途：用户想生成视频时调用。

#### 调用决策树

当用户表达 [生成视频] [做个视频] [图片变视频] 等意图时：

步骤 1：确认需求
  IF 用户提供了描述：
    prompt = 用户的描述
  ELSE：
    询问用户："请描述您想要生成的视频内容"
    → 停止，等待用户回复

  IF 用户想做图生视频但未提供图片：
    询问用户："图生视频需要一张参考图片，请发送图片或提供图片链接"
    → 停止，等待用户回复

步骤 2：构建请求
  POST /mcp/api/generate/video

步骤 3：发送请求并处理响应
  IF response 成功：
    serialNo = response.serial_no
    说："✅ 提交成功！视频生成中，请稍候..."
    转到 "API 5：查询任务状态" 流程
  ELSE：
    转到 "错误处理" 流程

#### 请求体字段

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | 是 | 视频描述 |
| model | 否 | 模型 slug（默认 seedance-3.5-pro），只能使用上方视频模型表格中的 slug |
| aspect_ratio | 否 | 16:9 / 9:16 / 1:1 |
| duration | 否 | 时长秒数（常用 5 / 10） |
| resolution | 否 | 480p / 720p / 1080p |
| reference_image | 否 | 参考图片（提供后自动切换为图生视频） |
| end_frame_image | 否 | 尾帧图片（部分模型支持） |

#### 响应字段

| 字段 | 说明 |
|------|------|
| serial_no | 任务编号 |
| model | 使用的模型 |
| mode | 文生视频 / 图生视频 |
| message | 提交结果消息 |

提交后必须立即轮询 get_task_status 直到完成。

---

### API 5：查询任务状态

用途：查询生成进度，或生成后轮询。

#### 调用决策树

步骤 1：确定要查询的任务编号
  IF 是刚生成的任务：
    serialNo = 上一步返回的 serial_no
  ELSE IF 用户提供了编号：
    serialNo = 用户提供的编号
  ELSE IF 用户说"刚才的图/最近的任务"：
    serialNo = 最近一次提交的任务编号（从上下文记忆）
  ELSE：
    询问用户："请问要查询哪个任务？请提供任务编号"
    → 停止，等待用户回复

步骤 2：发送请求
  GET /mcp/api/task/{serial_no}

步骤 3：处理响应
  IF status == 2（已完成）：
    图片任务 → 用 ![描述](URL) 内联展示 image_urls 中的每张图
    视频任务 → 提供 video_url 可点击链接
  ELSE IF status == 0 或 1（排队/生成中）：
    等待后重试（图片间隔 5 秒，视频间隔 10 秒）
    继续轮询直到完成或失败
  ELSE IF status == 3（失败）：
    展示 fail_msg 失败原因，不要重试

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| serial_no | string | 任务编号 |
| status | number | 0=排队中 / 1=生成中 / 2=已完成 / 3=失败 |
| status_text | string | 状态文本描述 |
| prompt | string | 原始提示词 |
| image_urls | array | 图片 URL 数组（仅图片任务 status=2 时有值） |
| video_url | string | 视频 URL（仅视频任务 status=2 时有值） |
| fail_msg | string | 失败原因（仅 status=3 时有值） |

---

### API 6：上传图片

用途：上传图片供后续使用。

POST /mcp/api/upload

| 参数 | 必填 | 说明 |
|------|------|------|
| image | 是 | 图片 URL 或 base64 |

返回字段：key（OSS key，可在 generate 接口的 input_images / reference_image 中复用）

⚠️ generate 接口已支持直接传入图片，一般无需单独调用。

---

### API 7：查看历史记录

用途：用户查看历史生成记录。

GET /mcp/api/tasks?type={image|video}&status={0|1|2|3}&page=1&limit=10

- type（可选）：image 或 video
- status（可选）：0=排队中 / 1=生成中 / 2=已完成 / 3=失败
- page（可选）：页码，默认 1
- limit（可选）：每页数量，默认 10，最大 20
- 返回字段：total、current_page、last_page、page_size、list 数组

---

### API 8：MJ 绘画（MidJourney 风格）

用途：用户想用 MJ/MidJourney 风格绘画时调用。

#### 调用决策树

当用户表达 [用MJ画] [MidJourney绘画] [MJ风格] 等意图时：

步骤 1：确认需求
  IF 用户提供了描述：
    prompt = 用户的描述
  ELSE：
    询问用户："请描述您想要的图片效果"
    → 停止，等待用户回复

步骤 2：构建请求
  POST /mcp/api/mj/draw

步骤 3：发送请求并处理响应
  IF response 成功：
    serialNo = response.serial_no
    说："✅ MJ 绘画任务已提交！正在生成中..."
    转到 "API 5：查询任务状态" 流程
  ELSE：
    转到 "错误处理" 流程

#### 请求体字段

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | 是 | 描述词，支持中英文混合，建议详细描述以获得更好效果 |
| model | 否 | 模型名称或 ID（默认 V6.1），先调 /mcp/api/models?type=mj 查看可用模型，直接传返回的名称或 ID |
| aspect_ratio | 否 | 1:1（默认）/ 1:2 / 16:9 / 9:16 / 4:3 / 3:4 / 3:2 / 2:3 |
| speed | 否 | normal / fast（默认）/ turbo（仅MJ7.0）/ draft（仅MJ7.0） |
| quality | 否 | 质量化 0~100，默认 100 |
| stylize | 否 | 风格化 0~1000，默认 100（MJ 7.0 不支持） |
| chaos | 否 | 多样化 0~100，默认 0 |
| iw | 否 | 图片权重 0.25~2.0，默认 1.25（仅有参考图时生效） |
| sref | 否 | 风格参考权重 |
| cref | 否 | 角色参考 |
| oref | 否 | 物体参考 |
| input_images | 否 | 参考图片数组（URL / base64） |
| public | 否 | 是否公开作品，默认 false |

---

### API 9：MJ 后续操作

用途：对 MJ 四宫格图片执行放大、变幻等操作。

POST /mcp/api/mj/action

| 参数 | 必填 | 说明 |
|------|------|------|
| serial_no | 是 | 原始任务序列号 |
| action | 是 | 操作类型（见下方） |

操作类型：
- U1~U4：放大第1~4张图（左上=1，右上=2，左下=3，右下=4）
- V1~V4：变幻第1~4张图
- REROLL：重新生成
- STRONG/SUBTLE：强/弱变幻
- ZOOM15/ZOOM20：缩放
- LEFT/RIGHT/UP/DOWN：平移
- EXTEND：扩展

---

### API 10：MJ 视频

用途：MJ 视频生成（需要首帧图片）。

POST /mcp/api/mj/video

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | 是 | 视频描述 |
| image | 是 | 首帧图片（URL / base64） |
| speed | 否 | normal（默认）/ fast |
| count | 否 | 视频数量 1（默认）/ 2 / 4 |
| motion | 否 | 动作幅度 low（默认）/ high |
| loop | 否 | 是否循环，默认 false |
| end_image | 否 | 尾帧图片 |

---

### API 11：MJ 图生文

用途：上传图片获取 MJ 风格描述词。

POST /mcp/api/mj/describe

| 参数 | 必填 | 说明 |
|------|------|------|
| image | 是 | 图片（URL / base64） |

---

### API 12：MJ 混图

用途：多图混合融合。

POST /mcp/api/mj/blend

| 参数 | 必填 | 说明 |
|------|------|------|
| images | 是 | 图片数组，至少 2 张（URL / base64） |

---

## 错误提示模板（必须原样使用，不准修改）

| HTTP 状态码 | 提示语 |
|-------------|--------|
| 401/403 | "API Key 无效或已过期，请检查 MX_AI_API_KEY 配置" |
| 5xx | "请求服务器异常，请稍后重试" |
| 超时 | "请求超时，请稍后重试" |
| 网络错误 | "网络连接失败，请检查网络或代理设置" |

⚠️ 禁止使用其他表述，禁止添加"可能原因"、"建议检查"等额外内容。

---

## 详细错误日志输出（任何 HTTP 请求失败时必须执行）

除了展示上述用户友好的提示外，还必须输出详细的技术日志供排查问题。

### 需要输出的信息

| 类别 | 信息内容 | 说明 |
|------|----------|------|
| 请求信息 | HTTP 方法 | GET/POST |
| | URL（不含 query 参数） | 如 https://mcp.mxai.cn/mcp/api/user |
| | Header（隐藏 Authorization） | Authorization 显示为 Bearer nb_******** |
| | 请求体（隐藏 key） | 如有 key 相关字段，用 ******** 替换 |
| 响应信息 | HTTP 状态码 | 如 401、500 |
| | 响应头 | 完整展示 |
| | 响应体 | 完整展示，即使是错误信息 |
| 错误信息 | 错误类型 | 如 NetworkError、TimeoutError |
| | 错误消息 | 完整的错误文本 |

### 敏感信息隐藏规则

- Authorization: Bearer nb_xxxxxxxxxx → Authorization: Bearer nb_********
- 任何 nb_ 开头的字符串 → nb_********
- MX_AI_API_KEY 环境变量的完整值 → ********

### 日志输出格式

使用代码块包裹详细日志，格式如下：

=== 错误详情 ===
请求：POST https://mcp.mxai.cn/mcp/api/generate/image
状态码：503
错误：请求服务器异常

--- 请求头 ---
Content-Type: application/json
Authorization: Bearer nb_********

--- 响应头 ---
Content-Type: application/json

--- 响应体 ---
{"error": "Service Unavailable", "message": "Please try again later"}

⚠️ 详细日志仅供技术排查，不要让普通用户误解。先展示用户友好提示，再展示详细日志。

---

## 版本

- **Skill 版本**: 1.4.3
- **API 版本**: 以 https://mcp.mxai.cn/mcp/skill/version 返回为准
- **兼容性**: 不假设 API 格式固定，以实际响应为准

如果 API 响应包含未预期的字段，原样展示，不要报错。

升级提示：如果之前安装过旧版（文件夹名为 mx-ai-studio），请先删除旧文件夹再安装新版，避免两个 skill 共存冲突。

版本检查：GET https://mcp.mxai.cn/mcp/skill/version
如果 latest_version 高于 1.4.3，告知用户有新版本。
