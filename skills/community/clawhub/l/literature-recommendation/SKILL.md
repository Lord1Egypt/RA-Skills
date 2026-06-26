---
name: literature-recommendation
description: "用于论文推荐、文献推荐、论文匹配、按偏好找论文、根据研究方向推荐论文；从数据库读取成员偏好，召回候选论文并输出给OpenClaw。"
license: MIT
---

# Literature Recommendation

## What it does

This skill implements a minimal literature recommendation workflow for a team:

- store member research profiles
- fetch candidate papers from arXiv
- score papers with lightweight rules
- persist run history and recommendation output in PostgreSQL
- output personal card payload for OpenClaw delivery

## 触发词

优先使用中文触发，建议包括：

- 论文推荐
- 文献推荐
- 论文匹配
- 按偏好找论文
- 根据研究方向推荐论文
- 给我推荐相关论文
- 帮我推荐几篇论文

## Usage

Run the CLI from the project root:

```bash
python entrypoints/run_paper_matching.py --dry-run
```

## Workflow

1. Load member profiles from PostgreSQL.
2. Fetch candidate papers from arXiv.
3. Score papers with direction and keyword matching.
4. Store papers and recommendations in PostgreSQL.
5. Build delivery payloads: personal card JSON only.
6. Return payload to OpenClaw for actual Feishu sending.

## 职责边界（规范）

- 本 Skill 负责：
	- 从数据库读取成员偏好
	- 从 arXiv 召回候选论文
	- 用硬规则打分并给出规则理由（rule_reason）
	- 输出 openclaw_rerank_payload 与 personal_cards
- OpenClaw 负责：
	- 读取 openclaw_rerank_payload 并调用 LLM 做语义复排
	- 判定是否推荐（keep/drop）与最终排序
	- 生成最终推荐理由（可覆盖 rule_reason）
	- 推荐理由需解释论文摘要核心内容，并指出与成员偏好的匹配点
	- 执行私聊发送和定时调度

## 输出契约（推荐结果）

- 候选输入给 OpenClaw：openclaw_rerank_payload
	- strategy: hard_rule_recall
	- llm_reason_contract:
		- language: zh-CN
		- reason_style: explanatory
		- required_source:
			- paper.title
			- paper.abstract
			- profile.primary_direction
			- profile.keywords
		- forbidden:
			- title_only_reason
		- reason_generation_steps:
			- 先阅读 paper.abstract 提取论文核心方法/任务
			- 再对照成员偏好字段判断匹配点
			- 最后生成一句概括 + 一句匹配说明
		- must_include:
			- 论文核心内容一句话概括
			- 与该成员偏好匹配的具体点
		- max_length: 120
	- by_member[record_id].candidates[*]:
		- paper_id
		- rule_score
		- rule_reason
		- paper (title/abstract/tags/url 等)
	- llm_output_schema:
		- by_member[record_id].items[*]:
			- paper_id
			- keep
			- rank
			- score
			- reason
- 最终发送：delivery_payload.personal_cards
	- record_id
	- paper_id
	- rank
	- score
	- reason
	- paper_title
	- paper_abstract
	- card

## Notes

- The MVP uses rule-based matching only.
- The weekly push is part of the MVP, not a later iteration.
- The payload now targets personal direct messages only.
- Feishu sending, Bitable sync, and feedback storage are handled by the data-hub skill.
- This skill is invoked manually from chat or by OpenClaw orchestration; it does not schedule itself.
- If you need timed execution, let OpenClaw or an external scheduler trigger this skill on a schedule.
