---
name: kb-digest
version: 1.1.0
description: "知识提炼器：任意链接/PDF/文字，一条命令提炼成结构化知识卡片。支持生成摘要、Q&A、思维导图、播客脚本。当用户想消化文章、研究论文、整理信息、做知识管理时触发。"
metadata:
  requires:
    bins: ["python3"]
    pip: ["requests", "pypdf", "python-dotenv", "markdownify"]
  env:
    - name: OPENCLAW_LLM_API_KEY
      description: "大模型 API Key（OpenClaw 自动注入）"
      required: true
    - name: OPENCLAW_LLM_BASE_URL
      description: "大模型 API 地址（OpenClaw 自动注入）"
      required: true
    - name: OPENCLAW_LLM_MODEL
      description: "大模型名称（OpenClaw 自动注入）"
      required: true
---

# kb-digest

**任何内容 → 结构化知识卡片。扔进去，出来就能用。**

## 快速开始

```bash
cd /path/to/kb-digest
pip install -r requirements.txt
python handler.py --url "https://example.com/article"
```

> OpenClaw 会自动注入 `OPENCLAW_LLM_API_KEY`、`OPENCLAW_LLM_BASE_URL`、`OPENCLAW_LLM_MODEL`，无需手动配置。

## 命令

```bash
# 从 URL 生成知识卡片（默认输出）
python handler.py --url "https://arxiv.org/abs/1706.03762"

# 从 PDF
python handler.py --pdf paper.pdf

# 从文字粘贴
python handler.py --text "把这段内容结构化..."

# 指定输出格式
python handler.py --url "..." --output card      # 知识卡片（默认）
python handler.py --url "..." --output mindmap   # 思维导图（Markdown）
python handler.py --url "..." --output qa        # Q&A 问答对
python handler.py --url "..." --output podcast   # 播客对话脚本
python handler.py --url "..." --output summary   # 纯摘要

# 保存到文件
python handler.py --url "..." --save output.md

# 推送到飞书（需设置 FEISHU_WEBHOOK_URL）
python handler.py --url "..." --push feishu

# 批量处理
python handler.py --batch urls.txt
```

## 输出示例（知识卡片）

```
📚 知识卡片 | Attention Is All You Need

💡 一句话
  用纯自注意力机制替代 RNN/CNN，开创 Transformer 架构。

🔑 核心要点
  1. Self-Attention 允许序列中任意位置直接交互，无需逐步传递
  2. Multi-Head Attention 从多个子空间捕捉不同语义关系
  3. Positional Encoding 以正弦波注入位置信息
  4. 训练速度比 RNN 快 8 倍（可并行化）

❓ Q&A
  Q: 为什么比 RNN 快？
  A: RNN 必须串行处理，Transformer 全序列并行计算

🧠 思维导图
  Transformer
  ├── Encoder ×6
  │   ├── Multi-Head Self-Attention
  │   └── Feed-Forward Network
  └── Decoder ×6
      ├── Masked Self-Attention
      ├── Cross-Attention（看 Encoder）
      └── Feed-Forward Network

🔗 延伸阅读
  BERT | Vision Transformer (ViT)

来源: https://arxiv.org/abs/1706.03762
生成: 2026-04-11 18:05
```

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `OPENCLAW_LLM_API_KEY` | 大模型 API Key | ✅（OpenClaw 自动注入）|
| `OPENCLAW_LLM_BASE_URL` | 大模型 API 地址 | ✅（OpenClaw 自动注入）|
| `OPENCLAW_LLM_MODEL` | 大模型名称 | ✅（OpenClaw 自动注入）|
| `FEISHU_WEBHOOK_URL` | 飞书推送 Webhook | 推送用 |

## 支持的输入格式

- **URL**: 网页文章、arXiv 论文、GitHub README
- **PDF**: 研究论文、报告、书籍章节
- **文本**: 直接粘贴任意文字
- **批量**: 一个文件列出多个 URL，逐条处理
