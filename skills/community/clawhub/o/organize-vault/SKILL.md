---
name: organize-vault
description: 扫描 Markdown vault 中的笔记，按语义主题生成目录层级，将笔记移动到
  对应目录，并在根目录和每个主题目录下创建 MOC.md。增量维护模式下检测 git 新增笔记，
  移动归类并更新对应 MOC.md。笔记内容始终不变，git 是唯一回退机制。
origin: OrganizeVault
version: "1.1.0"
license: MIT
homepage: https://github.com/wanli6/OrganizeVault
metadata:
  openclaw:
    emoji: "🗂️"
    os: ["darwin", "linux", "win32"]
---

# organize-vault

知识库目录结构生成与 MOC 维护助手。

## When to Use

当用户说以下内容时激活：
- "整理一下 vault"、"把新笔记归类"、"更新 MOC"
- "帮我初始化 vault 结构"、"生成目录层级"
- "哪些笔记还没归类"
- "organize my vault"、"update MOC"

## Core Constraints

在整个执行过程中，以下约束不可违反：

1. **永不修改笔记内容**：笔记的 body 文本不可改动。可移动文件位置、创建 MOC.md、在 MOC.md 中追加 wikilink。
2. **变更必须经用户确认**：所有文件移动和写入在执行前展示完整清单，等待明确确认。
3. **模糊性是正常状态**：无法归类的笔记归入 `misc/`，标注"待整理"，不强制归入不合适的主题。
4. **git 是唯一回退**：所有变更受 git 追踪，执行前告知用户可通过 `git revert` 撤销。

---

## 目标结构

初始化完成后，vault 应呈现如下层级：

```
vault/
├── MOC.md                  # 根目录索引，链接所有主题目录
├── programming/
│   ├── MOC.md              # 本主题笔记列表（含描述）
│   ├── python-async.md
│   └── docker-compose.md
├── tools/
│   ├── MOC.md
│   └── vim-config.md
├── reading/
│   ├── MOC.md
│   └── deep-work.md
└── misc/
    ├── MOC.md              # 标注"待整理"
    └── random-idea.md
```

---

## 入口：检测场景

```
1. 若 vault_root 未知，询问用户 vault 的根目录路径

2. 检测 git 状态：
   git -C <vault_root> status --porcelain 2>&1
   - 若返回 "not a git repository"：提示用户执行 git init，停止

3. 检测是否存在 MOC 文件（见 MOC 识别规则）：
   - 若无 MOC 文件 → 走【场景 B：初次初始化】
   - 若有 MOC 文件 → 走【场景 A：增量维护】
```

### MOC 识别规则

以下任一条件满足，则该文件被识别为 MOC，不参与归类：
- 文件名为 `MOC.md`（大小写不敏感）
- 文件顶部 frontmatter 中含 `type: moc` 或 `moc: true`

---

## 笔记描述提取规则

在读取笔记全文时，同步提取一句简短描述，用于写入 MOC.md。提取优先级：

1. frontmatter 的 `description` 字段（直接使用）
2. H1 标题后第一个非空段落的首句（截断到 50 字以内）
3. 以上均无：不写描述，只写 `- [[note-stem]]`

描述**只写入 MOC.md**，不触碰原笔记文件。

---

## 场景 A：增量维护（已有 MOC）

### Step 1 — 识别新增笔记

```bash
# 未提交的新增文件
git -C <vault_root> status --porcelain | grep '^?' | awk '{print $2}' | grep '\.md$'

# 或：相对上次 commit 新增的文件
git -C <vault_root> diff --name-only --diff-filter=A HEAD
```

过滤规则：
- 只保留 `.md` 文件
- 排除 `MOC.md`（按 MOC 识别规则）
- 若结果为空：告知用户"未发现新笔记（相对 git 状态）"，结束

### Step 2 — 读取现有目录结构

用 find 找到所有 `MOC.md` 文件，逐一读取，理解各主题目录的内容范围。

在内存中构建映射：
```
{
  "programming/MOC.md": "涵盖编程语言和框架，已有：[[python-async]], [[docker-compose]]...",
  "tools/MOC.md": "开发工具配置，已有：[[vim-config]], [[git-tips]]..."
}
```

### Step 3 — 归类决策

对每个新笔记，Read 其全文，然后：

1. 按【笔记描述提取规则】提取一句描述
2. 对比各主题目录，判断归属：
   - **高置信度**：直接给出目标目录
   - **低置信度**：列出候选目录，给出理由，让用户选择
   - **无法归类**：归入 `misc/`，标注"待整理"
3. 每篇笔记只移动到一个目录（主要主题）；若同时匹配多个主题，在多个 `MOC.md` 中均追加 wikilink
4. 检查目标 `MOC.md` 是否已含该笔记链接：若已含，跳过

### Step 4 — 展示变更预览

```
待执行的操作：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  移动：python-async.md → programming/python-async.md
  更新：programming/MOC.md ← 追加
        [[python-async]] — Python asyncio 事件循环机制详解
  理由：笔记讨论 Python asyncio，归入 programming

  移动：vim-config.md → tools/vim-config.md
  更新：tools/MOC.md ← 追加
        [[vim-config]] — Vim 配置文件与插件管理
  理由：编辑器配置，归入 tools

无法归类（共 1 篇）：
  random-idea.md → misc/random-idea.md（标注"待整理"）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

所有变更受 git 追踪，可通过 git revert 撤销。
确认执行？（可指定"全部"或逐条接受/拒绝）
```

### Step 5 — 执行变更

对每个用户确认的归类：
1. `mv <vault_root>/<note>.md <vault_root>/<topic>/<note>.md`
2. Edit `<topic>/MOC.md`，在笔记列表末尾追加：
   - 有描述：`- [[note-stem]] — {描述}`
   - 无描述：`- [[note-stem]]`

若目标目录不存在，先 `mkdir -p` 创建，再在其中创建 `MOC.md`（格式见下文）。

---

## 场景 B：初次初始化（无 MOC）

> 分四步执行，避免一次读取大量笔记导致上下文过长。

### Step 1 — 标题扫描

```bash
find <vault_root> -name "*.md" -not -path "*/.git/*" -not -name "MOC.md"
```

对每个文件，只提取：
- 文件相对路径
- H1 标题（首行 `# ...`）或文件名 stem（若无 H1）

**不读取笔记 body。**

### Step 2 — 分组提案

基于文件路径（目录结构）+ 标题，推断主题分组，向用户提出候选结构：

```
建议生成以下目录结构（基于 47 篇笔记的标题和路径）：

  programming/    — 约 18 篇（Python, TypeScript, 算法...）
  tools/          — 约 12 篇（Docker, Vim, Git...）
  reading/        — 约 9 篇（读书笔记, 摘录...）
  projects/       — 约 5 篇（项目记录...）
  misc/           — 约 3 篇（暂无明显归属）

是否采用这个结构？可以调整目录名、合并或拆分分组。
```

等待用户确认或修改。**不执行任何文件操作。**

### Step 3 — 逐组细化

用户确认结构后，按分组**逐批**读取笔记全文（每批 10-15 篇），对每篇笔记：

1. 按【笔记描述提取规则】提取一句描述
2. 确认归属哪个目录：
   - 归属明确的：记录目标目录 + 描述
   - 跨主题的：移动到主要目录，在次要目录的 `MOC.md` 中也追加链接
   - 完全不匹配的：归入 `misc/`，标注"待整理"

记录所有归属决策（含描述），**不写文件**。

### Step 4 — 目录重组

汇总所有归属决策，展示完整预览：

```
即将执行以下操作（共 47 个笔记）：

新建目录：
  programming/    tools/    reading/    projects/    misc/

移动文件（共 47 个）：
  python-async.md          → programming/python-async.md
  docker-compose.md        → programming/docker-compose.md
  vim-config.md            → tools/vim-config.md
  ...（共 47 条，全部展示）

新建 MOC 文件（共 6 个）：
  MOC.md                   （根目录索引，5 个主题）
  programming/MOC.md       （18 个笔记，含描述）
  tools/MOC.md             （12 个笔记，含描述）
  reading/MOC.md           （9 个笔记，含描述）
  projects/MOC.md          （5 个笔记，含描述）
  misc/MOC.md              （3 个笔记，标注"待整理"）

清理空目录（若有）：移走笔记后变空的原目录将被删除

所有变更受 git 追踪，可通过 git revert 撤销。
确认执行？
```

用户确认后，按以下顺序执行：
1. `mkdir -p` 创建所有主题目录
2. `mv` 移动所有笔记文件
3. Write 创建每个 `<topic>/MOC.md`（含描述）
4. Write 创建根目录 `MOC.md`
5. `rmdir` 清理空目录（失败则静默跳过）

---

## MOC 文件格式

**主题目录 `<topic>/MOC.md`**：
```markdown
# {主题名称}

## 笔记

- [[python-async]] — Python asyncio 事件循环机制详解
- [[docker-compose]] — 多容器应用编排配置示例
- [[algorithm-notes]]
```

（无描述的笔记直接写 `- [[note-stem]]`，不强制加破折号）

**根目录 `MOC.md`**：
```markdown
# Vault Index

## 主题

- [[programming/MOC|Programming]]
- [[tools/MOC|Tools]]
- [[reading/MOC|Reading]]
- [[projects/MOC|Projects]]
- [[misc/MOC|Misc]]
```

---

## 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| vault 未初始化 git | 提示执行 `git init && git add -A && git commit -m "init"`，停止 |
| vault 无任何 .md 文件 | 告知 vault 为空，结束 |
| 无法确定 vault 根目录 | 询问用户，不猜测 |
| 根目录已有 MOC.md | 询问用户是覆盖还是追加，不默认覆盖 |
| 笔记同时匹配多个主题 | 移动到主要目录，在次要目录 MOC.md 中追加跨目录 wikilink |
| 移走笔记后原目录变空 | `rmdir` 删除，失败则静默跳过（可能含其他文件） |
| MOC.md 已含该笔记链接 | 跳过，不重复添加 |
| 新笔记本身是 MOC.md | 跳过归类，告知用户 |
| 笔记无可提取描述 | 只写 `- [[note-stem]]`，不加破折号，不报错 |
| 大型 vault（> 100 篇笔记）初始化 | 严格执行分步策略，每批不超过 15 篇全文读取 |
