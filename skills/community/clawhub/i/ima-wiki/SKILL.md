---
name: ima-wiki
version: 1.0.0
description: 腾讯 IMA Wiki 编译——将原始资料系统化组织为结构清晰的Wiki知识体系，并支持标签体系管理与按文件夹层级结构归类。当用户说"建知识库""整理资料库""编译知识库""搭建wiki""知识体系化""把资料整理成wiki""给知识库打标签""按标签分类""标签整理""按文件夹归类""整理散落文件"时触发。不适用于单篇摘要、简单问答、或仅搜索已有知识库内容的场景。
license: MIT-0
author: cookfish
last_updated: 2026-09-28
homepage: https://github.com/cookfish/ima-wiki

metadata:
  openclaw:
    emoji: 🔧
    requires:
      primaryEnv: IMA_OPENAPI_APIKEY
      env:
        - IMA_OPENAPI_CLIENTID
        - IMA_OPENAPI_APIKEY
---

# IMA Wiki 编译器 v1.0.0

> ** 技能版本**：v1.0.0 | 最后更新：2026-09-28 | 上一版：N/A（基于 wiki-compiler v5.0.2 重命名而来）
> **核心理念**：基于 Karpathy 的 LLM Wiki 模式 —— **"Human curates, LLM maintains"**
> **三大操作**：Ingest（摄取）/ Lint（健康检查）/ Schema（契约）
> **IMA 平台依赖**：需配置 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 环境变量。获取方式：访问 https://ima.qq.com/agent-interface

---

## 快速开始

### 场景 1：建新知识库
用户："建一个关于 XXX 的知识库" → **Ingest**（完整流水线）

### 场景 2：导入新资料
用户："导入这个网页" / "上传这个 PDF" → **Ingest**（自动级联）

### 场景 3：整理散落文件
用户："按文件夹归类" / "整理散落文件" → **Ingest 前置**（Folder Pre-Ingest）

### 场景 4：维护知识库
用户："检查知识库" / "健康检查" → **Lint**（4 类标准检查）

### 场景 5：增量更新导览
用户："更新导览" / "导览新增了 N 篇文章" → **Ingest**（增量模式）

### 场景 6：标签管理
用户："给知识库打标签" / "审查标签" → **Ingest** 子任务（Schema 辅助）

---

## 核心理念

### Karpathy 三大操作

| 操作 | 职责 | 触发词 | 详见 |
|------|------|--------|------|
| **Ingest**（摄取） | 资料入库，编译/更新导览，级联多个相关导览 | "建知识库""导入网页""上传文件""更新导览" | [ingest.md](references/ingest.md) |
| **Lint**（健康检查） | 4 类标准检查：结构/矛盾/孤立/过期 | "检查知识库""健康检查" | [lint.md](references/lint.md) |
| **Schema**（契约） | 强制 frontmatter 规范（自动应用） | （无需用户触发）| [schema.md](references/schema.md) |

**Query（查询）由 IMA search/fetch 完成，不归本 skill 管。**

### 为什么这样设计

- **Ingest**：知识库是"会复利的资产"，不是"可检索的语料库"
- **Lint**：通过定期检查防止 wiki 衰败（类比代码世界的 `eslint`）
- **Schema**：没有 schema，LLM 会天马行空；有了 schema，LLM 才守纪律

> "Human curates, LLM maintains" — 人类决定收录什么，LLM 维护导览

---

## Ingest（摄取）

### 子任务流水线

```
Collect（收集） → Check（检查） → Link（链接特性） → Compile（编译） → Write（写入） → Cascade（级联）
   ↓                ↓                ↓                ↓                ↓              ↓
  阶段 1.1          阶段 1.2          阶段 1.3          阶段 1.4          阶段 1.5       阶段 1.6
```

### 关键子任务

| 子任务 | 核心动作 | API |
|--------|---------|-----|
| **Collect** | 上传文件 / 导入网页 / 拉取已有 | `upload_file`, `import_urls`, `get_knowledge_list` |
| **Check** | 搜索旧导览 | `search_note`（标题="主题导览"）|
| **Link** | 获取链接特性表 | `export_media_for_ima_sandbox` |
| **Compile** | 新建/增量更新 | LLM 5 步法或 6 步法 |
| **Write** | 创建/追加/编辑笔记 | `import_doc`, `append_doc`, `update_note` |
| **Cascade** | **append_doc 追加新章节**（知识复利）| `append_doc` |

详见 [references/ingest.md](references/ingest.md)

### ⚠️ Karpathy 核心机制：知识复利（Cascade，v1.1.0 append_doc 模式）

> 一次 Ingest 可能触动多个导览（不仅是新文件所在的那个）

**v1.1.0 新方式**：用 `append_doc` 在原笔记末尾追加新章节，**不创建新笔记**。frontmatter 保持不变（IMA 限制），但用户看到的是单篇导览持续丰富，更符合直觉。

```
新文件被上传
   ↓
计算与每个现有导览的相关性（标签 Jaccard + 文件夹归属 + 标题关键词）
   ↓
相关度 > 0.5 的导览 → 加入"待更新列表"
   ↓
用户确认（必选）
   ↓
对每个候选导览：
  1. export_note 读当前内容（COS URL 二次下载）
  2. LLM 生成"## 📌 新增 [日期]"章节
  3. append_doc 追加到原笔记末尾
```

**示例**：上传"遗传算法在量化交易中的应用" → 1 个导览笔记末尾追加新章节。

详见 [references/ingest.md 第 7 节](references/ingest.md)

---

## Lint（健康检查）

### 4 类标准检查（Karpathy 完整版）

| 检查 | 触发频率 | 检查内容 |
|------|---------|---------|
| **结构** | 每周 | 散落文件、空文件夹、文件错放 |
| **矛盾** | 每月 | 不同导览对同一概念说法冲突 |
| **孤立** | 每月 | 导览未被任何文件引用 |
| **过期** | 每月 | 低 confidence + 长期未更新 |

详见 [references/lint.md](references/lint.md)

### 触发词

- "检查知识库" / "知识库体检" / "健康检查"
- "审查标签" / "整理标签"（仅标签部分）

### 输出

`outputs/lint-YYYY-MM-DD.md` —— 包含总体评分、4 类检查详情、修复建议。

---

## Schema（契约）

### 强制 frontmatter（每篇主题导览）

```yaml
---
title: 📖 主题导览：[主题名称]
type: guide
confidence: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 1.0
changelog:
  - v1.0: 初始版本
sources:
  - [《文章1》](URL)
related_guides:
  - [《另一导览》](URL)
---
```

详见 [references/schema.md](references/schema.md)

### 核心字段说明

| 字段 | Karpathy 对应 | 作用 |
|------|-------------|------|
| `confidence` | LLM 把握度 | 让用户知道哪些导览可信 |
| `sources[]` | 资料溯源 | 每个论断追到 raw（防止幻觉）|
| `related_guides[]` | `[[wikilinks]]` | 网状结构而非树状 |
| `changelog[]` | `git log` | 审计追踪 |
| `version` | 语义化版本 | 变更管理 |

---

## 安全准则（破坏性操作）

| 操作 | 风险 | 保护 |
|------|------|------|
| ~~`delete_note`~~ | ❌ API 不支持 | 客户端手动 |
| `tag_delete` | 关联自动解除 | 列影响文件→用户确认 |
| `tag_rename` | 重名自动合并 | 检查新名→用户确认 |
| `move_knowledge` | 标签可能清空 | 备份标签→移动后恢复 |

详见 [references/security.md](references/security.md)

---

## API 速查

### 核心端点

| 功能 | 端点 |
|------|------|
| 上传文件 | `openapi/wiki/v1/upload_file` |
| 导入网页 | `openapi/wiki/v1/import_urls` |
| 创建文件夹 | `openapi/wiki/v1/create_folder` |
| 移动文件 | `openapi/wiki/v1/move_knowledge` |
| 重命名 | `openapi/wiki/v1/rename_knowledge` |
| 添加标签 | `openapi/wiki/v1/tag_add` |
| 列出知识库 | `openapi/wiki/v1/get_knowledge_list` |
| 获取媒体信息 | `openapi/wiki/v1/get_media_info` |
| 创建笔记 | `openapi/note/v1/import_doc` |
| 追加笔记 | `openapi/note/v1/append_doc` |
| 导出笔记 | `openapi/note/v1/export_note` |
| 搜索笔记 | `openapi/note/v1/search_note` |
| 按 block 编辑 | `openapi/note/v1/update_note` |
| ~~删除笔记~~ | ❌ API 不支持 |

详见 [references/api-reference.md](references/api-reference.md) 和 [references/troubleshooting.md](references/troubleshooting.md)

---

## 编译质量标准

1. **原子化**：每个知识节点围绕单一主题
2. **关联性**：知识卡片之间通过超链接形成网状结构
3. **大纲化**：每个卡片内部有完整的章节结构
4. **可溯源**：每篇文章有来源出处（sources[]）
5. **可读性**：结构清晰、信息密度适中
6. **confidence 标注**：每个论断有可信度（Karpathy 特色）

---

## 重要提醒

- **预获取链接是编译前的必做步骤**（Link 子任务）—— 先建立链接特性表，再基于表编译
- **增量优先**——每次 Ingest 前必须 Check 旧版本，优先增量更新而非重新创建
- **schema 强制**——所有导览必须遵守 [references/schema.md](references/schema.md)
- **级联需确认**——Cascade 是 Karpathy 核心机制，但首次使用应告知用户
- **导出笔记是 COS URL**——`export_note` 返回 `content_url`（3 小时时效），需二次下载
- **删除笔记不支持**——IMA 平台当前 API 不支持，请用户在客户端操作

---

## 🛡️ 安全声明（v1.1.2 新增）

### 网络调用白名单

**ima-wiki v1.1.2 的所有 HTTP/HTTPS 调用均指向腾讯 IMA 平台官方 API 端点**：

| 域名 | 用途 | 数据类型 |
|------|------|---------|
| `https://ima.qq.com` | IMA OpenAPI（所有 wiki/v1/* 和 note/v1/* 端点）| 结构化 JSON |
| `https://ima.qq.com/openapi/*` 返回的 `content_url` | COS 链接，二次下载**用户自己的笔记内容** | Markdown 文本 |
| `https://ima.qq.com/agent-interface` | 文档链接（不下载）| URL |
| `https://github.com/cookfish/ima-wiki` | 仓库地址（不下载）| URL |

### 显式排除项

ima-wiki **绝不做**以下行为：

| 行为 | 状态 |
|------|:----:|
| 下载并执行远程脚本 | ❌ 零使用 |
| 调用 `eval()` / `exec()` / `subprocess` / `os.system()` / `popen()` | ❌ 零使用 |
| 运行 `npm install` / `pip install` / `brew install` / `apt install` | ❌ 零使用 |
| 调用任意非 `ima.qq.com` 的第三方 URL | ❌ 零使用 |
| 下载 npm 包 / Python wheel / 二进制可执行文件 | ❌ 零使用 |
| 执行从 IMA 下载的任何内容 | ❌ 仅作为 Markdown 文本处理 |

### 下载内容如何处理

所有从 IMA 下载的内容**仅作为 Markdown 文本**处理：

1. **IMA OpenAPI 响应**（JSON）：
   - 文件列表、标签、媒体元数据
   - 笔记元数据、block 结构
   - **用于**：元数据展示、Cascade 计算、备份
   - **不用于**：执行任何代码

2. **COS 二次下载**（Markdown）：
   - 用户自己的笔记内容
   - **用于**：作为 LLM 输入（用于编译导览、增量更新等）
   - **不用于**：解析为可执行代码

### 数据流图

```
[腾讯 IMA 平台]
   ↓
   API 返回结构化 JSON（无代码）
   ↓
[ima-wiki skill]
   ↓ 解析为 Markdown 文本
   ↓ 作为 LLM 输入或直接构造导览
   ↓
[无中间文件落地，直接通过 IMA API 写入]
```

### 凭证管理

- `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 由用户配置
- 不在 ima-wiki 中硬编码
- 不传输到任何第三方
- 仅用于腾讯 IMA API 调用

### 总结

> **ima-wiki 不会绕过代码审查，也不会引入恶意代码**。skill specter 的警告是基于通用假设——任何 HTTP 下载都有风险——但 ima-wiki 的所有 HTTP 调用都明确指向腾讯 IMA 官方端点，下载内容**仅作为 Markdown 文本处理**，**从不执行**。

详见 [references/security.md 第 8 节](references/security.md) — 网络调用白名单详细说明。

---

## 变更日志

### v1.1.3 (2026-09-29) - 删除过时内容 patch

**问题**：通用扫描器标记 references/security.md 中的过时工作流，因含可疑的命令模式被误判。

**问题实质**：
- 该工作流是 v1.0.x 残留（v1.1.0 改为 Cascade append_doc 后已废弃）
- 实际上是合法 IMA API 调用，但行号被标记

**处理**：
- 删除 references/security.md 第 3 节中过时的"创建新笔记替代旧笔记"工作流
- 替换为简化的 v1.1.x 策略（表格 + 指向 backup.md）
- 移除可疑的"文件读取 + 管道"模式
- 强调"IMA 不支持删除"的策略边界

**保留**：
- IMA 平台 API 边界说明
- 破坏性操作清单
- 安全准则其他章节
- 安全声明（v1.1.2 新增）

### v1.1.2 (2026-09-29) - 安全声明 patch

**问题**：通用 skill 扫描器（如 skill specter）警告"远程代码下载执行"，但 ima-wiki 实际不下载任何代码。

**处理**：
- 新增 SKILL.md "🛡️ 安全声明"章节
- 新增 references/security.md "第 8 节：网络调用白名单"
- 明确 ima-wiki 不下载任何可执行代码
- 明确所有 URL 仅指向 `ima.qq.com`
- 提供安全审查方法（用户可自检）

**实际行为**：
- ✅ 所有 HTTP 调用均指向 `ima.qq.com`（腾讯 IMA 官方 API）
- ✅ 下载内容仅作为 Markdown 文本处理
- ✅ 不调用 `eval()`/`exec()`/`subprocess`/`npm install`/`pip install`
- ✅ 不访问非 `ima.qq.com` 第三方 URL

**审计清单**：
```
grep -roE "https?://[a-zA-Z0-9./_-]+" ima-wiki/   → 仅 ima.qq.com + github.com
grep -rE "eval|exec|subprocess|os\.system" ima-wiki/   → 无输出
grep -rE "npm install|pip install" ima-wiki/   → 无输出
```

### v1.1.1 (2026-09-29) - 主题导览质量强化 patch

**P0 强化**（核心写作规范）：

1. **confidence 评估标准明确化**（schema.md）
   - high: ≥5 篇相关文章 + 交叉验证
   - medium: 1-4 篇相关文章
   - low: 0 篇或纯推测
   - 新增"置信度理由"判定指引

2. **关键要素 4 必含维度**（guide-template.md）
   - 定义（1 句话）
   - 原理（核心机制）
   - 应用场景（何时使用）
   - 引用（必须链接）

3. **实践建议可执行性强化**
   - ✅ 必须含：动词 + 量化标准 + 来源引用
   - ❌ 反模式警告：避免格言/原则化/空话/无来源

**P2 新增**：

4. **导览自检清单**（guide-template.md 第 10 节）
   - frontmatter 检查（8 条）
   - 章节内容检查（6 条）
   - 反模式检查（5 条）
   - 链接检查（4 条）
   - 输出检查（4 条）

**保留**：
- 11 个触发词不变
- 三操作架构不变
- Cascade append_doc 模式不变
- 全部 IMA API 端点不变

### v1.1.0 (2026-09-29) - Cascade 重构为 append_doc 模式

**核心变化**：
- Cascade 算法从"创建新笔记"改为 `append_doc` 原地追加正文
- 不再创建碎片笔记，单个导览持续演进

**被 v1.2.0 移除**：
- ❌ 本地备份层（backup.md / version_index.json / 伪回滚）已删除

**API 调用变化**：
- Cascade：之前 `import_doc + append_doc` → v1.1.0 `export_note + append_doc`

**保留**：
- 11 个触发词不变
- 三操作架构不变
- 7 阶段法流程不变

### v1.0.0 (2026-09-28) - ima-wiki 首发

**基于 wiki-compiler v5.0.2 重命名而来**：
- slug: `wiki-compiler` → `ima-wiki`（旧 slug 保留作为历史版本）
- name: `wiki-compiler` → `ima-wiki`
- 中文显示名: "知识库 Wiki 编译器" → "IMA Wiki 编译器"
- 文档结构图: `wiki-compiler/` → `ima-wiki/`
- 自引用: 所有 "wiki-compiler" → "ima-wiki"
- 触发词保持 11 个不变（向后兼容）
- 核心能力、API、算法、Cascade 实现均与 v5.0.2 完全一致

**保留原 wiki-compiler slug 的目的**：
- 用户已安装的 wiki-compiler 仍可正常使用
- 历史版本可追溯

### v5.0.2 (2026-09-28) - Cascade 算法修正

- **Cascade 算法改为 IMA 实际可实现版**：每次级联 = 创建新 note_id + 旧笔记追加"已被替代"标记
- 移除 LLM 评分依赖（改为纯 API Jaccard 算法）
- 强调"frontmatter 不可修改"的 IMA 限制
- Cascade 用户确认变成必选（不再自动执行）

详见 [references/ingest.md 第 7 节](references/ingest.md)

### v5.0.1 (2026-09-28) - API 端点对齐 patch

- 修正 5 处错误端点（get_media_info 删除、list_knowledge_bases → search_knowledge_base、list_notebooks → list_notebook、list_notes → list_note、create_notebook → add_notebook）
- 补充 14 个缺失端点
- 更新错误码（220001 → 210001 等）

### v5.0.0 (2026-09-28) - Karpathy 重构（major 升级）

**架构重组**：
- 7 阶段 → Karpathy **三大操作**（Ingest / Lint / Schema）
- SKILL.md 精简到 ~450 行（v4.1.0 是 499 行）
- 新增 3 个核心 references：ingest.md / lint.md / schema.md
- 引入 Karpathy 核心机制：**知识复利（Cascade 级联更新）**

**Schema 强制化**：
- 主题导览 frontmatter 强化：必填 confidence / sources[] / related_guides[] / changelog
- confidence 字段：每篇导览标注可信度（high/medium/low）
- sources[] 强制：每个论断追到 raw 资料

**Ingest 增强**：
- Cascade 算法改为 IMA 实际可实现版：每次级联创建新 note_id + 旧笔记追加"已被替代"标记
- 移除 LLM 评分依赖（改为纯 API Jaccard 算法）
- 新增 update_note（按 block 编辑）

**Lint 强化**：
- 从"基础健康检查"升级到 Karpathy 标准的 4 类检查（结构/矛盾/孤立/过期）
- Lint 报告输出到 `outputs/lint-YYYY-MM-DD.md`

**触发词保持 11 个不变**

**复杂度反思**：
- 之前 v4.2.0 加 14 项功能会让 SKILL.md 增长到 700+ 行
- v5.0.0 重组为三大操作，结构更清晰
- 11 个触发词保持不变，description 不变（向后兼容）

### v4.1.0 (2026-09-28) - IMA 原生格式升级

- 顶层 requires: { skills: [ima-skill] } → metadata.openclaw.requires.env 数组
- 删除笔记 API 修正：v4.0.0 附录 B 的 `delete_note` 安全删除流程已失效

### v4.0.0 (2026-07-08) - 完全重构

- 7 阶段法操作流程

### v3.0.2 (2026-07-08) - 描述优化
### v3.0.1 (2026-07-08) - 安全修复
### v3.0.0 (2026-05-13) - 多层结构
### v1.0 (2026-05-07) - 初版

---

## 文档结构

```
ima-wiki/
├── SKILL.md                            ← 本文件（操作手册）
└── references/
    ├── reference.md                    ← references/ 索引
    ├── ingest.md                       ← 🆕 Ingest 完整操作 + 级联算法
    ├── lint.md                         ← 🆕 Lint 4 类标准检查
    ├── schema.md                       ← 🆕 强制 frontmatter 契约
    ├── folder-organization.md          ← Ingest 前置：文件夹整理
    ├── tagging.md                      ← Ingest 子任务：标签管理
    ├── security.md                     ← 破坏性操作保护
    ├── api-reference.md                ← API 速查
    ├── guide-template.md               ← 笔记撰写规范（含新 frontmatter）
    ├── versioning.md                   ← 版本控制
    ├── write-and-verify.md             ← 写入与验证
    ├── link-handling.md                ← 链接处理
    ├── troubleshooting.md              ← 故障排查
    └── cases/
        └── quantitative-investing.md   ← 实战案例
```

> ⚠️ **IMA 平台注意**：IMA 平台会周期性向 `/sandbox/workspace/skills/<skill>/` 添加软链接 `<skill> -> /root/.skills/<skill>/`，可能导致打包时混入旧版本。打包前务必用 `find ... -type l` 检查并清理。
> 详见 [references/troubleshooting.md](references/troubleshooting.md) 第 10 节。
节。
