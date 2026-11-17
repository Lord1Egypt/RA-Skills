# llm-wiki-expert — LLM Wiki 全流程专家

面向个人开发者、研究者与小团队的 LLM Wiki 知识工程技能库。它把 Wiki 当作由 Agent 持续维护的“编译产物”：原始来源保存在 `raw/`，概念、实体、来源摘要与决策页面写入 `wiki/`，查询结果只有在具有长期价值时才晋升为知识页面。

## 定位与边界

- 解决：Wiki 蓝图、来源摄取、知识编译、有据查询、增量维护、反馈治理和质量评测。
- 默认形态：Git 可追踪的 Markdown、相对链接、机器可读 frontmatter、全文检索。
- 不等同于：通用笔记应用、文档站生成器、向量数据库产品或无来源约束的聊天记忆。
- 面向规模：个人与小团队；大型组织可复用内容模型，但需另行设计权限、合规和分布式索引。

## Superpower 五层架构

```text
llm-wiki-expert/
├── SKILL.md       # L1 路由层
├── references/    # L2 七篇深层 playbook
├── skills/        # L3 七个细粒度能力
├── scripts/       # L4 脚手架、Manifest 与审计脚本
├── assets/        # L5 Wiki 契约、页面和评测模板
├── tests/         # 好/坏样本自动验证
├── AGENTS.md
└── README.md
```

加载时先读根 `SKILL.md`，按任务只打开一个相关 playbook；具体动作再调用对应子技能。确定性的结构、链接、索引和新鲜度问题交给脚本，不让 LLM 凭印象检查。

## 核心理念

1. `raw/` 是不可变证据层，`wiki/` 是可重编译知识层。
2. 页面按概念和用户任务组织，而不是一份来源对应一篇百科。
3. 查询必须报告证据范围与知识缺口，不用模型先验伪装成 Wiki 事实。
4. 先用索引和全文检索；只有真实评测证明召回不足时才加 Embedding/RAG。
5. 人类反馈进入审计队列，接受、部分接受、拒绝和延期都保留解决记录。

## 子技能清单

| 环节 | 子技能 | 描述 |
|------|--------|------|
| 蓝图 | `wiki-blueprint` | 定义范围、受众、问题集合、页面类型、命名和新鲜度契约 |
| 摄取 | `wiki-source-ingestion` | 保存不可变来源、补齐元数据、去重并判定 New/Update/Disputed/No material |
| 编译 | `wiki-knowledge-compilation` | 将来源编译为概念、实体、摘要、解释和决策页面并维护交叉链接 |
| 查询 | `wiki-grounded-query` | 索引 + 全文 + 可选语义检索，生成带页面与来源依据的答案 |
| 维护 | `wiki-maintenance` | 增量刷新、级联更新、冲突/过期标注、拆分合并和反馈闭环 |
| 审计 | `wiki-quality-audit` | 审计结构、索引、链接、来源、新鲜度、孤儿页和查询评测集 |
| 检索 | `rag-retrieval` | 为 Agent/应用构建 RAG 检索后端：分块、Embedding、混合检索、重排、检索评测 |

## 快速开始

```bash
# 整库安装（推荐）—— 路由 + references + scripts + assets
npx skills add skills-repo/llm-wiki-expert -g -y

# 单技能安装——只取一个细粒度能力
npx skills add skills-repo/llm-wiki-expert@wiki-blueprint -g -y
npx skills add skills-repo/llm-wiki-expert@rag-retrieval -g -y
```

创建与验证 Wiki：

```bash
python3 scripts/scaffold_wiki.py ~/docs/my-wiki --title "My Research Wiki" --strict
python3 scripts/build_manifest.py ~/docs/my-wiki --strict
python3 scripts/audit_wiki.py ~/docs/my-wiki --max-age-days 180 --strict
```

## 推荐工作流

```text
Blueprint → Scaffold → Ingest → Compile → Audit → Query → Promote → Refresh
```

1. `wiki-blueprint` 先定义 Wiki 宪章和成功问题，避免先堆文件再找结构。
2. 运行 `scaffold_wiki.py` 生成最小工作树。
3. `wiki-source-ingestion` 逐份保存来源，并做增量价值判定。
4. `wiki-knowledge-compilation` 串行更新共享索引和知识页面。
5. `audit_wiki.py` 与评测集共同阻止断链、无证据和召回退化。
6. `wiki-grounded-query` 回答问题；只有可复用综合才晋升到 Wiki。
7. `wiki-maintenance` 处理来源变化、反馈、过期和归档。

## 来源与改编原则

子技能均标注 `source.type: derived`。主要参考 [Karpathy LLM Wiki](https://skills.sh/astro-han/karpathy-llm-wiki/karpathy-llm-wiki)，并吸收 [Diátaxis documentation](https://github.com/mcollina/skills/tree/main/documentation) 的页面类型分离原则，以及 [llm-wiki-skill](https://github.com/lewislulu/llm-wiki-skill) 的反馈审计机制。其中 `rag-retrieval` 子技能改编自 [OrchestKit rag-retrieval](https://skills.sh/yonatangross/orchestkit/rag-retrieval)（1.2K installs），聚焦独立 RAG 后端的分块/Embedding/混合检索/重排/评测实现，与 Wiki 内部的语义检索决策形成互补。所有内容已重新组织为 skills-repo 的中文 superpower 架构，未直接复制上游技能。

## 许可

MIT
