# 文章发布格式规范

基于实战经验，发布文章时请遵循以下规则，避免格式错乱或发布失败。

## 1. 默认流程：Markdown → HTML（富文本）

如果提供的是 Markdown 文件（如 `.md`），**默认先将其转换为 HTML**，再以 `--raw-type html` 发布。这样 Halo 的默认编辑器能正常识别和渲染。

快速转换示例：

```bash
# 去掉 front matter，正文转成 HTML
sed '1,/^---$/d' article.md | sed '1{/^---$/d}' > body.md
npx marked body.md > body.html

# 创建 HTML 文章（用 Python 等脚本把 body.html 传给 --content）
python3 -c "
import subprocess
with open('body.html', 'r', encoding='utf-8') as f:
    html = f.read()
subprocess.run([
    'halo', 'post', 'create',
    '--profile', 'blog-danke',
    '--title', '文章标题',
    '--slug', 'post-slug',
    '--content', html,
    '--raw-type', 'html',
    '--publish', 'true'
])
"
```

**降级策略**：如果 HTML 转换失败（如 `npx marked` 不可用），则降级为直接用 `halo post import-markdown --file article.md --force` 发布纯 Markdown。

## 2. Markdown 文件结构

推荐在文件开头加 YAML front matter：

```markdown
---
title: "文章标题"
slug: "post-slug"
---

## 已完成

- 事项 1
- 事项 2
```

**注意：不要重复写一级标题 `# 文章标题`**。因为 Halo 主题本身会根据 front matter 的 `title` 显示文章标题，正文里再写一遍会变成双标题。正文直接从 `##` 二级标题开始。

## 3. 发布与可见性检查

创建/导入后默认可能是 `PRIVATE`（私密）或未发布状态。发布到博客后必须执行：

```bash
halo post update <name> --visible PUBLIC
halo post update <name> --publish true
```

其中 `<name>` 是文章的 metadata.name（创建成功后会输出）。

## 4. 封面图、分类与标签规范

### 封面图

发布文章时**默认生成一张封面图**。生成成功后先发送到当前对话确认，再上传至 Halo 作为文章封面。

**封面图要求**：
- **比例：优先使用 21:9 超宽横幅**。Halo 主题的文章封面区域偏扁平，16:9 或 4:3 会被严重裁剪或压缩
- **目的：以符合文章主题为第一原则**，根据内容生成对应的场景或意象画面
- **信息丰富度**：封面图应能**概括文章的大致内容**，而不仅仅是一张简单的装饰性图片。优先在 prompt 中加入能够体现文章核心信息、关键步骤或典型场景的元素，使封面本身具备一定的叙事性和识别度
- **注意：封面图和文章标题不会叠加显示**，不需要刻意留出标题空白区域

```bash
halo post update <name> --cover "https://blog.codingshen.top/upload/xxx.png"
```

如果图片生成失败（如文生图工具不可用），再降级为**不添加封面图**。

### 分类

发布前先用 Halo CLI 列出站点已有的分类：

```bash
halo post category list --profile blog-danke
```

**优先使用已存在的分类**。如果没有合适的，再自行创建：

```bash
halo post category create --display-name "新分类" --slug "new-category"
```

常用分类参考：日常、技术、AI、随笔、项目记录。

> ⚠️ **注意**：`--categories` 匹配的是分类的 **displayName（显示名称）**，而不是 `slug`。例如创建的是 `displayName=技术 slug=tech` 的分类，更新时必须传 `--categories "技术"`，传 `--categories "tech"` 会导致 Halo 自动新建一个 `displayName=tech` 的重复分类。

### 标签

标签根据文章主题自行补充，建议 1-3 个。常用标签参考：AI、碎碎念、Halo、技术、生活、随笔、项目。

```bash
halo post update <name> --tags "碎碎念,AI,Halo"
```

### AI 生成声明（必选）

**所有由 AI 生成的文章，必须添加 AI 生成声明 annotation。** Halo 后台实际读取的是这两个字段：

```bash
halo post export-json <name> --output /tmp/post.json
python3 -c "
import json
with open('/tmp/post.json', 'r') as f:
    d = json.load(f)
d['post']['metadata']['annotations']['ai_generated'] = 'true'
d['post']['metadata']['annotations']['ai_generated_desc'] = '本文内容由 AI 辅助生成，已经人工审核和编辑。'
with open('/tmp/post.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False)
"
halo post import-json --file /tmp/post.json --force
```

⚠️ **注意**：`import-json` 操作会将文章状态重置为 **未发布（DRAFT）**。导入后必须重新执行：
```bash
halo post update <name> --publish true
```

## 5. 快速验证格式

```bash
halo post get <name> --json | grep '"raw"'
```

- 如果是 HTML 发布，`rawType` 应为 `html`，`raw` 内容以 `<p>` / `<h2>` 等标签开头
- 如果是 Markdown 降级发布，`rawType` 应为 `markdown`，`raw` 内容应为真正的多行 Markdown
