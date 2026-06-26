---
name: huo15-knowledge-base-enterprise
displayName: 火一五知识库企业版
description: 火一五知识库企业版 - 基于 huo15-knowledge-base 构建，额外支持 Odoo Knowledge 同步功能。支持可见性控制、部门级权限、企业凭证管理。触发词：Odoo知识库、企业知识库、火一五知识库企业版、Odoo Knowledge。
version: 1.0.5
dependencies:
  required: ["huo15-knowledge-base"]
---

# SKILL.md - huo15-knowledge-base-enterprise

> 火一五知识库企业版 - 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案
> **在基础版基础上增加 Odoo Knowledge 同步功能**

---

## 版本历史

- **v1.0.0** — Enterprise 初始版本
  - Odoo Knowledge 同步
  - 可见性控制（private/workspace/department）
  - 部门级权限
- **v0.7.2** — 基础版最终版本

---

## 企业版功能

| 功能 | 基础版 | Enterprise |
|------|---------|------------|
| 知识库管理 | ✅ | ✅ |
| LLM 自动编译 | ✅ | ✅ |
| memory-evolution 桥接 | ✅ | ✅ |
| **Odoo Knowledge 同步** | ❌ | ✅ |
| **可见性控制** | ❌ | ✅ |
| **部门级权限** | ❌ | ✅ |

---

## Odoo Knowledge 同步

### 配置

创建 `config.enterprise.json`：

```json
{
  "odoo": {
    "url": "https://huo15.com",
    "db": "huo15",
    "uid": 5,
    "password": "your_password"
  },
  "visibility": {
    "default": "workspace",
    "departments": {
      "技术部": [2, 3, 5],
      "销售部": [7, 8, 9]
    }
  }
}
```

### 可见性控制

| 可见范围 | 说明 |
|----------|------|
| `private` | 仅创建者可见 |
| `workspace` | 工作区全员可见（默认）|
| `department:部门` | 指定部门可见 |

**实现机制**：
- 通过 `knowledge.article.member` 表管理成员权限
- 部门配置中的 user IDs 会自动转换为 partner IDs
- 为每个有效用户创建 `article.member` 记录（permission: write）

**注意**：需要确保配置的 user IDs 在 Odoo 中存在且有关联的 partner。

### 命令

```bash
# 导出所有 wiki 文章到 Odoo Knowledge
kb-odoo-export

# 仅导出指定文章
kb-odoo-export --article odoo-19-crm

# 预览模式（不实际创建）
kb-odoo-export --dry-run

# 设置默认可见性
kb-odoo-export --visibility private
```

### 工作流程

```
kb-ingest --url "https://..."
kb-compile
kb-odoo-export          # 同步到 Odoo Knowledge
```

---

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `kb-odoo-export` | **企业版新增** - 导出到 Odoo Knowledge |
| `kb-odoo-export.py` | **企业版新增** - Odoo API 调用器 |
| `kb-ingest` | 入库文档（自动抓取网页内容）|
| `kb-compile` | LLM 自动编译 raw → wiki |
| `kb-search` | 搜索知识库 |
| `kb-lint` | 体检知识库（自愈）|
| `kb-sync` | 桥接 memory-evolution |

---

## Agent 隔离架构

**设计原则：**
- Skill 代码共享，不重复安装
- 数据目录在每个 Agent 的 `agent/kb/` 下，完全隔离
- 通过 `AGENT_DIR` 环境变量自动检测当前 Agent 上下文

---

## 触发词

- **Odoo知识库**、"同步 Odoo 文档"、"入库 Odoo"
- **企业知识库**、"Odoo Knowledge"
- "编译知识库"、"体检知识库"

---

## 配置

Agent 专属配置：`~/.openclaw/agents/{agent-id}/agent/kb/config.json`

```json
{
  "version": "1.0.0",
  "paths": {
    "raw": "raw",
    "wiki": "wiki",
    "cache": "cache"
  },
  "odoo": {
    "url": "https://huo15.com",
    "db": "huo15"
  },
  "visibility": {
    "default": "workspace"
  },
  "memory_bridge": {
    "enabled": true,
    "auto_sync": false
  }
}
```

---

## 凭证管理

**企业凭证存储规则：**
- 所有账号密码、API Token 必须存储到公司 Odoo 系统知识库
- 不能只存在本地文件
- 位置：Odoo → 知识库 → 技术部凭证
