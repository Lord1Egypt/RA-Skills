---
name: notebooklm
description: Google NotebookLM 非官方 Python API 的 OpenClaw Skill。支持内容生成（播客、视频、幻灯片、测验、思维导图等）、文档管理和研究自动化。当用户需要使用 NotebookLM 生成音频概述、视频、学习材料或管理知识库时触发。
version: 1.0.0
---

# NotebookLM Skill

通过非官方 Python API 访问 Google NotebookLM 的全部功能。

## 前置要求

```bash
pip install notebooklm-py
pip install "notebooklm-py[browser]"  # 首次登录需要
playwright install chromium
```

## 认证

首次使用需要登录：

```bash
notebooklm login
```

或使用 Edge（某些企业环境需要）：
```bash
notebooklm login --browser msedge
```

## 核心功能

### 1. 笔记本管理

```bash
# 创建笔记本
notebooklm create "我的研究"

# 列出所有笔记本
notebooklm list

# 切换当前笔记本
notebooklm use <notebook_id>

# 删除笔记本
notebooklm delete <notebook_id>
```

### 2. 添加来源

```bash
# 添加网页
notebooklm source add "https://example.com/article"

# 添加本地文件（PDF、Word、Markdown、音频、视频、图片）
notebooklm source add "./paper.pdf"
notebooklm source add "./lecture.mp3"

# 添加 YouTube 视频
notebooklm source add "https://youtube.com/watch?v=xxx"

# 执行网络研究并自动导入
notebooklm source add-research "人工智能发展趋势" --mode deep
```

### 3. 内容生成

```bash
# 生成音频概述（播客）
notebooklm generate audio "让内容更生动有趣" --wait

# 生成视频概述
notebooklm generate video --style whiteboard --wait

# 生成电影风格视频
notebooklm generate cinematic-video "纪录片风格总结" --wait

# 生成幻灯片
notebooklm generate slide-deck

# 生成信息图
notebooklm generate infographic --orientation landscape

# 生成测验
notebooklm generate quiz --difficulty hard --quantity 10

# 生成记忆卡片
notebooklm generate flashcards --quantity 20

# 生成思维导图
notebooklm generate mind-map

# 生成数据表格
notebooklm generate data-table "对比主要观点"

# 生成报告
notebooklm generate report "研究简报"
```

**音频格式选项**：
- `deep-dive` - 深入探讨
- `brief` - 简要概述
- `critique` - 批判性分析
- `debate` - 辩论形式

**视频风格选项**：
- `whiteboard` - 白板风格
- `news` - 新闻风格
- `cinematic` - 电影风格

### 4. 下载生成的内容

```bash
# 下载音频（播客）
notebooklm download audio ./podcast.mp3

# 下载视频
notebooklm download video ./overview.mp4

# 下载幻灯片（支持 PDF 和 PPTX）
notebooklm download slide-deck ./slides.pdf
notebooklm download slide-deck --format pptx ./slides.pptx

# 下载测验（支持 JSON、Markdown、HTML）
notebooklm download quiz --format json ./quiz.json
notebooklm download quiz --format markdown ./quiz.md

# 下载记忆卡片
notebooklm download flashcards --format json ./flashcards.json

# 下载思维导图
notebooklm download mind-map ./mindmap.json

# 下载信息图
notebooklm download infographic ./infographic.png

# 下载数据表格
notebooklm download data-table ./data.csv
```

### 5. 聊天问答

```bash
# 向笔记本提问
notebooklm ask "总结核心观点"
notebooklm ask "解释这个概念"

# 使用自定义人格
notebooklm ask "用简单的语言解释" --persona "友好导师"
```

## 完整工作流示例

### 学术研究转播客

```bash
# 1. 创建笔记本
notebooklm create "论文解读"

# 2. 上传论文 PDF
notebooklm source add "./research-paper.pdf"

# 3. 生成播客（深入探讨风格）
notebooklm generate audio "深入分析研究方法" --format deep-dive --wait

# 4. 下载 MP3
notebooklm download audio ./paper-podcast.mp3
```

### 批量视频生成

```bash
# 1. 创建笔记本并添加多个来源
notebooklm create "课程笔记"
notebooklm source add "./lecture1.pdf"
notebooklm source add "./lecture2.pdf"
notebooklm source add "https://reference-site.com"

# 2. 生成白板风格教学视频
notebooklm generate video --style whiteboard --wait

# 3. 同时生成测验检验学习效果
notebooklm generate quiz --difficulty medium

# 4. 下载所有材料
notebooklm download video ./lesson.mp4
notebooklm download quiz --format markdown ./quiz.md
```

### 研究项目自动化

```bash
# 1. 执行深度网络研究
notebooklm create "市场调研"
notebooklm source add-research "2024年电动汽车市场趋势" --mode deep

# 2. 生成综合分析报告
notebooklm generate report "市场分析报告"

# 3. 生成数据对比表格
notebooklm generate data-table "对比主要厂商的市场份额"

# 4. 生成演示幻灯片
notebooklm generate slide-deck

# 5. 批量下载所有材料
notebooklm download report ./report.md
notebooklm download data-table ./data.csv
notebooklm download slide-deck ./presentation.pdf
```

## Python API 使用

当需要更复杂的逻辑时，使用 Python API：

```python
import asyncio
from notebooklm import NotebookLMClient

async def research_workflow():
    async with await NotebookLMClient.from_storage() as client:
        # 创建笔记本
        nb = await client.notebooks.create("自动化研究")
        
        # 批量添加来源
        await client.sources.add_url(nb.id, "https://example.com/1", wait=True)
        await client.sources.add_file(nb.id, "./doc.pdf", wait=True)
        
        # 生成内容
        status = await client.artifacts.generate_audio(
            nb.id, 
            instructions="制作引人入胜的播客",
            format="deep-dive"
        )
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        
        # 下载
        await client.artifacts.download_audio(nb.id, "output.mp3")
        
        return nb.id

# 运行
nb_id = asyncio.run(research_workflow())
print(f"完成！笔记本ID: {nb_id}")
```

## 故障排查

```bash
# 检查认证状态
notebooklm auth check --test

# 查看元数据
notebooklm metadata --json

# 查看分享状态
notebooklm share status

# 列出支持的语言
notebooklm language list
```

## 注意事项

- 这是**非官方**库，使用 Google 内部 API，可能随时变动
- 大量使用时可能触发 rate limit
- 适合原型、研究和个人项目
- 首次登录后，凭据会保存在本地，后续无需重复登录
