---
name: patent-disclosure
description: Invention disclosure template, checklist, and Markdown-to-Word export (no third-party API token).
version: 1.0.0
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: python-docx
---

# 技术交底书 · Invention Disclosure

## 概述 | Overview

| | |
|---|---|
| **中文** | 交底书模板与检查清单；配合 **patent-search** 填现有技术对比；`export` 将完整 Markdown 转为 **Word 下载**。无需 9235 Token。 |
| **English** | Disclosure template & checklist; use **patent-search** for prior art; `export` full Markdown to **downloadable .docx**. No API token. |

触发词：技术交底书、发明披露、交底、invention disclosure、导出 Word。

---

## 工作流

```
收集发明信息 → checklist 追问补全 → patent-search 现有技术检索
→ 对比表 → 按 template 生成交底书 Markdown → export 导出 Word 下载
```

## 工具命令（patent-disclosure）

| command | 说明 |
|---------|------|
| `template` | 返回空白交底书模板（Markdown） |
| `checklist` | 返回撰写检查清单 |
| `export` | **必填 `content`**：完整交底书 Markdown → 生成 `.docx` 并提供下载链接 |

> mchat 下通过 `importlib` 加载同目录 `docx_export.py`，无需单独安装 pandoc。

用户要 Word / 下载时：**先写完正文**，再调用 `export`，把完整 Markdown 传入 `content`。
不要只传摘要；`invention_name` 可选，用于文件名。

## 撰写要点

1. 用 **patent-search** 检索现有技术，填入背景技术对比表
2. 按 template 章节填写技术方案、有益效果、实施例
3. 导出前确认发明名称、技术问题、核心创新点已写清

## 免责声明

可专利性初评仅供参考，不构成法律意见；正式申请须由专利代理人审核。

## 关联 Skill

| Skill | 用途 |
|-------|------|
| patent-search | 现有技术、法律状态 |
| patent-transaction | 若发明涉及已有挂牌专利 |
