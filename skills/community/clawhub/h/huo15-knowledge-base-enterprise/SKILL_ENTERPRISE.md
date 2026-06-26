---
name: huo15-knowledge-base-enterprise
displayName: 火一五知识库企业版
description: 火一五知识库企业版 - 在基础版基础上增加 Odoo Knowledge 同步功能。支持可见性控制、部门级权限、企业凭证管理。触发词：Odoo知识库、企业知识库、火一五知识库企业版、Odoo Knowledge。
version: 1.0.0
dependencies:
  required: ["huo15-knowledge-base"]
---

# SKILL_ENTERPRISE.md - huo15-knowledge-base Enterprise

> 企业版知识库技能 - 在基础版基础上增加 Odoo Knowledge 同步功能

---

## Enterprise 功能

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

### 导出选项

- **自动可见性** — 根据文章名匹配部门配置
  - 标题含"技术部"→ 仅技术部可见
  - 标题含"销售"→ 仅销售部可见
- **手动覆盖** — 通过命令行参数指定

---

## 与基础版的区别

| 文件 | 基础版 | Enterprise |
|------|---------|------------|
| `SKILL.md` | ✅ | ✅（基础文档）|
| `SKILL_ENTERPRISE.md` | ❌ | ✅（本文档）|
| `config.json` | ✅ | ✅ |
| `config.enterprise.json` | ❌ | ✅（Odoo 配置）|
| `scripts/kb-sync` | ✅ | ✅ |
| `scripts/kb-odoo-export` | ❌ | ✅ |
| `scripts/kb-odoo-export.py` | ❌ | ✅ |

---

## 安装

Enterprise 版本独立安装：

```bash
clawhub install huo15-knowledge-base-enterprise
```

或从 GitHub：

```bash
git clone https://github.com/huo15/huo15-knowledge-base-enterprise
```

---

## 版本历史

- **v0.5.0** — Enterprise 初始版本
  - Odoo Knowledge 同步
  - 可见性控制（private/workspace/department）
  - 部门级权限
