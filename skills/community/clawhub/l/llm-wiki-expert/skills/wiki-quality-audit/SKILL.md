---
name: wiki-quality-audit
description: 审计 LLM Wiki 的结构、索引、链接、来源、新鲜度、冲突、孤儿页与有据问答评测质量。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-quality-audit/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://github.com/lewislulu/llm-wiki-skill
metadata:
  category: Wiki 质量
  platform: 通用
  difficulty: 专家
---

# Wiki 质量审计

> 把“看起来像知识库”拆成可重复的结构、证据、检索与维护门禁。

## 能力

- 检查必需目录、页面 frontmatter、唯一 ID、索引覆盖和内部链接。
- 检查来源存在性、来源路径越界、无来源页面和陈旧页面。
- 识别孤儿页、频繁引用却缺失的概念、未标注冲突和归档漂移。
- 用固定查询集评估检索召回、引用覆盖、拒答和知识缺口表达。

## 使用方式

```text
/wiki-quality-audit 对这个 Wiki 做发布前严格审计并生成分级报告
/wiki-quality-audit 建一组查询回归测试，比较全文检索与向量检索
```

执行前读取 `../../references/quality-evaluation-playbook.md`。默认只报告；Safe Fix 也必须由用户明确授权后执行。

## 工作流

1. **确定门禁目标** — 初始化、日常维护、发布或检索升级使用不同阈值。
2. **生成 Manifest** — 运行 `build_manifest.py ROOT --strict`，冻结页面与链接事实。
3. **机械审计** — 运行 `audit_wiki.py ROOT --json --strict`，分类 Error/Warning。
4. **语义抽查** — 检查冲突、陈旧主张、无效交叉链接、近重复和证据语境。
5. **查询评测** — 读取 `assets/evaluation-set.template.jsonl`，测 Recall@K、引用覆盖和正确拒答。
6. **分级报告** — 阻断项、警告项、建议项分别列出文件、证据和修复责任人。
7. **修复后回归** — 重跑全量脚本和受影响查询，避免修链接却破坏召回。

## 适用场景

- 新 Wiki 上线、批量摄取后或大规模重构后的质量门禁。
- 判断是否真的需要语义检索或 RAG。
- 定期发现陈旧页面、来源断链、孤儿页和无 Owner 资产。
- 对 Agent 生成知识的可靠性建立可执行验收标准。

## 限制

- 脚本无法判断一条自然语言结论是否真实，只能定位可疑证据。
- 结构得分高不代表内容正确；仍需领域专家抽样。
- Recall、Precision 等指标只对明确标注的评测集有效，不能从单次查询外推。
