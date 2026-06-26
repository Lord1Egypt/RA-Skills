---
name: obsidian-llm-wiki
description: |
  个人知识库构建系统 — 基于 Karpathy LLM-Wiki 方法论，结合 obsidian-cli 实现高效的 Obsidian vault 管理。
  让 AI 持续构建和维护你的 Obsidian 知识库，支持多种素材源（网页、公众号、知乎、YouTube、PDF、本地文件），
  自动整理为结构化的 wiki。触发条件：用户明确提到"知识库"、"wiki"、"消化素材"、"健康检查"、"检查知识库"等。
  不要在用户只是要求"总结这篇文章"时触发——必须是明确的知识库管理意图。
---

## ⚠️ 产品限制

**Obsidian CLI 依赖条件：**

1. **Obsidian CLI 必须开启**：设置 → 关于 → 命令行界面 → 启用
2. **Obsidian 建议最新版**（CLI 功能需要较新版本支持）
3. **vault 必须用 Obsidian 打开过一次**（CLI 需要 Obsidian 注册过该 vault）
4. **网络**：素材提取可能需要网络访问

---

# obsidian-llm-wiki — 个人知识库构建系统

> 把碎片化信息变成持续积累、互相链接的知识资产。你只需提供素材，AI 完成所有整理工作。

---

## 这个 skill 做什么

obsidian-llm-wiki 帮你构建一个**持续增长的 Obsidian 知识库**：

- 你给素材（链接、文件、文本），AI 提取核心知识并整理成互相链接的 wiki 页面
- 知识库随每次使用变得更加丰富，而不是每次重新开始
- 所有内容都是本地 markdown 文件，用 Obsidian 实时查看
- **obsidian-cli** 驱动所有 vault 操作，绕过文件锁

---

## 核心理念

**"这不是 RAG。RAG 每次查询都从原始文档重新推导知识。而 wiki 是编译一次，然后持续维护。"**

| 原则 | 含义 |
|------|------|
| Sources are truth | raw/ 是不可变的原始素材，AI 只写 wiki/ |
| Compound, don't duplicate | 每次 ingest 与已有页面整合，不是孤立总结 |
| Link liberally | 交叉引用是 wiki 长期价值的来源 |
| Surface contradictions | 用 `> ⚠️ Contradiction with [[source]]` 标记矛盾 |
| Index is the entry point | 每次查询从 index.md 开始 |
| Good answers belong in the wiki | 有价值的分析应该进入 wiki |
| Maintenance cost is near zero | AI 不会无聊、不会遗忘、不会失去一致性 |

---

## 素材获取插件推荐

Obsidian 官方和社区有多款插件可将网页内容转为 Markdown：

| 插件 | 类型 | 特点 |
|------|------|------|
| **Obsidian Web Clipper** | 浏览器扩展 | 官方出品，剪藏网页为 Markdown |
| **简悦 (Obsidian8)** | Obsidian 插件 | 高亮、标注、剪藏，生态成熟 |
| **Obsidian URL Clipper** | Obsidian 插件 | 可视化选择器精准抓取正文 |
| **Defuddle** | CLI/网页 | 命令行/网页内容提取 |

> 推荐组合：**Obsidian Web Clipper**（浏览器扩展）+ **Defuddle**（CLI 提取工具）配合使用。

---

## 目录结构

```
<vault_root>/
├── raw/                    # 原始素材 — 不可变，只读
│   ├── articles/          # 网页文章
│   ├── tweets/           # X/Twitter
│   ├── wechat/           # 微信公众号
│   ├── xiaohongshu/     # 小红书
│   ├── zhihu/            # 知乎
│   ├── pdfs/             # PDF 文件
│   └── notes/            # 本地笔记
│       ├── learning/      # 学习相关
│       ├── projects/     # 当前项目
│       └── testing/      # 测试管理
├── wiki/                  # 知识库 — AI 全权维护
│   ├── sources/           # 素材摘要（每篇素材的摘要页）
│   ├── entities/         # 实体页（人物、产品、概念、工具）
│   ├── topics/           # 主题页（研究领域、知识体系）
│   ├── comparisons/       # 对比分析
│   ├── synthesis/         # 综合报告
│   ├── index.md          # 知识库总索引
│   └── log.md           # 操作日志
├── templates/             # 页面模板（entity/topic/source）
└── README.md             # 知识库说明
```

---

## obsidian-cli 工具整合

> **核心发现**：`obsidian create ... overwrite` 在 Obsidian **关闭时也能工作**（直接写 vault 文件），完全绕过文件锁问题。

### vault 名称

首次使用需确认 vault 名称（Obsidian 打开时执行 `obsidian vaults` 查看）：

```
vault="<vault_name>"
```

### 核心命令速查

| 场景 | 推荐命令 | 备注 |
|------|---------|------|
| **新建/覆盖页面** | `obsidian vault="..." create path="wiki/path/page.md" content="..." silent overwrite` | `path` 支持子目录，`name` 不支持 `/` |
| **追加到日志** | `obsidian vault="..." append path="log.md" content="..."` | 直接追加 |
| **lint：断链检查** | `obsidian vault="..." unresolved total` / `verbose` | 获取断链列表 |
| **lint：孤立页面** | `obsidian vault="..." orphans total` / `verbose` | 没有其他页面链接到它 |
| **lint：死链页面** | `obsidian vault="..." deadends total` / `verbose` | 没有出站链接 |
| **全文搜索** | `obsidian vault="..." search query="关键词" path="wiki"` | 精准搜索 |
| **查看入站链接** | `obsidian vault="..." backlinks file="页面名"` | 分析页面关系 |
| **查看出站链接** | `obsidian vault="..." links file="页面名"` | 分析页面关系 |
| **读取页面内容** | `obsidian vault="..." read path="wiki/xxx.md"` | 读取文件 |
| **读取模板** | `obsidian vault="..." template:read name="模板名"` | 需 Obsidian 打开 |

### 文件写入策略（重要更新）

> **⚠️ 经验教训**：obsidian-cli 的 `content` 参数不适合长内容（>500字），会截断！请务必遵循以下策略。

#### 判断标准

| 内容长度 | 推荐方式 | 原因 |
|----------|----------|------|
| **短内容（<500字）** | `obsidian create content=xxx` | CLI 写入，绕过文件锁 |
| **长内容（>500字）** | `write_to_file` | 直接写文件，避免截断 |
| **追加日志** | `obsidian append` | 适合短日志条目 |
| **编辑文件中间部分** | `replace_in_file` | 精确替换，避免重复 |

#### 长内容写入流程

```bash
# Step 1: 使用 write_to_file 直接写入完整内容
# Step 2: （可选）验证文件是否完整
obsidian vault="<vault>" read path="wiki/path/page.md"
```

#### 短内容写入流程（Obsidian 打开时）

```bash
# 短内容可以用 CLI 写入
obsidian vault="<vault>" create path="wiki/path/page.md" content="简短内容" silent overwrite

# 追加日志
obsidian vault="<vault>" append path="log.md" content="## [2026-04-08] log entry"
```

> **⚠️ CLI 写入长内容的风险**：如果内容包含代码块（反引号）、特殊字符或超过命令行长度限制，会被截断！宁可多用 write_to_file。

### 何时用 Python/File工具 vs obsidian-cli

| 任务 | 推荐方案 | 说明 |
|------|---------|------|
| **新建/覆盖 wiki 页面**（长内容） | **write_to_file** | 避免截断风险 |
| **新建/覆盖 wiki 页面**（短内容） | `obsidian create` | Obsidian 打开时用 |
| **追加日志** | `obsidian append` | 适合短条目 |
| **编辑文件中间部分** | `replace_in_file` | 精确替换 |
| **lint 健康检查** | **obsidian CLI** | 内置精准命令 |
| **全文搜索** | `obsidian search` | 内置搜索 |
| **页面关系查询** | `obsidian backlinks/links` | 内置命令 |
| **文件统计** | `obsidian files folder` | 内置命令 |

### 临时文件管理

如果处理过程中创建了临时文件（如 `temp.md`），**必须及时删除**：

```bash
# 处理完成后检查并删除临时文件
rm temp_source.md
```

---

## 模板系统

知识库使用固定格式的模板，保证页面结构一致性。

### 模板文件位置

Skill 自带模板（初始化时复制到 vault）：

```
<skill_dir>/templates/
├── entity-template.md    # 实体页模板
├── topic-template.md     # 主题页模板
└── source-template.md    # 素材摘要模板
```

初始化后，模板位于 vault 的 `templates/` 目录：
├── entity-template.md    # 实体页模板
├── topic-template.md     # 主题页模板
└── source-template.md    # 素材摘要模板
```

### 页面格式（5段式）

所有 wiki 页面遵循统一格式：

**实体页 / 主题页**：
```markdown
# 标题

> 类型描述

## 概述
- **类型**：
- **定位**：

## 关键要点
- 要点1（→ [[来源页面]]）
- 要点2

## 关联
- [[相关实体]] — 关联原因

## 反面论证与空白
- 暂无已记录的局限或待验证点

## 来源
- [[素材摘要页]]
```

**素材摘要页**：
```markdown
# 标题

> 来源：raw/...
> 日期：YYYY-MM-DD

## 概述
- **类型**：
- **来源**：

## 关键要点

## 关键概念

## 关联
- [[相关实体/主题]] — 关联原因

## 来源
- raw/...
```

### 模板使用方式

```python
import os

SKILL_DIR = r"C:\Users\<用户名>\.workbuddy\skills\obsidian-llm-wiki"

def load_template(vault_root, name):
    # 优先用 vault 本地模板，否则用 skill 内置模板
    local = os.path.join(vault_root, "templates", f"{name}-template.md")
    skill_tpl = os.path.join(SKILL_DIR, "templates", f"{name}-template.md")
    path = local if os.path.exists(local) else skill_tpl
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def create_entity_page(vault_root, title, page_type, key_facts, sources):
    t = load_template(vault_root, "entity")
    return t.replace("{{title}}", title)\
             .replace("{{type}}", page_type)\
             .replace("{{key_facts}}", key_facts)\
             .replace("{{sources}}", sources)
```

---

## 工作流路由

根据用户意图路由到对应工作流：

| 用户意图关键词 | 工作流 |
|---|---|
| "初始化知识库"、"新建 wiki" | → **init** |
| URL / 文件路径 / "添加素材"、"消化"、"整理" | → **ingest** |
| "批量消化"、"把这些都整理" / 文件夹路径 | → **batch-ingest** |
| "关于 XX"、"查询"、"XX 是什么" | → **query** |
| "深度分析 XX"、"综述 XX"、"digest XX" | → **digest** |
| "检查知识库"、"健康检查"、"lint" | → **lint** |
| "知识库状态"、"现在有什么" | → **status** |

---

## 工作流 1：init（初始化）

> **推荐直接运行初始化脚本**，一键完成所有设置。

### 一键初始化（推荐）

**跨平台初始化脚本（Windows / macOS / Linux）：**

```bash
# Windows (Git Bash / WSL)
chmod +x "<skill_dir>/scripts/init-wiki.sh"
"<skill_dir>/scripts/init-wiki.sh" "C:/MyVault" "AI学习"

# macOS / Linux
chmod +x "<skill_dir>/scripts/init-wiki.sh"
"<skill_dir>/scripts/init-wiki.sh" ~/MyVault "AI学习"

# 或不带参数运行交互式模式
"<skill_dir>/scripts/init-wiki.sh"
```

> 💡 **Windows 用户提示**：使用 **Git Bash** 或 **WSL** 运行脚本

脚本自动完成：
- 创建 `raw/` 和 `wiki/` 完整目录结构
- 复制模板文件到 `templates/`
- 生成 `index.md`（表格格式）
- 生成 `log.md`（分类前缀格式）
- 生成 `README.md`

### 手动初始化步骤

1. **询问 vault 路径**："你的知识库要放在哪里？"
2. **询问知识库主题**："你的知识库要围绕什么主题？"
3. **运行初始化脚本**或手动创建目录
3. **创建目录结构**：创建 raw/ 和 wiki/ 子目录
4. **创建模板文件**：写入 entity/topic/source 模板
5. **创建 index.md 和 log.md**
6. **记录 vault 名称**：写入 `~/.llm-wiki-vault` 方便后续复用

---

## 工作流 2：ingest（消化素材）

### 素材提取路由

| 素材类型 | 提取方式 |
|---------|---------|
| 微信公众号文章 | `<env> run wechat-article-to-markdown "<URL>"` |
| YouTube 视频 | `<env> uv run scripts/get_transcript.py "<url>"` |
| X/Twitter | `bun --cwd "<scripts>" main.ts <url>` |
| 其他 URL | `bun --cwd "<scripts>" main.ts <url>` |
| 本地 .md/.txt/.pdf | 直接读取 |
| 用户粘贴文本 | 直接使用 |

### 完整处理流程

1. **保存原始素材**到 `raw/` 对应目录
2. **阅读素材，提取关键信息**：
   - 核心观点（3-5 个要点）
   - 关键概念（3-5 个）
   - 与已有素材的关联
3. **生成素材摘要页** → **write_to_file** `wiki/sources/`
   > ⚠️ 素材摘要通常较长，用 write_to_file 避免截断
4. **更新或创建实体页** → **write_to_file** `wiki/entities/`
   > 如果内容很短（<500字），可用 obsidian CLI
5. **更新或创建主题页** → **write_to_file** `wiki/topics/`
6. **更新 index.md** → **replace_in_file**（追加新条目到表格）
7. **更新 log.md** → **replace_in_file**（追加 ingest 记录）
8. **向用户展示结果**

> 💡 **验证文件完整性**：写入后读取前 30 行确认内容完整

### 简化处理（短素材 <= 1000 字）

只生成素材摘要 + 提取 1-3 个关键概念，不创建/更新主题页。

> 💡 简化处理的文件写入仍建议用 write_to_file，除非确认内容非常简短。

---

## 工作流 3：lint（健康检查）

> **优先使用 obsidian CLI**——内置精准的 lint 命令，无需 Python 扫描全文。

```bash
# 1. 断链（被 [[链接]] 但文件不存在）
obsidian vault="<vault>" unresolved total
obsidian vault="<vault>" unresolved verbose    # 详细列表

# 2. 孤立页面（没有其他页面链接到它）
obsidian vault="<vault>" orphans total
obsidian vault="<vault>" orphans verbose      # 详细列表

# 3. 死链页面（没有出站链接）
obsidian vault="<vault>" deadends total
obsidian vault="<vault>" deadends verbose    # 详细列表

# 4. index 一致性
obsidian vault="<vault>" files folder="wiki/entities" total
obsidian vault="<vault>" files folder="wiki/topics" total
obsidian vault="<vault>" files folder="wiki/sources" total
```

### 输出报告

```markdown
知识库健康检查报告

断链（被 [[链接]] 但不存在）：N 条
- [[某概念]] → 建议创建新页面（来自 [[页面A]]）

孤立页面（无其他页面链接）：N 条
- [[某页面]] → 建议从 [[相关页面]] 添加链接

死链页面（无出站链接）：N 条
- [[某页面]] → 建议添加相关链接

index 一致性：
- wiki/entities/ 中有 N 个文件，index 中有 M 条
```

### 修复优先级

1. **断链 → 创建缺失实体/主题页**（阻塞其他问题）
   > 发现断链后，立即创建对应实体页，用 write_to_file 写入
   > 创建后记得更新 index.md 和 log.md
2. **孤立页面 → 添加到相关页面**
3. **死链页面 → 检查是否孤立或真的无需链接**
4. **index 不一致 → 更新 index.md**

### 断链修复流程

```
1. obsidian unresolved verbose → 获取断链列表
2. 对每个断链 [[名称]]:
   a. 判断类型：实体页 / 主题页
   b. write_to_file 创建页面
   c. replace_in_file 更新 index.md
3. replace_in_file 更新 log.md（记录修复）
```

---

## 工作流 4：query（查询知识库）

1. **读取 index.md** 了解知识库全貌
2. **搜索相关页面**：`obsidian search query="关键词" path="wiki"`
3. **读取最相关的 3-5 个页面**：`obsidian read path="wiki/..."`
4. **综合回答**：带内联引用 `[[页面名]]`
5. **建议回写**：询问是否保存为新的 wiki 页面

---

## 工作流 5：status（查看状态）

```bash
obsidian vault="<vault>" files folder="wiki/entities" total
obsidian vault="<vault>" files folder="wiki/topics" total
obsidian vault="<vault>" files folder="wiki/sources" total
obsidian vault="<vault>" recents total   # 最近打开
```

输出：页面数统计 + 最近活动 + 建议

---

## 环境依赖

> skill 支持多种运行时环境。占位符 `<env>` 表示用户应替换为自己的环境标识符。

### 依赖说明

| 依赖 | 安装方式 | 备注 |
|------|---------|------|
| youtube-transcript-api | `pip install youtube-transcript-api` 或 `<env> pip install youtube-transcript-api` | 视频字幕提取 |
| wechat-article-to-markdown | `uv tool install wechat-article-to-markdown` 或 `pip install wechat-article-to-markdown` | 微信公众号文章提取 |
| baoyu-url-to-markdown | `bun install <package>` | 通用网页提取 |

**环境说明：**
- `<env_name>` — 替换为你的 Python 环境名（如 `manti`、`base` 等）
- 示例：`pip install youtube-transcript-api` 或 `<env_name> pip install youtube-transcript-api`
- 推荐用 `uv` 或 `pipx` 安装全局工具避免污染项目环境

**即使部分依赖缺失，skill 仍可工作**（用户可以手动粘贴文本内容）。


---

## Security

- 纯指令型 skill，无外部代码执行
- 无凭据要求
- 只读写 vault 内文件
- 文件操作通过 obsidian-cli（沙箱内）

### 初始化脚本安全性

**✅ 已修复的安全问题：**

1. **Shell 注入漏洞** - `init-wiki.sh` 移除了危险的 `eval` 调用
   - 使用 `${VAULT_PATH/#\~/$HOME}` 安全展开 `~`
   - 使用 `realpath` 解析绝对路径
   - 添加路径验证（禁止以 `-` 开头的路径）

2. **硬编码开发者路径** - 移除了 `/home/eddie/...` 等特定路径
   - 使用通用路径查找策略
   - 兼容不同用户环境

3. **跨平台脚本安全** - 统一使用 bash 脚本
   - 移除 PowerShell 脚本（避免 ClawHub 安全限制）
   - bash 脚本提供完整的路径验证和规范化

**🔒 安全最佳实践：**
- 不使用 `eval` 处理用户输入
- 所有路径参数都经过验证和规范化
- 使用语言内置的安全 API 处理文件系统

---

## 致谢

本 skill 基于 [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) 项目构建，感谢原作者的启发和贡献。
