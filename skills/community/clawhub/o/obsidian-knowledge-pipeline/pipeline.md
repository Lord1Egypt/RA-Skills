# Pipeline — 完整7步处理流程

## 环境准备

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
RAW_DIR="$VAULT/raw"
IMAGES_DIR="$RAW_DIR/images"
MAPPING_FILE="$IMAGES_DIR/关联关系.md"
WIKI_DIR="$VAULT/wiki/知识透视"
CLIPPINGS_DIR="$VAULT/Clippings"

# 确保目录存在
mkdir -p "$RAW_DIR" "$IMAGES_DIR" "$WIKI_DIR" "$CLIPPINGS_DIR"
```

---

## Step 1: 抓取内容 {#step-1}

### 优先方案：web_fetch

```
使用 web_fetch 工具抓取 URL 内容
参数：
  url: 目标URL
  extractMode: "markdown"
  maxChars: 50000
```

### 回退方案：scrapling（StealthyFetcher）

当 web_fetch 返回空内容、反爬拦截或内容质量不足时，执行：

```bash
python3 ~/.openclaw/skills/openclaw-scrapling/scripts/scrapling-fetch.py "<URL>" --text-only --max-chars 50000
```

- 默认 `--text-only --max-chars 5000`，对于完整文章建议提高 `--max-chars`
- 需要特定元素时加 `--selector "css.selector"`
- 需要原始 HTML 时用 `--html`

### 抓取后处理

1. 检查内容完整性（标题、正文、作者、日期）
2. 清理无关元素（广告、导航栏、cookie提示等）
3. 保留原文结构（标题层级、列表、代码块）
4. 提取元数据：title, author, date, source_url, word_count

---

## Step 2: 存入 raw/ {#step-2}

### 文件命名规则

```
格式：{文章标题}.md
冲突处理：{文章标题}_{YYYYMMDD_HHmmss}.md
特殊字符：将 / : * ? " < > | 替换为 -
```

### 存储模板

使用 [templates/raw-article.md](templates/raw-article.md) 模板：

```markdown
---
title: "{{文章标题}}"
source_url: "{{原始URL}}"
author: "{{作者}}"
date: "{{发布日期}}"
fetched_at: "{{抓取时间 YYYY-MM-DD HH:mm}}"
word_count: {{字数}}
tags: []
status: raw
---

# {{文章标题}}

> 来源：[{{来源名称}}]({{原始URL}})
> 作者：{{作者}} | 日期：{{发布日期}}

![配图](images/{{主题}}-配图.png)

---

{{正文内容}}

---

*抓取时间：{{抓取时间}}*
```

### 配图占位

文章存储时即嵌入配图引用 `![配图](images/{主题}-配图.png)`。若配图尚未生成，先写入占位引用，Step 3 生成后无需回改（路径一致即可）。

---

## Step 3: 生成配图 {#step-3}

详细规则见 [image-mapping.md](image-mapping.md)。

### 方案选择

```
if [ -n "$DASHSCOPE_API_KEY" ]; then
    # 使用 Wan2.7 脚本生成
    参考 ~/.agents/skills/wan2.7-image-skill/SKILL.md
else
    # 使用 image_generate 工具
    调用 image_generate 工具，prompt 基于文章主题生成
fi
```

### 配图 Prompt 构造

```
基础公式："{文章核心概念} 的概念插画，科技风格，扁平化设计，{主色调}色调，16:9比例"

示例：
- AI应用类："{主题} AI应用场景概念图，蓝色科技风格"
- 基础设施类："{主题} 系统架构示意图，深色技术风格"
- 人物观点类："{人物名} 技术理念可视化，现代简约风格"
```

### 保存规则

- 保存路径：`$IMAGES_DIR/{主题}-配图.png`
- 命名规则：提取文章核心概念作为主题，中文或英文均可
- 文件名禁止包含空格和特殊字符，用 `-` 连接

---

## Step 4: 更新映射 {#step-4}

详细规则见 [image-mapping.md](image-mapping.md)。

### 映射文件位置

`$IMAGES_DIR/关联关系.md`

### 追加条目

使用 [templates/mapping-entry.md](templates/mapping-entry.md) 模板，向映射文件追加：

```markdown
### {文章标题}

- **文章路径**: raw/{文章标题}.md
- **配图路径**: images/{主题}-配图.png
- **配图Prompt**: {生成时使用的prompt}
- **生成时间**: YYYY-MM-DD HH:mm
- **分类**: {自动分类结果}
- **状态**: ✅ 已完成
---
```

### 初始化映射文件

若 `关联关系.md` 不存在，先创建头部：

```markdown
# 配图关联关系

> 本文件记录所有文章与配图的映射关系
> 自动生成，请勿手动修改格式

---
```

---

## Step 5: 自动分类 {#step-5}

详细规则见 [classification.md](classification.md)。

### 分类决策流程

```
1. 分析文章标题、标签、核心关键词
2. 匹配分类关键词表（见 classification.md）
3. 确定主分类和子分类
4. 确定目标 Wiki 目录路径
5. 返回分类结果：{分类名, 目标目录, 标签列表}
```

### 无法明确分类时

- 优先归入"商业与消费"分类
- 在 front matter 中标记 `classification_confidence: low`

---

## Step 6: Wiki 编译 {#step-6}

详细规则见 [classification.md](classification.md)。

### 编译目标

将 raw 文章编译为结构化的 Wiki 知识节点，保存到 `$WIKI_DIR/{分类目录}/` 下。

### 6要素必须完整

使用 [templates/wiki-node.md](templates/wiki-node.md) 模板，确保以下6要素全部包含：

1. **定义** — 一句话定义核心概念
2. **类型/标签** — 便于检索的标签
3. **核心内容** — 结构化摘要（不是原文复制）
4. **关联概念** — 双向链接 `[[概念名]]`
5. **来源** — 原文链接和编译时间
6. **配图** — 嵌入生成的配图

---

## Step 7: 知识图谱 {#step-7}

### 双向链接建立

1. **从新节点出发**：扫描 Wiki 编译内容中提到的已有概念，添加 `[[概念名]]` 链接
2. **向新节点链接**：在已有的相关 Wiki 节点中追加对新节点的 `[[新概念名]]` 引用

### 操作步骤

```bash
# 1. 扫描已有 Wiki 节点，提取现有概念名列表
搜索 $WIKI_DIR 下所有 .md 文件的标题和定义

# 2. 新节点中匹配到的概念，用 [[概念名]] 包裹
例如原文提到 "Kubernetes" → 检查是否存在 wiki 节点 Kubernetes.md → 存在则链接

# 3. 在已有关联节点中追加反向链接
找到与新节点相关的已有节点，在其"关联概念"部分追加 [[新节点名]]

# 4. 保存修改
```

### 链接格式

```markdown
- 相关技术：[[LangChain]] · [[MCP]] · [[Function Calling]]
- 应用场景：[[Vibe-Trading]] · [[AI Agent]]
```

---

## Clippings/ 同步流程

```bash
# 1. 确保目标目录存在
mkdir -p "$CLIPPINGS_DIR"

# 2. 复制 Wiki 编译节点到 Clippings
cp "$WIKI_DIR/{分类目录}/{节点名}.md" "$CLIPPINGS_DIR/{节点名}.md"

# 3. 确保 Clippings 版本包含 source_url front matter
# （模板中已包含，无需额外操作）
```

### Clippings 特殊处理

- Clippings/ 目录用于与 Obsidian 插件（如 Obsidian ReadItLater）协同
- 若目标文件已存在且内容更新，替换为新版本并保留历史版本号
- 文件名与 raw/ 中的文件名保持一致的命名规则

---

## 完整执行检查清单

Agent 执行完毕后，必须确认以下内容：

- [ ] raw/{文章标题}.md 已创建且包含配图引用
- [ ] raw/images/{主题}-配图.png 已生成
- [ ] raw/images/关联关系.md 已更新
- [ ] Wiki 节点已编译到正确分类目录
- [ ] Wiki 节点包含完整6要素
- [ ] 双向链接已建立（新→旧 + 旧→新）
- [ ] Clippings/ 同步完成
- [ ] 所有路径使用了环境变量，无硬编码
