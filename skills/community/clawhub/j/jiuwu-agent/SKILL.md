---
name: jiuwu-agent
description: 调用久吾智能体API进行文本或文件分析处理。支持两种调用方式：(1) 文本内容分析 - 传入name(智能体名称)、docno(文档编号)、content(文本内容)；(2) 文件分析 - 传入name、docno和files(文件列表)进行智能评审。适用于合同评审、需求评审、文档审查等场景。当用户要求评审合同、分析条款、审查文档、需求评审、合同条款分析、或需要对文本和文件进行AI智能分析时触发。
---

# 久吾智能体

调用久吾智能体API进行文本或文件分析。

## 环境配置

Token 从环境变量 `JIUWU_CORE_TOKEN` 读取，OpenClaw 会自动注入 `env.vars` 中的变量。也可在 `~/.openclaw/workspace/.env` 或 `~/.openclaw/.env` 中配置。

## 脚本调用（优先使用）

**始终使用 `scripts/call_agent.py`，不要直接 curl。**

### 文本分析

```bash
python scripts/call_agent.py text -n "智能体名称" -d "文档编号" -c "要分析的文本内容"
```

示例：
```bash
python scripts/call_agent.py text -n "合同评审" -d "JWSO20260001" -c "合同金额：10万元，付款方式：先款后货"
```

### 文件分析

```bash
python scripts/call_agent.py file -n "智能体名称" -d "文档编号" -f 文件路径1 文件路径2 ...
```

示例：
```bash
python scripts/call_agent.py file -n "信息化需求评审" -d "JWBG20260001" -f "需求文档.docx"
```

**支持的文件格式**: `.doc`, `.docx`, `.pdf`, `.xls`, `.xlsx`, `.txt`

### 常用智能体名称

- `合同评审` - 合同条款分析
- `信息化需求评审` - 需求文档审查
- `信息化问题评审` - 问题分析

## 脚本参数说明

| 参数 | 缩写 | 说明 |
|-----|-----|------|
| `--name` | `-n` | 智能体名称 |
| `--docno` | `-d` | 文档编号 |
| `--content` | `-c` | 要分析的文本（text子命令） |
| `--files` | `-f` | 文件列表（file子命令） |

## 响应格式

成功时返回 `success: true` 和 `data.reviewOpinion`（分析结果文本）。失败时返回 `success: false` 和错误信息。

## 常见错误

- **匹配到多个智能体**：`name` 需更精确，如用 `信息化需求评审` 而非 `信息化`
- **未获取到智能体**：检查 `name` 是否正确，确认智能体存在
