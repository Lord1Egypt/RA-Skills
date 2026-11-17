---
title: "文章标题"
date: 2026-07-21
draft: false
tags:
  - tag1
  - tag2
  - automation
  - productivity
  - developer-tools
categories: ["tech"]
description: "文章描述. 适用于需要相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
pricing_tier: free
version: "1.0.0"
category: "Operations"
license: "MIT"
slug: hugo-blog-publisher-free
name: hugo-blog-publisher-free
displayName: "技能工具"
summary: "提供核心功能的开发技能工具"
tools:
  - read
  - exec
---
```

规则：
- `categories`：使用已有分类的小写英文slug，如 `tech`, `investment`, `ai`, `photo`
- `tags`：使用小写英文slug，不用中文
- `slug`：文件名使用小写英文，不用中文 关键词: hugo blog publisher

### 3. 标签分类映射（Taxonomy Branch Bundle）
文章frontmatter用英文slug，页面展示用中文，通过 `_index.md` 实现：

1. frontmatter中使用英文slug：
```yaml
tags: ["ssg", "网络代理"]
categories: ["tech"]
```

2. 遇到新标签/分类没有映射文件时，创建：
```
content/tags/<slug>/_index.md
content/categories/<slug>/_index.md
```

3. 文件内容极简：
```yaml
---
title: "显示的中文名"
---
```

### 4. 截断标记与Git推送
在领先段或导言后添加 `<!--more-->`，让列表页显示摘要.
从博客目录自动检测git状态并推送：
```bash
cd {博客路径}
git add content/posts/{文件名}
git commit -m "新增：{文章标题}"
git push
```

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 发布技术文章 | Markdown内容 | 文章文件+Git推送+部署链接 |
| 创建新标签映射 | 新标签slug | _index.md映射文件 |

## 使用流程

1. 读取用户记忆文件(`MEMORY.md`/`USER.md`)获取博客配置
2. 分析文章内容,提取标题、标签、分类
3. 生成front matter,创建文章文件 `content/posts/{slug}.md`
4. 检查新标签/分类,创建 `_index.md` 映射文件
5. 添加截断标记 `<!--more-->`
6. Git推送并返回部署链接

#
## 示例

### 示例:发布技术文章

用户输入文章内容后，系统自动完成：

```bash
# 1. 生成文件
content/posts/hugo-blog-deployment.md
# ...
# 2. 文件内容
```
echo "操作完成"
```yaml
---
title: "静态站点部署指南"
date: 2026-07-21
draft: false
tags: ["ssg", "deployment"]
categories: ["tech"]
description: "如何将静态站点部署到生产环境"
---
# ...
本文介绍静态站点的部署流程.
# ...
<!--more-->
# ...
## 准备工作
# ...
首先确保本地环境已安装所有依赖...
```
echo "操作完成"
```bash
# 3. 如需新标签，创建映射
content/tags/deployment/_index.md
# 内容: ---\ntitle: "部署"\n
---
# ...
# 4. Git推送
cd ./my-blog
git add content/posts/hugo-blog-deployment.md
git commit -m "新增：静态站点部署指南"
git push
```

输出：
```
文章已发布成功！
部署链接: https://example.com/posts/hugo-blog-deployment/
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 博客路径未找到 | 配置文件缺失 | 检查 `MEMORY.md` 或 `.git` 配置，询问用户提供博客路径 |
| Git推送认证失败 | SSH key或credentials未配置 | 确保用户已配置SSH key或git credentials |
| 文件名slug冲突 | 同名文章已存在 | 检查 `content/posts/` 目录，添加日期前缀或修改slug |
| front matter格式错误 | YAML语法问题 | 确保YAML缩进正确，字符串用引号包裹 |

## 常见问题

### Q1: 标签和分类应该用中文还是英文？
A: frontmatter中使用小写英文slug（如 `tech`, `ai`），页面展示通过 `_index.md` 映射为中文。不用i18n配置，全部用 `_index.md` 映射.
### Q2: 如何处理新标签没有中文映射的情况？
A: 需要创建 `content/tags/<slug>/_index.md` 文件，内容为 `---\ntitle: "中文显示名"\n---`。例如标签 `docker` 创建文件后title设为 `"Docker"`.
### Q3: 截断标记 `<!--more-->` 应该放在哪里？
A: 通常放在领先段结束后的空行，或导言和正文之间。列表页只显示截断标记之前的内容作为摘要.
## 已知限制

- 需要本地运行，必须能访问博客目录
- 需要Git和代码仓库访问权限（SSH key或credentials）
- 标签分类映射使用 `_index.md` 文件方式，不用i18n

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 升级提示

本免费版提供基础功能。升级到完整版 hugo-blog-publisher 获取全部能力和高级特性.