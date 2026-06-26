---
name: knowledge-orchestrator
description: [已整合] 知识库协调器已整合到 knowledge 统一入口技能
argument-hint: "[操作] [参数]"
---

# ⚠️ 已整合 - 请使用 knowledge 统一入口

> **本技能保留用于向后兼容，功能已整合到 `knowledge` 统一入口技能**
>
> **推荐使用：** `knowledge search/sync/link [参数]` 或直接使用本技能（自动转发）

---

# Knowledge Orchestrator（兼容层）

知识库协调器，统一管理 Zotero + Obsidian + IMA 三个平台。

## 迁移指南

**新用法：**
```
knowledge search RTHS --all
knowledge sync 笔记名称 --to-ima
knowledge link 10.1002/eqe.1234 RTHS 综述
```

**旧用法（仍然可用）：**
```
search RTHS --all
sync 笔记名称 --to-ima
```

## 核心功能
- 🔍 统一搜索（跨平台）
- ☁️ 云端同步（IMA）
- 🔗 关联文献和笔记

## 配置要求
| 服务 | 配置文件 | 说明 |
|------|---------|------|
| Zotero | `~/.config/zotero/api_key` | 文献库访问 |
| IMA | `~/.config/ima/client_id` | 客户端 ID |
| IMA | `~/.config/ima/api_key` | API 密钥 |

## 安全说明
- ✅ 仅发送到官方 API（api.zotero.org, ima.qq.com）
- ❌ 不要分享凭据
- ❌ 不要硬编码在脚本中
