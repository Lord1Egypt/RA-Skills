---
name: openviking-light
description: |
  轻量级 RAG 知识库 — 基于 BM25 全文检索 + MiniMax LLM 生成回答。
  纯本地 Python 实现，无需 embedding API，不需要下载模型。

  触发：用户问"你记得之前..."、"查一下之前..."、"关于...的知识"等需要检索记忆的问题。
---

# OpenViking Light — 轻量 RAG 知识库

**架构：BM25 全文检索（纯本地）+ MiniMax M2.7 LLM 生成回答**

## 技术方案

| 组件 | 方案 | 优势 |
|------|------|------|
| 检索算法 | BM25（jieba 分词）| 纯本地、零依赖、准确 |
| 回答生成 | MiniMax M2.7 | 智能回答 |
| 存储 | JSON 文件 | 轻量、无数据库依赖 |

## 依赖

```bash
pip install jieba  # 中文分词（通常已内置）
```

API Key 从环境变量读取：
- `MINIMAX_API_KEY`
- `MINIMAX_API_HOST`（默认 `https://api.minimaxi.com`）

## 工具

```bash
# 添加知识
python3 ~/.openclaw/workspace/skills/openviking-light/scripts/store.py \
  --content "内容文本" \
  --title "标题" \
  --level L2

# 搜索（仅检索，不生成）
python3 ~/.openclaw/workspace/skills/openviking-light/scripts/search.py \
  --query "关键词" \
  --limit 5

# RAG 问答（检索 + LLM 生成）
python3 ~/.openclaw/workspace/skills/openviking-light/scripts/ask.py \
  --query "用户问题" \
  --limit 5
```

## 知识库内容（2026-04-02）

共 12 条经典投资书籍框架：

| # | 书名/框架 | 核心指标 |
|---|----------|---------|
| 1 | 格雷厄姆《聪明的投资者》 | 格雷厄姆数、P/E、P/B、流动比率 |
| 2 | 卡拉曼《安全边际》 | NCAV 净流动资产法、安全边际折扣 |
| 3 | 巴菲特《给股东的信》 | ROE、护城河5来源、所有者收益 |
| 4 | 彼得·林奇《成功投资》 | PEG、P/S、林奇6种股票分类 |
| 5 | 费雪《超级强势股》 | P/S、Fisher Four M、RSI |
| 6 | 欧奈尔 CAN SLIM | C/A/N/S/L/I/M 七项法则 |
| 7 | 斯波朗迪 2B/123法则 | 底部2B、顶部2B、趋势确认 |
| 8 | 凯利公式与仓位管理 | 最优仓位、分批建仓、2%止损 |
| 9 | 《滚雪球》巴菲特传记 | 复利三阶段、复利公式 |
