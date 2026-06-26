---
name: notebooklm-ppt
description: 使用 NotebookLM CLI 生成 PPT 演示文稿。从预置风格模板库中选择模板，通过 notebook query 设置风格要求，再生成幻灯片。适用于需要快速将文档转换为演示文稿的场景。
---

# NotebookLM PPT 生成

## 核心原则

**必须使用预置模板！** 不要自己编写风格提示词，必须从 `references/templates.md` 中选择。

## 快速开始

1. **安装 nlm CLI**
   ```bash
   pip install notebooklm-mcp-cli
   ```

2. **确认认证配置完成**
   ```bash
   nlm doctor
   ```

## 工作流程

### Step 1: 选择风格模板（必须！）

**从以下预置模板中选择**，不要自行编写：

| 模板名称 | 适用场景 | 关键字 |
|----------|----------|--------|
| Modern Newspaper | 商业报告、经济媒体、智库研究 | 商业、专业、严肃 |
| Sharp-edged Minimalism | 技术分享、产品介绍、架构设计 | 技术、极简、架构 |
| Yellow × Black Editorial | 时尚杂志、创意提案 | 创意、时尚、设计 |
| Black × Orange Creative | Agency 演示 | 创意、活力 |
| Manga Style | 教育培训、趣味讲解 | 教育、趣味、漫画 |
| Magazine Style | 女性向内容、生活方式 | 杂志、时尚、生活 |
| Pink Street-style | 街头文化、潮牌 | 街头、潮流、年轻 |
| Neo-Retro Dev | 开发者文档、技术博客 | 技术、开发者、复古 |
| Royal Blue × Red | 艺术展示、创意项目 | 艺术、创意、水彩 |
| Studio / Mockup / Premium | 产品发布、硬件展示 | 产品、硬件、高端 |
| Sports / Athletic | 运动品牌、健身内容 | 运动、健身、能量 |

**选择方法**：
1. 根据文档内容类型选择最合适的模板
2. 从 `references/templates.md` 中获取该模板的完整提示词
3. 替换占位符（如语言）

### Step 2: 创建笔记本并添加源

```bash
# 创建笔记本
nlm notebook create "演示文稿"

# 添加源文档
nlm source add <notebook_id> --url "https://..."
```

### Step 3: 用 Query 设置风格要求（重要！）

从模板获取提示词后，用 query 设置：

```bash
nlm notebook query <notebook_id> "请用中文回答。我希望生成PPT演示文稿，风格要求：[从templates.md复制的完整模板内容]。输出语言为中文。"
```

### Step 4: 生成幻灯片（只执行一次！）

```bash
nlm slides create <notebook_id> --language zh --confirm
# 记录返回的 Artifact ID
```

### Step 5: 等待并下载

```bash
# 等待生成完成
nlm studio status <notebook_id>

# 下载（使用 Artifact ID）
nlm download slide-deck <notebook_id> --id <artifact_id> --format pptx
```

### Step 6: 发送文件

```bash
# 复制到白名单目录
cp *.pptx ~/.openclaw/media/inbound/

# 发送
message --filePath ~/.openclaw/media/inbound/xxx.pptx ...
```

## ⚠️ 关键注意事项

1. **必须使用预置模板**：从 `references/templates.md` 选择，不要自行编写
2. **slides create 只执行一次**：每次执行都会创建新版本
3. **记录 Artifact ID**：下载时使用
4. **文件大小**：建议 <15MB

## 模板参考

完整模板内容见 `references/templates.md`
