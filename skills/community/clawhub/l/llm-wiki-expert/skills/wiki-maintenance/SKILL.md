---
name: wiki-maintenance
description: 运行 LLM Wiki 的增量刷新、级联更新、冲突/过期治理、页面拆并、反馈闭环和归档流程。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-maintenance/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://github.com/lewislulu/llm-wiki-skill
metadata:
  category: Wiki 维护
  platform: Markdown
  difficulty: 专家
---

# Wiki 增量维护

> 知识库不是一次生成的文档，而是一组有 Owner、状态、新鲜度和变更历史的长期资产。

## 能力

- 根据来源、代码或版本变化计算受影响页面并进行级联刷新。
- 管理 Draft、Active、Disputed、Outdated、Deprecated、Archived 状态。
- 处理页面拆分、合并、重命名、重定向和查询归档。
- 将人类反馈转化为可审计的接受、部分接受、拒绝或延期记录。

## 使用方式

```text
/wiki-maintenance 官方文档升级后刷新所有受影响页面并保留旧结论
/wiki-maintenance 处理 audit/open 中的反馈，不删除拒绝记录
```

开始前读取 `../../references/maintenance-governance-playbook.md`。涉及删除、重命名或大范围重写时，先给出影响清单并等待确认。

## 工作流

1. **发现变化** — 比较来源哈希、版本、更新时间、人工反馈和审计报告。
2. **建立影响集** — 搜索引用该来源、实体、页面或主张的全部非归档页面。
3. **分类动作** — Refresh、Dispute、Supersede、Split、Merge、Deprecate 或 Archive。
4. **按风险执行** — 来源元数据可机械修复；语义冲突和大规模拆并需人工确认。
5. **维护兼容** — 重命名时保留 Redirect/alias，避免打断已有查询与链接。
6. **关闭反馈** — 写 Resolution，移动到 resolved；拒绝记录同样保留理由。
7. **更新索引、Manifest 与日志** — 保证变更后可追溯、可查询、可回滚。
8. **回归验证** — 运行质量审计和受影响的查询评测用例。

## 适用场景

- 官方文档、论文版本、代码 API 或产品事实发生变化。
- Wiki 出现重复页、超长页、过时页和命名漂移。
- 团队通过审计文件提交纠错或补充证据。
- 定期季度维护、Owner 交接或主题归档。

## 限制

- 不静默删除历史结论或人类反馈。
- 不把文件修改时间直接等同于知识更新时间。
- 不保证外部系统副作用可回滚；本技能只治理 Wiki 资产。
