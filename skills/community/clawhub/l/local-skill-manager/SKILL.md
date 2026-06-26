---
name: local-skill-manager
description: >
  本地 Skill 目录的集中管理工具（"Skill 管家"）。当用户想要：
  (1) 列出或查询已安装的 Skill（系统级或用户级）；
  (2) 检查各 Skill 的版本信息；
  (3) 使用标准模板快速创建新的本地 Skill；
  (4) 删除或移除不再需要的 Skill。
  请使用此技能。
triggers:
  - manage skills
  - list skills
  - query skills
  - check skill versions
  - skill version
  - create skill
  - new skill
  - delete skill
  - remove skill
  - skill manager
  - 管理skill
  - 管理技能
  - 查询skill
  - 列出skill
  - 列出所有skill
  - 检查skill版本
  - skill版本
  - 新建skill
  - 创建skill
  - 删除skill
  - 移除skill
  - skill管家
  - 我有哪些skill
  - 查看skill
version: 1.0.0
---

# 本地 Skill 管家

本技能是 `skills/` 目录的集中管理工具，提供查询、监控、创建和删除 Skill 的能力，帮助你保持开发环境的整洁有序。

## 前置依赖

使用本技能前，请确认已安装依赖：

```bash
pip install -r requirements.txt
```

> `requirements.txt` 包含：`pyyaml`（用于解析 SKILL.md 的 YAML frontmatter）

---

## 功能说明

### 1. 查询与列出 Skill

列出所有已安装的 Skill（含系统级和用户级），显示名称、版本和描述。

**触发示例：**
- "列出我的 Skill"
- "我有哪些 Skill"
- "查询所有 Skill"

### 2. 版本检查

检查每个 Skill 的版本号，确认是否为最新版本。

**触发示例：**
- "检查 Skill 版本"
- "我的 Skill 是什么版本"

### 3. 创建新 Skill

使用标准目录结构（`scripts/`、`references/`、`assets/`）和 `SKILL.md` 模板快速脚手架一个新 Skill。

**触发示例：**
- "创建一个名为 'data-analyzer' 的新 Skill"
- "新建一个 Skill"

### 4. 删除 Skill

安全地移除一个 Skill 目录，内置多层安全保护：路径名格式校验、受保护 Skill 拦截、路径遍历防护、软链接警告、二次确认提示。

**触发示例：**
- "删除 'old-test-skill' 这个 Skill"

**可用参数：**
- `--dry-run`：预览将要删除的路径，不实际执行（推荐先用此参数确认）
- `--force`：跳过确认提示，直接删除（谨慎使用）

---

## 脚本说明

所有脚本位于 `scripts/` 目录：

| 脚本 | 功能 |
|------|------|
| `list_skills.py` | 扫描并列出所有 Skill |
| `check_versions.py` | 检查各 Skill 的版本元数据 |
| `create_skill.py` | 初始化新 Skill 的标准目录结构 |
| `delete_skill.py` | 安全移除指定 Skill 目录 |

---

## 执行规则

> **重要**：必须使用以下脚本执行操作，禁止直接使用 `ls` 或 `glob` 命令操作 `skills/` 目录。

脚本路径结构（从 Skill 根目录相对引用）：

```
# 列出所有 Skill
python scripts/list_skills.py

# 检查版本
python scripts/check_versions.py

# 创建新 Skill（将 skill-name 替换为你的 Skill 名称）
python scripts/create_skill.py "skill-name"

# 删除 Skill（将 skill-name 替换为要删除的 Skill 名称）
# 推荐先用 --dry-run 预览，确认无误后再实际删除
python scripts/delete_skill.py "skill-name" --dry-run
python scripts/delete_skill.py "skill-name"
```

**注意**：如果你的平台将 Skills 存放在特定子目录下（如 `.trae/skills/`），请在命令前加上对应的完整路径前缀，例如：

```
python .trae/skills/local-skill-manager/scripts/list_skills.py
```
