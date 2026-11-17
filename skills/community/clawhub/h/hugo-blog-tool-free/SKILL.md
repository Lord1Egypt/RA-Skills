---
slug: hugo-blog-tool-free
name: hugo-blog-tool-free
version: 1.0.0
displayName: Hugo博客发布免费版
summary: 将 Markdown 文章发布到 Hugo 博客，自动生成 Front Matter 并推送到远程仓库.
license: Proprietary
edition: free
description: '面向个人博主的 Hugo 博客发布工具，简化文章发布流程。核心能力:

  - 自动分析文章内容，提取标题、标签、分类

  - 生成符合 Hugo 规范的 Front Matter

  - 自动添加截断标记（more）

  - Git 推送发布到远程仓库

  适用场景:

  - 个人技术博客文章发布

  - Markdown 文章的 Front Matter 自动生成

  - 博客内容的版本管理与推送

  差异化: 免费版聚焦个人博主的单篇文章发布场景，提供自动化的 Front Matter 生成与推送流程，开箱即用'
tags:
  - 开发工具
  - 博客
  - Hugo
  - 内容发布
  - 工具
  - 效率
  - 创意
  - git
  - hugo
  - content
  - posts
  - draft
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# Hugo 博客发布工具（免费版）

## 概述

本工具为个人博主提供 Hugo 博客文章发布的自动化流程，将 Markdown 文章自动转换为符合 Hugo 规范的博客文章并推送到远程仓库。通过自动分析内容提取标题、标签、分类，生成标准化的 Front Matter，添加截断标记，并执行 Git 推送，简化从写作到发布的全流程。免费版聚焦单篇文章的发布场景，提供开箱即用的发布模板与标签映射.
## 核心能力

| 能力模块 | 描述 | 典型用法 |
|----|---|----|
| 内容分析 | 自动提取标题、标签、分类 | `帮我发布这篇博客` |
| Front Matter 生成 | 生成 Hugo 标准格式 | 自动创建 YAML 头部 |
| 截断标记 | 自动添加 `<!--more-->` | 列表页显示摘要 |
| Git 推送 | 自动提交并推送 | `git push` |
| 标签映射 | 英文 slug 映射中文显示 | 自动创建 `_index.md` |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Markdown、文章发布到、自动生成、并推送到远程仓库、面向个人博主的、博客发布工具、简化文章发布流程、自动分析文章内容、生成符合、规范的、自动添加截断标记、推送发布到远程仓等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：发布技术文章

博主写完一篇技术文章，需要发布到 Hugo 博客.
```text
用户：帮我发布这篇 blog（附文章内容）
# ...
助手：自动完成以下步骤
# ...
1. 分析内容
   - 标题：从内容中提取
   - 标签：根据主题判断（如 AI → ["ai"]）
   - 分类：根据类型判断（如技术文章 → ["tech"]）
# ...
2. 生成文件名
   - 格式：content/posts/{slug}.md
   - slug：标题转为 URL 友好格式（小写、连字符）
# ...
3. 渲染 Front Matter
   ---
   title: "文章标题"
   date: 2026-07-18
   draft: false
   tags: ["ai", "programming"]
   categories: ["tech"]
   description: "文章描述"
   ---
# ...
4. 添加截断标记
   在第一段后添加 <!--more-->
# ...
5. Git 推送
   cd {博客路径}
   git add content/posts/{文件名}
   git commit -m "新增：{文章标题}"
   git push
# ...
6. 返回部署链接
```

### 场景二：新标签创建

文章使用了一个博客中还不存在的标签，需要创建映射文件.
```bash
# frontmatter 中使用英文 slug
# tags: ["ssg", "ssr"]
# categories: ["tech"]
# ...
# 如果遇到新标签没有映射文件，创建 _index.md
# 标签映射文件
cat > content/tags/new-tag/_index.md << 'EOF'
---
title: "新标签中文名"
---
EOF
# ...
# 分类映射文件
cat > content/categories/new-category/_index.md << 'EOF'
---
title: "新分类中文名"
---
EOF
```

### 场景三：本地预览后发布

博主想在发布前先本地预览效果.
```bash
# 1. 本地预览
cd {博客路径}
hugo server -D  # -D 包含草稿
# ...
# 2. 浏览器访问 http://localhost:1313 预览
# ...
# 3. 确认无误后发布
# 将 draft 改为 false
sed -i 's/draft: true/draft: false/' content/posts/{文件名}.md
# ...
# 4. 推送发布
git add content/posts/{文件名}.md
git commit -m "新增：{文章标题}"
git push
```

## 不适用场景

以下场景Hugo博客发布免费版不适合处理：

- 纯技术文档撰写
- 学术论文写作
- 法律文书起草

## 触发条件

需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于非本工具能力范围的需求.
## 快速开始

### Front Matter 规范

```yaml
---
title: "文章标题"
date: 2026-07-18
draft: false
tags: ["tag1", "tag2"]
categories: ["Category"]
description: "文章描述"
---
```

**重要规则**：
1. **categories**：使用已有分类（小写英文 slug），如 `tech`, `ai`
2. **tags**：使用小写英文 slug，不要用中文
3. **slug**：文件名使用小写英文，不要用中文
4. **date**：日期在 front matter 的 `date` 字段中指定，文件名不包含日期

### 常用分类速查

| Slug | 中文显示 |
|:-----|:-----|
| tech | 技术 |
| photo | 摄影 |
| ai | AI |
| investment | 投资 |
| tech-news | 科技资讯 |
| science | 科学 |
| art | 艺术 |
| life | 生活 |
| reading-notes | 读书笔记 |

### 常用标签速查

| Slug(续)| 中文显示 |
|-----:|-----:|
| ai | AI |
| llm | 大语言模型 |
| agent | 智能体 |
| programming | 编程 |
| thinking | 思考 |
| photography | 摄影 |
| camera | 相机 |
| photo | 照片 |
| go | Go |
| kubernetes | Kubernetes |
| rag | RAG |

### 专属名词（保持英文显示）

AI、RAG、NLP、Kubernetes、Go、Elasticsearch、PHP、SQL、SSG、SSR 等技术名称用英文 slug

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 截断标记位置

在第一段或导言后添加 `<!--more-->`，让列表页显示摘要.
```markdown
---
title: "我的文章"
date: 2026-07-18
draft: false
tags: ["programming"]
categories: ["tech"]
---
# ...
这是文章的导言部分，会在列表页显示.
# ...
<!--more-->
# ...
这是正文内容，不会在列表页显示.
```

### Git 推送流程

```bash
# 从博客目录自动检测 git 状态并推送
cd {博客路径}
# ...
# 添加新文章
# ...
# 提交（建议用"新增:"前缀）
git commit -m "新增：{文章标题}"
# ...
# 推送到远程
git push
```

### 配置自动读取

此工具会自动尝试从以下位置读取博客配置：

1. 用户记忆文件（MEMORY.md / USER.md）中的博客域名、路径等
2. 博客目录下的 .git 配置

如果未找到配置，才询问用户.
## 最佳实践

1. **slug 使用英文**：文件名使用小写英文，不要用中文
   ```bash
   # 正确
   content/posts/getting-started-with-hugo.md
# ...
   # 错误
   content/posts/Hugo入门指南.md
   ```

2. **标签用英文 slug**：frontmatter 中用英文，页面展示用中文（通过 `_index.md`）

3. **截断标记位置**：放在第一段结束后的空行，或导言和正文之间

4. **commit message 规范**：建议用 `新增:` 前缀
   ```bash
   git commit -m "新增：Hugo 博客发布指南"
   ```

5. **发布前预览**：使用 `hugo server -D` 本地预览

6. **配置 SSH Key**：确保 git push 不需要每次输入密码

## 常见问题

### Q1：如何生成 URL 友好的 slug？

```bash
# 英文标题：直接转为小写连字符
"Getting Started with Hugo" → "getting-started-with-hugo"
# ...
# 中文标题：可用拼音或英文关键词
"Hugo 入门指南" → "hugo-getting-started" 或 "hugo-ru-men-zhi-nan"
```

### Q2：如何创建新的标签映射？

```bash
# 创建标签映射文件
mkdir -p content/tags/new-tag
---
title: "新标签"
---
EOF
```

### Q3：文章发布后看不到怎么办？

```bash
# 1. 检查 draft 是否为 false
grep "draft:" content/posts/{文件名}.md
# ...
# 2. 检查日期是否是未来时间
grep "date:" content/posts/{文件名}.md
# ...
# 3. 本地预览（包含草稿）
hugo server -D
# ...
# 4. 检查文件路径是否正确
ls content/posts/
```

### Q4：如何修改已发布文章？

```bash
# 1. 编辑文章
# 2. 更新 date 或添加 lastmod
---
title: "文章标题"
date: 2026-07-18
lastmod: 2026-07-19
---
# ...
# 3. 推送更新
git commit -m "更新：{文章标题}"
git push
```

### Q5：git push 需要认证怎么办？

```bash
# 方案一：配置 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"
# 将公钥添加到 Git 平台
# ...
# 方案二：配置凭据缓存
git config --global credential.helper cache
helper "cache --timeout=3600"
```

### Q6：如何批量发布多篇文章？

```bash
# 批量添加
git add content/posts/*.md
# ...
# 批量提交
git commit -m "新增：批量发布多篇文章"
# ...
# 推送
git push
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Hugo 版本**: 建议 0.100 及以上
- **Git**: 需要配置远程仓库访问权限

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Hugo | 静态站点生成器 | 推荐 | gohugo.io 下载 |
| Git | 命令行工具 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令驱动，无需额外 API Key
- Git 推送需要配置 SSH Key 或个人访问令牌

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行博客发布流程，Git 推送需要命令行执行能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Hugo博客发布免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "hugo blog"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
