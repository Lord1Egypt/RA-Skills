# agent.md — Codex 兼容垫片

> 本文件为 Codex 执行器保留。完整项目规范在 `CLAUDE.md`，本文件仅提供 Codex 所需的最小上下文。
> 如果你是 Claude Code，请忽略本文件，直接遵循 CLAUDE.md。

## 角色

当前执行器是"龙虾爬虫技能"项目的任务代理，职责是按 `docs/TODO.md` 的顺序逐步完成爬虫系统的开发任务。项目目标：定向抓取 Webnovel、ReelShorts 等网站内容，支持站点地图沉淀、定时调度、内容分级和钉钉播报。

## 执行要求

- 完整规范见 `CLAUDE.md`，以下为核心摘要
- **最高优先级**：检查 `bug_fix/` 目录（排除 `resolved/`），如有 `.md` 文件则为紧急 bug，优先修复后移入 `bug_fix/resolved/`
- 只执行一个 `ACTIVE_TODO`
- 执行前必须阅读：`docs/TODO.md`、`docs/STATE.md`、`docs/FEEDBACK.md`、`CLAUDE.md`
- 反馈自检：阅读 `docs/FEEDBACK.md` 中所有 `status: open` 条目，将其 action 作为强制约束
- 只修改完成该任务所必需的文件
- 必须更新 `docs/STATE.md`
- 仅在任务真实完成时勾选 `docs/TODO.md`

## 编码规范（摘要）

1. 新增/删除第三方依赖时同步更新 `requirements.txt`
2. 项目结构/CLI 用法/启动方式变化时同步更新 `README.md`
3. Python 代码遵循 PEP 8，Google 风格 docstring，所有公开函数需类型注解
4. YAML 配置键名 snake_case

## 输出 JSON

```json
{
  "run_status": "success | blocked | failed",
  "active_todo": "Txxx",
  "completed": true | false,
  "summary": "short summary",
  "bugs_fixed": ["filename.md", ...],
  "files_changed": ["a", "b"],
  "state_updated": true | false,
  "todo_updated": true | false,
  "next_todo": "",
  "blockers": []
}
```
