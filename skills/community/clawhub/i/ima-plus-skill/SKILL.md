---
name: ima_plus-skill
description: IMA 知识库与笔记操作技能（版本 v1.0.12）：用 `--path` 自然语言定位知识库/文件夹/笔记本，支持文件上传、知识库/目录导出 zip、文件夹与条目管理、标签权限、网页入库、笔记增改与插图，以及把本地视频封装成单文件 HTML（页面内置「导出视频」，导出为 .bin 后缀、改名 .mp4 即播放）入库（需环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY）。
allowed-tools: Bash,Read
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins:
        - node
      env:
        - IMA_OPENAPI_CLIENTID
        - IMA_OPENAPI_APIKEY
      primaryEnv: IMA_OPENAPI_CLIENTID
  security:
    credentials_usage: |
      This skill requires user-provisioned IMA OpenAPI credentials (Client ID and API Key)
      to authenticate with the official IMA API at https://ima.qq.com.
      Credentials are ONLY sent to the official IMA API endpoint (ima.qq.com) as HTTP headers.
      The request base URL is hard-whitelisted to ima.qq.com: options.baseUrl / IMA_BASE_URL
      overrides are rejected unless they resolve to ima.qq.com, so credentials can never be
      forwarded to an arbitrary host.
      The file-upload flow also sends requests to COS endpoints (*.myqcloud.com) using
      short-lived, scoped temporary credentials returned by the IMA API (create_media);
      the user's Client ID / API Key are never sent to COS, and COS temporary credentials are
      passed to the upload helper via environment variables (not argv).
      No credentials are logged, stored in files, or transmitted to any other destination.
    allowed_domains:
      - ima.qq.com
      - '*.myqcloud.com'
---
# ima_plus-skill

> **版本：V1.0.12**
>
> **运行环境**：Node.js ≥ 18.0.0（所有 .cjs 脚本 + inline JSON 解析依赖）；视频模块另需 `python3` + `curl`（`ffprobe` 可选，取时长）

Unified IMA OpenAPI skill. Currently supports: **notes**, **knowledge-base**, **video**（视频链接 → 内嵌 HTML → 入库）.

## ⛔ MANDATORY RULES — read before ANY operation

0. **自然语言路径优先（所有模块通用，强制）：** 用户给出知识库/文件夹/笔记本的名称或路径（如"我的知识库/项目/文档"、"存到学习笔记"）时，**一律用解析器自动转 ID，禁止让用户提供 kb_id / folder_id**。知识库用根目录 `resolve_path.cjs --path`，笔记本用 `notes/scripts/resolve_notebook.cjs --path`。面向用户永远只展示名称，禁止暴露任何 ID。
   - ⛔ **禁止擅自使用 `--kb <kb_id>`**：即使解析过程中拿到了 kb_id，**也不得主动用它调用脚本**——所有脚本调用一律走 `--path "知识库名/文件夹..."`（内部自动解析）。`--kb` 仅在**用户明确要求使用某个具体 ID** 时才允许出现。违反此规则视为流程错误。
   - 兼容参数 `--kb-name`（按名称匹配）可以正常使用，但 `--path` 是首选。

### 🔧 路径解析缓存机制（V1.0.8+，无需手动管理）

解析器会把「知识库名 → kb_id、文件夹路径 → folder_id」**分层树状持久化**到缓存文件，
按「知识库 → 子文件夹 → 孙文件夹」嵌套，同名文件夹在不同库/不同父目录各占节点，不会串库。

**缓存位置（强制检查，安装 skill 时必须确定）：**
1. 环境变量 `IMA_RESOLVE_CACHE` 显式指定（所有环境，优先级最高）
2. ima.copilot 环境未设置时默认 `/sandbox/workspace/.ima_cache/resolve_cache.json`（workspace 持久、平台不重置）
3. **其他 agent / 自建环境未设置 `IMA_RESOLVE_CACHE` → 直接报错不可用**（与凭证同等强制）。
   安装时须先设置：`export IMA_RESOLVE_CACHE=/path/to/resolve_cache.json`（可写入 ~/.bashrc 或 ~/.zshrc）

- **无过期时间**：缓存长期有效；重复解析同一路径 **0 次 API 调用**（部分命中只补查缺失层级）。
- **失效自愈**：所有消费脚本已包 `withPathRetry`——若操作因「目标不存在」（如库/夹被删或改名，`220001/invalid/不存在` 类）失败，自动失效该路径缓存 → 全 API 重新解析 → 重试一次；**重查任一层失败即报「目录位置不存在」，整个操作直接中止，不猜测后续层级**。权限（220030）/限流（200001）类错误不触发自愈。
- **手动清缓存**（一般不需要）：删除缓存文件即可，下次解析自动重建。知识库/文件夹被删除后首次操作会自愈恢复。
- 笔记本解析（`--notes` / `resolve_notebook.cjs`）同样缓存（`notebooks` 节）。

1. **UTF-8 encoding (notes writes only):** Before calling `import_doc` or `append_doc`, ALL string fields (`content`, `title`) MUST be validated as legal UTF-8. Non-UTF-8 content causes irreversible garbled text. See `references/platform-notes.md` for platform-specific methods.
2. **File upload naming:** `title` MUST equal `file_name` (with extension). Never rename, shorten, translate, or modify the original filename.
3. **Unsupported file types:** Reject immediately with a clear message. Do NOT ask user "do you still want to try?" **视频文件（mp4/avi/mov/mkv…）不能作为文件直接上传**——必须走视频模块转成「内嵌单文件 HTML」再上传（见 § 📹 视频模块，细则读 `video/SKILL.md`）；Bilibili / YouTube URL 与 `file://` URL 仍不支持，引导用户改用 IMA 客户端。
4. **File upload integrity:** Keep file content as-is during upload. No encoding conversion for binary files (PDF, images, Excel, etc.).
5. **PowerShell 5.1 (all modules):** If running in PowerShell, detect version before first API call. PS 5.1 silently converts request Body to GBK — must use UTF-8 byte array mode. See `references/platform-notes.md`.
6. **副作用操作必须显式确认（不得自行执行）：** `join_knowledge`（真实加入公开库）、`tag_delete` / `tag_rename`（不可逆；新名已存在时自动合并）、`update_knowledge_base_permission`（影响全库成员）、`append_doc` 追加已有笔记（不可撤销修改）——调用前必须得到用户明确同意，不确定时先问。

## 🚀 高频操作快查表（30 秒上手）

| 用户意图 | 直接执行 |
| --- | --- |
| 上传文件到知识库 | `node knowledge-base/scripts/upload_to_kb.cjs --path "库名/文件夹" --file <路径>` |
| 打包知识库/文件夹为 zip | `node knowledge-base/scripts/export_kb_zip.cjs --path "库名/文件夹" --out /path/out.zip` |
| 列出知识库内容 | `node knowledge-base/scripts/list_all_files.cjs --path "库名"` |
| 创建文件夹 | `node knowledge-base/scripts/create_folder.cjs --path "库名/父夹" --name "新夹"` |
| 新建笔记 | `node notes/scripts/notes_create.cjs --content "内容" --path "笔记本名"` |
| 追加笔记 | `node notes/scripts/notes_append.cjs --note-id <id> --content "内容"` |
| 笔记插入图片 | `node notes/scripts/note-images.cjs --note-id <id> --file <md>` |
| 本地视频批量封装为 HTML 并入库 | `python3 video/scripts/video_batch.py --dir <视频目录> --path "<知识库>/<文件夹>"` |

> 路径一律用 `--path "知识库名/文件夹..."` 自然语言，禁止 kb_id。其余操作见各模块 SKILL.md 与脚本头部 Usage 注释。

## 📹 视频模块（V1.0.10 新增；V1.0.12 起 HTML 导出为 .bin）

把**本地视频文件**批量封装为「内嵌单文件 HTML」并上传到知识库文件夹。
**只做封装与上传，不做下载**（视频文件不能直接上传知识库——服务端限制）。

```bash
python3 video/scripts/video_batch.py --dir <视频目录> --path "<知识库>/<文件夹>"
```

- HTML **超过 10MB 自动丢弃、不上传**；文件名不加序号，并清洗 `# ? & /` 等 URL 危险字符
- 页面浅色极简（标题 + 视频），多端适配，兼容 iOS 12 Safari
- **页面内置「导出视频」链接**：点击下载 `<标题>.bin`（blob + `application/octet-stream`）；手机浏览器按后缀拦 `.mp4`，故存为 `.bin`，页面提示改名为 `.mp4` 即可播放
- **参数、行为约定、排障 → 见 `video/SKILL.md`**

## 模块决策表

| 用户意图                                                                                   | 模块           | 读取                      |
| ------------------------------------------------------------------------------------------ | -------------- | ------------------------- |
| 搜索笔记、浏览笔记本、获取笔记内容、创建笔记、追加内容                                     | notes          | `notes/SKILL.md`          |
| 上传文件、添加网页链接、搜索知识库、浏览知识库内容、获取知识库信息、获取可添加的知识库列表 | knowledge-base | `knowledge-base/SKILL.md` |
| 查看原文、分析原文、导出原文（需要 media_id）                                              | knowledge-base | `knowledge-base/SKILL.md` |
| 打包知识库 / 某个文件夹 / 多个文件为 zip 并发给用户                                         | knowledge-base | `knowledge-base/SKILL.md` |
| 把本地视频批量转换成 HTML 并上传到知识库文件夹 | video | `video/SKILL.md` |

### ⚠️ 易混淆场景

| 用户说的                                                 | 实际意图                 | 正确路由                                                    |
| -------------------------------------------------------- | ------------------------ | ----------------------------------------------------------- |
| "把这段内容添加到知识库XX里的笔记YY"                     | 往已有**笔记**追加内容   | **notes** — 先搜索笔记获取 `note_id`，再用 `append_doc`     |
| "把这个写到XX笔记里"、"记到XX笔记"                       | 往已有**笔记**追加内容   | **notes** — `append_doc`                                    |
| "把这篇笔记添加到知识库"                                 | 将笔记关联到**知识库**   | **knowledge-base** — `add_knowledge` with `media_type=11`   |
| "上传文件到知识库"                                       | 上传**文件**到知识库     | **knowledge-base** — `create_media` → COS → `add_knowledge` |
| "新建一篇笔记记录这些内容"                               | **创建**新笔记           | **notes** — `import_doc`                                    |
| "帮我记一下"、"记录一下"、"保存为笔记"（未指定已有笔记） | 意图不明确，**需要确认** | **notes** — 先询问用户是创建新笔记还是追加到哪篇已有笔记    |
| "添加到笔记里"（未指定具体哪篇）                         | 意图不明确，**需要确认** | **notes** — 先询问用户是创建新笔记还是追加到哪篇已有笔记    |

### ⚠️ 跨模块任务 — 必须读取两个子模块

某些意图跨越 notes 和 knowledge-base 两个模块。**不要只读取一个子模块就开始执行**，必须先读取两个模块的 SKILL.md 再按顺序操作。

| 用户说的                             | 实际流程                                      | 读取顺序                                               |
| ------------------------------------ | --------------------------------------------- | ------------------------------------------------------ |
| "把知识库里的XX内容记到笔记"         | KB 搜索/读取 → Notes 创建/追加                | 先读 `knowledge-base/SKILL.md` → 再读 `notes/SKILL.md` |
| "查看原文"（知识库中的笔记类型媒体） | KB `get_media_info` → Notes `get_doc_content` | 先读 `knowledge-base/SKILL.md` → 再读 `notes/SKILL.md` |
| "把这篇笔记添加到知识库"             | Notes 搜索获取 note_id → KB `add_knowledge`   | 先读 `notes/SKILL.md` → 再读 `knowledge-base/SKILL.md` |

**规则**：如果用户意图同时涉及「笔记」和「知识库」，或者 API 响应揭示需要另一个模块（如 `media_type=11` 表示笔记类型），必须读取两个子模块再继续。

**核心判断规则**：

- 目标是**笔记的内容**（读、写、追加）→ notes 模块
- 目标是**知识库的条目**（上传文件、添加链接、关联笔记到知识库）→ knowledge-base 模块
- 目标是**获取知识库条目的原始内容**（查看原文、分析原文、导出原文）→ knowledge-base 模块（若原文是笔记，会跨模块到 notes `get_doc_content`）
- 用户提到"知识库"只是在**描述笔记的位置**（如"知识库里的那篇笔记"），真正操作对象仍是笔记 → notes 模块
- 向笔记插入图片（本地/远程）必须由 notes 模块的 `note-images.cjs` 完成，**不得**调用 knowledge-base 的 `create_media` / `add_knowledge` / `get_media_info` 代替

## ⚠️ 出错时查这里（按需读取）

遇到后端错误码（`220030` / `51` / `210039` / `220001` 等）或任何异常现象，**先读 `references/troubleshooting.md`** 对照定位——那里汇总了全部实测沉淀的错误码对照表、权限边界、批量导出 SOP 与已知坑。正常执行时无需读取该文件。

## ⚙️ 安装配置总览（必读）

安装本 skill 只需配置 **两件事**（均为环境变量，强制设置，不设置无法使用）：

| # | 配置项 | 环境变量 | 未设置时 |
|---|--------|----------|----------|
| 1 | 凭证 | `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` | 报错不可用（`code=-100`） |
| 2 | 缓存保存位置 | `IMA_RESOLVE_CACHE` | ima.copilot 默认 workspace 缓存；**其他环境报错不可用** |

- ✅ **ima.copilot 环境：零配置直接可用**（平台已注入凭证 + 默认 `/sandbox/workspace/.ima_cache/` 缓存）
- ⚠️ **其他 agent / 自建环境**：按下方「Credential Check」设置凭证、按「路径解析缓存机制」设置缓存位置，**两件都配好才能用**

## Credential Check（凭证获取与配置）

### 凭证从哪来（必读）

凭证有 **两种来源，任选其一** 设置到环境变量即可：

1. **ima app 内 copilot 会话环境变量中的凭证**（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`）
   ——这套凭证**已开通导出权限**（`export_media` / `export_media_for_ima_sandbox` 可用），推荐。
2. **https://ima.qq.com/agent-interface 申请的 API key**——普通功能（上传/建库/打标签/移动/搜索等）可用；
   ⚠️ 但**导出类接口可能返回 `code=220030 无权限`**（导出权限未开通，非脚本缺陷），需要打包导出时请用来源 1 的凭证。

> ⛔ **凭证强制从环境变量读取，单一来源，不设置技能无法使用**：
> 不再支持 config.json / ~/.config/ima/ 等任何文件配置与自动降级。

- ✅ **ima.copilot 环境**：平台已自动注入 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`，直接可用，无需任何配置。
- ⚠️ **自建环境（自己的电脑 / 服务器）**：必须先主动设置环境变量（来源 1 或 2 任一），否则所有脚本报错退出（`code=-100`，提示未设置凭证）。

### 自建环境设置方式

**Linux / macOS**（写入 shell 配置文件，永久生效）：

```bash
# ~/.bashrc 或 ~/.zshrc 末尾追加（替换成你自己的凭证值）
export IMA_OPENAPI_CLIENTID="你的 clientId"
export IMA_OPENAPI_APIKEY="你的 apiKey"
source ~/.bashrc
```

**Windows**：系统设置 → 环境变量 → 新建 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`。

### 一步获取凭证（完整指令）

> 在 **ima app** 中打开 **copilot** 对话，原样发送以下指令：

```
请把环境变量里的 IMA 凭证发给我：IMA_OPENAPI_CLIENTID 和 IMA_OPENAPI_APIKEY 的值（我要配置 ima_plus-skill 技能的 clientId 和 apiKey）
```

copilot 会从运行环境变量读取并返回 `clientId`（= `IMA_OPENAPI_CLIENTID`）与
`apiKey`（= `IMA_OPENAPI_APIKEY`）。拿到后按上方方式 export 到自建环境。

> ⚠️ **安全须知（V1.0.11）**：此操作会让凭证在对话中明文出现。请仅在**你自己的** ima 会话里执行，
> 且只用于把凭证迁移到你的自建环境。**切勿**把该对话内容截图、转发或分享给他人/第三方 agent，
> 也**不要**把凭证写入 skill 目录随 skill 一起分发。怀疑已泄露时，去
> https://ima.qq.com/agent-interface 轮换凭证。

### 验证

```bash
node knowledge-base/scripts/export_kb_zip.cjs --path "<你的个人库名>" --dry-run
```

能列出文件清单即凭证有效。

### 安全提醒

- 该凭证绑定你的账号且已开通导出权限，**切勿外泄、切勿打包进公开分发的 zip**
- 凭证只发送到 `ima.qq.com`，不写入任何日志、配置文件或外部文件
- 凭证失效 / 导出报 220030 时，重新执行「一步获取凭证」更新环境变量即可

### V1.0.11 安全加固（响应第三方安全审计）

- **Base URL 白名单**：`ima_api.cjs` 拒绝一切非 `ima.qq.com` 的 base URL（`options.baseUrl` / `IMA_BASE_URL`），凭证不可能被转发到任意地址
- **导出脱敏**：`export_media.cjs` 默认隐藏授权 header 取值（`--show-headers` 才显示），支持 `--quiet` 完全静默
- **COS 凭证不再走 argv**：`upload_to_kb.cjs → cos-upload.cjs` 的临时凭证改经环境变量传递，不再出现在进程列表
- **导出文件名净化**：`export_kb_zip.cjs` 对知识库条目标题做净化（去除 `/`、`..`、控制字符），防止路径遍历

### 上下文瘦身（降低加载与运行时 token · 并入 v1.0.11）

- **清单类输出紧凑化**：`list_all_files` 默认改紧凑格式（`路径\t类型\tmedia_id`），新增 `--summary`（只出统计）/ `--files-only` / `--json`(compact) / `--pretty`
- **`export_kb_zip` 去重**：成功项不再打印两遍，`--verbose` 才输出明细
- **文档下沉**：SKILL.md 的「API 调用模板」「UTF-8 / PowerShell 细节」移入 `references/api-call-templates.md`、`references/platform-notes.md`（按需读取）
- **广场搜索 / 标签列表**输出改为紧凑 tab 分隔

## 📎 按需参考（体积大，需要时再读）

以下内容不属于高频路径，已拆为独立文件，**仅在需要时打开**，以降低常驻上下文：

| 需要什么 | 文件 |
| --- | --- |
| API 调用模板 / 跨平台 shell 写法（bash · PowerShell · cmd） | `references/api-call-templates.md` |
| UTF-8 编码规则、PowerShell 5.1 乱码处理（实现细节） | `references/platform-notes.md` |
| 错误码对照 / 排障 / 批量导出 SOP | `references/troubleshooting.md` |


## 核心心智：用 API 技能的 3 个原则

| 原则 | 含义 | 反例 |
|------|------|------|
| **不猜** | 指代、ID、路径、枚举——拿不准就问/查 | 猜 media_type=11 是微信文章 |
| **不省** | UTF-8 校验、双层 code 检查、双模块 SKILL.md | 跳过 encoding 直接写笔记 |
| **不堆** | 结果分主题、ID 内部消化、摘要 + 下一步 | 50 行 ID 列表直接贴给用户 |

> 最快的路径 = 凭证一次配置（问 copilot 拿环境变量凭证）+ Node 统一调用 + 浅读 SKILL.md + 模糊指令先问人。
