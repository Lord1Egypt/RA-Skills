# {{NAME}}

> 大项目根（由 skill `project-organization` 创建，{{DATE}}）。
> ⚠️ 根目录只允许本 README（及 `.bigproject.json` 标记）。其余内容一律进子目录。

## 这个大项目要做什么

<范围 / 目标 / 主要负责人 / 起止时间>

## 目录结构

| 目录 | 用途 |
|------|------|
| `projects/` | 各子项目 / 阶段，每个一个子文件夹（每个必有 README.md） |
| `shared/` | 跨项目共享资源（只读引用，不在此写新文件） |
| `archive/` | 已结束项目归档（见 `archive/README.md` 索引） |
| `.tools/` | 工具 / 辅助脚本 + 操作日志（`.tools/journal.jsonl`、派生 `_log.md`） |
| `.trash/` | 软删除暂存（由 `scripts/trash.py` 管理，可恢复） |

## 子项目清单

见 `projects/_index.md`。

## 说明

- 新建子项目：`python <skills>/project-organization/scripts/new_subproject.py --name <项目名>`
- 结构自检：`python <skills>/project-organization/scripts/audit_project.py`
- 看操作日志：`python <skills>/project-organization/scripts/journal.py --tail 20`
- "删除"文件一律先移入 `.trash/`，不得直接硬删。
