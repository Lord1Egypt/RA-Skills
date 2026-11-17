---
name: 加豆AI
description: 企业级营销智能体平台，支持视频生成、AI商拍、数字人口播、商品场景图、商品海报、红笔记内容生成及抖音/TikTok/快手等社媒账号管理。当用户需要AIGC内容生成或社媒运营时调用本skill。
homepage: https://www.jiadouai.com
version: 1.1.0
privacy_policy: https://www.jiadouai.com/privacy
author: 微众互联科技
---

# 加豆AI 使用指南

## ⚠️ 安全与隐私

1. **敏感凭证**：Token 是敏感凭证，建议使用临时或最低权限 Token
2. **数据上报**：不支持的功能会上报到远程服务器，上报前会征得您的同意
3. **文件上传**：本地文件会上传到云存储(OSS)，请勿上传敏感内容（身份证、私密视频等）
4. **网络通信**：本skill 会与 `mcp.jiadouai.com` 通信，详见[隐私政策](https://www.jiadouai.com/privacy)

## ⚙️ 快速配置

首次使用需完成本地安装和鉴权，详见 `references/auth.md`。

## 🎯 场景路由表

| 场景     | 触发关键词                                                     | 工具                   | 参考                                                                |
| -------- | -------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------- |
| AI商拍   | 试衣服、换装、AI试穿、上身效果、穿上试试、帮我换装、虚拟试穿   | model_try_clothes      | references/model_try_clothes.md                                     |
| AI商拍   | 试鞋、上脚试试、上脚效果、鞋子上脚、鞋子看看、鞋子穿上         | shoes_dressing         | references/shoes_dressing.md                                        |
| AI商拍   | 生成模特、AI模特、模特图、虚拟人物、创建模特、给我个模特       | model_produce          | references/model_produce.md                                         |
| 商品图   | 商品场景、场景效果、换个背景、产品摆拍、放场景里、商品带场景   | business_product_scene | references/business_product_scene.md                                |
| 商品图   | 做海报、促销海报、活动海报、生成海报、给我做个海报、宣传海报   | business_poster        | references/business_poster.md                                       |
| 图文笔记 | 小红书配图、种草笔记、小红书图、做小红书图、红笔记、生成笔记图 | ice_design_image_xhs   | references/ice_design_image_xhs.md                                  |
| 社媒发布 | 发视频、发布视频、上传视频、发到抖音、发到快手、推送视频       | video_publish          | references/video_publish.md ⚠️ 需先调 account_page（传 `{}`）       |
| 社媒发布 | 发图文、发图片、发布照片、图文发布、发到小红书、图片发上去     | image_publish          | references/image_publish.md ⚠️ 需先调 account_page（传 `{}`）       |
| 视频生成 | 对口型、配音视频、口型同步、给视频配音、让视频说话、数字人口播 | ice_voice_video        | references/ice_voice_video.md                                       |
| 视频生成 | 照片唱歌、图片唱歌、唱歌视频、让照片唱歌、照片唱起来、图片演唱 | image_song             | references/image_song.md                                            |
| 视频生成 | 混剪、剪视频、素材混剪、帮我剪个视频、剪个视频、混剪出来       | ai_mixed_script        | references/ai_mixed_script.md                                       |
| 视频生成 | 视频复刻、模仿视频、同款视频、翻拍视频、拍个一样的、照着做     | ai_clone_video         | references/ai_clone_video.md                                        |
| 工具箱   | 解析链接、提取视频、抖音去水印、链接解析、获取地址、提取链接   | get_raw_url            | references/get_raw_url.md                                           |
| 工具箱   | 分析视频、视频分析、风格分析、拆解视频、分析一下、解析视频     | analyze_video          | references/analyze_video.md ⚠️ 双层判断：code=0 + data.success=true |

### 公共工具

| 工具                 | 说明                               | 参考                     |
| -------------------- | ---------------------------------- | ------------------------ |
| get_job_status       | 异步任务轮询                       | 见下方"异步任务轮询"章节 |
| account_page         | 获取已授权社媒账号（传 `{}` 即可） | references/workflows.md  |
| video_publish_status | 查询发布结果（视频和图文通用）     | references/workflows.md  |
| signature            | 获取 OSS 上传签名                  | references/workflows.md  |

## 🔧 调用方式

**执行调用**（正常流程，直接从 reference 确定参数）：

```bash
echo '<JSON参数>' | mcporter call ClawAgent.<工具名> --args -
```

**查看 Schema**（参数不确定、或返回报错提示参数不匹配时）：

```bash
mcporter list ClawAgent.<工具名> --schema --json
```

> 参数以 mcporter Schema 为准。reference 提供 Schema 无法表达的额外约束。

## 📡 全局API响应结构

- `code`: 状态码，`0` 成功，**任何非 `0` 值均表示异常**
- `msg`: 状态描述，成功时 `ok`，异常时含具体错误信息
- `data`: 响应数据，固定包含 `_id`（调用链追踪 ID）

## ⚡ 异常处理规则

当 `code != 0` 时：

1. 读取 `msg`，结合上下文分析失败原因
2. 临时性错误（网络超时、服务繁忙）→ 自动重试 1-2 次
3. 参数/权限/算力错误 → 主动告知用户原因和操作建议
4. **不要静默失败**：必须将错误信息和处理建议反馈给用户

## 📁 文件处理规范

### 文件来源识别

**公网URL**：

- 必须先验证可访问性：`curl -I --max-time 5 -L <URL>`
- HTTP 200 → 直接传入工具
- 403/401 → 告知"链接需要登录或权限"
- 404 → 告知"链接已失效"
- 超时/失败 → 告知"链接无法访问"

**本地文件路径**：

- 需上传到云存储获取公网URL，见下方[上传规则](#文件上传规则)

**引用文件**（@image、@file等）：

- 告知用户"请将文件保存到本地，提供完整路径"

**对话中直接上传的图片**：

- 告知用户"请右键保存图片，提供完整路径"

**绝对禁止**：

- ❌ 编造或猜测 URL/文件路径
- ❌ 使用示例 URL、占位符
- ❌ 未验证可访问性/存在性就调工具

### 文件上传规则

> 加豆AI 接口需要公网可访问 URL，本地文件必须先上传。

```bash
node upload.mjs <本地文件路径>
# 输出: IMPORT_READY / FILE_URL:<url> / FILE_SIZE:<size>
```

### 管道自动处理

当工具返回 `{"error": "need_upload", ...}` 时，直接 pipe 给上传脚本：

```bash
echo '<上面的JSON>' | node upload.mjs
# 上传完成后会输出 TOOL_NAME，用得到的 FILE_URL 继续调用
```

### 文件搜索限制

**禁止全系统搜索**：不允许 `find /`、`find /Users`、`find ~` 等。
**允许范围**：当前工作目录、下载目录、用户明确指定的目录。

## ⏳ 异步任务轮询

生成类工具返回 `_id` 后，需调用 `get_job_status` 轮询：

```bash
echo '{"id":"<任务_id>"}' | mcporter call ClawAgent.get_job_status --args -
```

- `status=processing/pending` → 等 5-10s 重试（最多 60 次）
- `status=complete/success` → 提取结果。图片类取 `urls`，视频类取 `videos`
- `status=failed/error` → 查看 `msg`

> ⚠️ 响应中是 `data._id`，但 `get_job_status` 入参名是 `id`（服务端不接受 `_` 开头的变量名）。发布类任务的结果在 `data` 数组里（不含 `urls`/`videos`），详见各发布工具的 reference。

## 🔍 问题定位指南

| 错误码            | 错误类型       | 解决                              |
| ----------------- | -------------- | --------------------------------- |
| 403 或 `code=403` | Token 鉴权失败 | 重新授权，见 `references/auth.md` |
| 80000000          | 算力不足       | 需购买算力                        |

## 🔄 SKILL 更新

每天使用前建议检查更新。**必须告知用户并获得同意**后才能执行：

1. 告知用户正在检查更新并征求意见
2. 用户同意后：`echo '{"version":"<当前版本>"}' | mcporter call ClawAgent.check_skill_update --args -`
3. 有新版本时展示 release_note，用户确认后按 instruction 执行更新

## 📋 核心规则

- 参数以 mcporter Schema 为准，reference 提供额外业务约束
- 不支持的功能需用户同意后上报（见 `references/unsupported_feature_reporting.md`）
- 文件/URL 必须先验证可达性再调用工具
