---
name: llm-wiki-expert
description: >-
  LLM Wiki 全流程专家：为个人与小团队设计、搭建和运营由 Agent 持续编译的 Markdown 知识库。
  覆盖 Wiki 蓝图、来源摄取与溯源、概念/实体/解释页面编译、有据查询、增量维护、冲突与过期治理、
  图谱/索引/引用质量审计及评测门禁。触发词："LLM Wiki"、"Karpathy Wiki"、"AI 知识库"、
  "知识编译"、"Wiki ingest"、"Wiki lint"、"知识库维护"、"有据问答"。
agent_created: true
metadata:
  version: 1.0.0
  category: 知识工程
  difficulty: 专家
  architecture: superpower
---

# LLM Wiki 全流程专家

> 把 AI 助手变成知识库架构师、编译器与维护者：原始资料可追溯，知识页面可导航，回答有证据，更新可审计。

本技能采用 **superpower 架构**：根 `SKILL.md` 只做路由；方法论按需加载 `references/`；
独立动作使用 `skills/`；确定性工作交给 `scripts/`；可复用契约与页面骨架位于 `assets/`。

## 何时使用

- 从零设计个人、项目或研究主题的 LLM Wiki
- 把网页、论文、会议记录、代码文档等来源摄取为可追溯知识
- 将原始资料编译成概念、实体、来源摘要、决策与解释页面
- 基于 Wiki 回答问题，并区分已知、冲突、过期与证据缺口
- 增量刷新 Wiki，处理上游变化、页面合并、拆分、弃用和人类反馈
- 审计死链、孤儿页、索引遗漏、来源断链、陈旧页面和评测覆盖
- 在纯 Markdown、全文检索与语义检索之间选择合适的检索层级
- 为 Agent 或应用搭建独立的 RAG 检索后端（分块、Embedding、混合检索、重排、评测）

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|-------------|---------------------|
| 全生命周期与操作状态机 | `references/wiki-lifecycle-playbook.md` | lifecycle ingest compile query refresh retire 操作日志 |
| 内容模型、页面类型与导航 | `references/information-architecture-playbook.md` | taxonomy Diátaxis concept entity summary decision index |
| 来源、引用、冲突与证据 | `references/source-grounding-playbook.md` | provenance citation evidence disputed outdated raw hash |
| 检索、查询、综合与升级 | `references/retrieval-and-synthesis-playbook.md` | grep full-text semantic retrieval query synthesis promote |
| 刷新、责任、反馈与治理 | `references/maintenance-governance-playbook.md` | owner freshness SLO audit feedback deprecate migration |
| 质量模型、测试集与门禁 | `references/quality-evaluation-playbook.md` | coverage deadlink orphan precision recall eval gate |
| 定义范围、受众、页面契约 | `skills/wiki-blueprint/SKILL.md` | blueprint charter scope audience schema naming |
| 摄取和归档原始来源 | `skills/wiki-source-ingestion/SKILL.md` | source ingest raw metadata immutable triage |
| 编译结构化知识页面 | `skills/wiki-knowledge-compilation/SKILL.md` | compile split merge concept entity summary crosslink |
| 进行有据查询与综合 | `skills/wiki-grounded-query/SKILL.md` | grounded query cite unknown confidence archive |
| 增量更新与生命周期治理 | `skills/wiki-maintenance/SKILL.md` | refresh cascade stale conflict supersede audit log |
| 运行 Wiki 质量审计 | `skills/wiki-quality-audit/SKILL.md` | lint manifest link source index staleness evaluation |
| 构建 RAG 检索管线 | `skills/rag-retrieval/SKILL.md` | rag retrieval embedding 向量检索 混合检索 rerank 重排 分块 chunk 检索评测 recall |
| RAG 检索深度实现（分块/重排/评测） | `references/rag-retrieval-playbook.md` | rag chunk embedding rerank recall 分块 重排 评测 RRF 混合检索 |

## 内置脚本（确定性、可重复执行）

- `scripts/scaffold_wiki.py TARGET --title TITLE [--dry-run] [--json] [--strict]` — 安全生成 Wiki 骨架，不覆盖已有文件
- `scripts/build_manifest.py ROOT [--output PATH] [--json] [--strict]` — 构建机器可读页面/来源/链接清单
- `scripts/audit_wiki.py ROOT [--max-age-days N] [--json] [--strict]` — 检查结构、索引、链接、来源和新鲜度

```bash
python3 scripts/scaffold_wiki.py ./my-wiki --title "Agent Runtime" --strict
python3 scripts/build_manifest.py ./my-wiki --strict
python3 scripts/audit_wiki.py ./my-wiki --max-age-days 180 --strict
```

## 模板资源

- `assets/wiki-config.template.yml` — 范围、受众、页面类型、引用和新鲜度策略
- `assets/WIKI.template.md` — Wiki 宪章与 Agent 运行契约
- `assets/index.template.md` — 人类导航入口与页面登记骨架
- `assets/source.template.md`、`article.template.md` — 来源与知识页面模板
- `assets/audit.template.md` — 人类反馈与解决记录模板
- `assets/evaluation-set.template.jsonl` — 有据问答回归集模板

## 核心原则（始终遵循）

1. **Raw 不可改，Wiki 可重编译**：原始来源只追加；解释页面可合并、拆分和重写。
2. **证据先于文案**：精确数字、日期、引语和关键结论必须定位到来源；缺证据就标未知。
3. **结构服务查询**：页面按用户任务和概念边界拆分，不按来源文件机械复制。
4. **简单检索优先**：先索引 + `rg` 全文；规模和召回证据不足时才引入语义检索。
5. **渐进式加载**：先读本路由和一个相关 playbook，再加载子技能或脚本。
6. **明确边界**：脚本只检查确定性事实；冲突裁决、知识取舍和发布仍需人类判断。

## 与其他技能协作

- 深度调研与学术引用 → `skills-repo/academic-researcher`
- README、API 文档和图表写作 → `skills-repo/docs-writer`
- 个人长期记忆与上下文治理 → `skills-repo/productivity-master`
- 网站、检索 API 或 RAG 实现 → `skills-repo/ai-fullstack-engineer`
- 仓库创建与发布门禁 → `skills-repo/skills-repo-admin`
