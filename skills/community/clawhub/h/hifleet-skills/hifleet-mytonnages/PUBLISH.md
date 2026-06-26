# ClawHub 发布说明

在**本 Skill 源码目录**下执行（含 `SKILL.md`、分册 `*.md`、`scripts/*.py`）。仓库内文件夹名可与发布名不同；示例以目录名 **`hifleet-charter-ai`** 为例，**ClawHub 技能名**须为 **`hifleet-mytonnages`**（与 `SKILL.md` frontmatter `name` 一致）。

## 首次发布（v1.0.0）

```bash
clawhub publish ./hifleet-charter-ai --name hifleet-mytonnages --version 1.0.0
```

发布前请将 **`SKILL.md` frontmatter 中的 `version`** 与命令行 **`--version`** 保持一致（当前均为 **1.1.0**）。

**v1.2.0**：移除公开船盘/公开货盘（原 C/D）；**路由 C** 改为 **预抵船舶**（`DESTINATION_SEARCH_API.md`）；单行补充信息默认公网 **`enrich-row`**；新增 **`USER_WORDING.md`**（对用户口语规范）。

**v1.1.0**：新增路由 C/D（公开船盘/货盘，**已在 v1.2.0 移除**）；**`FIRST_SETUP.md`**；路由 A/B/C/D；解锁 `typeCode` 区分班轮/公开船/货盘。

**v1.0.0** 包含：`SKILL.md` 总纲；**`SKILL_CONTEXT.md`**、**`ROUTING_AND_WHEN.md`**、**`MEMORY_LANCEDB.md`**、**`WORKFLOW_1_MAIL.md`** / **`WORKFLOW_2_MAIL.md`**、**`WORKFLOW_OUTPUT.md`**；路由 B 契约 **`SCHEDULE_API.md`**；邮件解析字段 **`PARSE_SCHEMA.md`**；示例配置 **`CONFIG.example.md`**；脚本 **`scripts/charter_facts_tool.py`**、**`scripts/desensitize_for_llm.py`**。发布前建议用 UTF-8 字节数确认 **`SKILL.md`** 未超过平台单文件体积限制。

---

## 发布前检查（ClawHub「仅文本」）

当前平台可能**不允许**带点前缀的配置/忽略文件入包。发布或打 zip 前请确认**待发布目录内**不存在：

- 任意路径下的 `__pycache__` 目录与 `*.pyc`、`*.pyo`
- `*.sqlite3`、`.env`、`.venv/`（本地调试残留）
- 任何非文档约定的二进制或禁用扩展名

Windows 可在资源管理器中删除 `scripts\__pycache__`，或在仓库根执行清理后再 `clawhub publish`。
