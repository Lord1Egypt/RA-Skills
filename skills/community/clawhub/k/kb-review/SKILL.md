---
name: kb_review
description: Generate and save knowledge-base reviews such as literature reviews, research gaps, onboarding notes, stage summaries, and experiment suggestions based on existing KB sources.
---

# Skill: kb_review — 综述 / 研究缺口 / onboarding / 实验建议

## 用途

基于知识库中已经存在的资料做跨文档综合，不使用通用知识硬凑答案。

支持：

- 领域综述
- 研究缺口分析
- 方法对比
- 实验改进建议
- 新人 onboarding 文档
- 阶段总结

默认保存回知识库。

## 触发条件

Activate when:

- “写一份 X 综述”
- “X 有哪些研究缺口”
- “对比库里几种方法”
- “根据团队资料给新人入门路线”
- “我的实验结果不理想，库里有没有改进思路”

Do NOT activate when:

- 单点查找 → `query_kb`
- 存资料 → `ingest_document`

## 执行流程

1. 用范围解析脚本确定个人库/团队库/项目范围；群聊时必须通过 `GroupSubject -> chat_bindings.json` 找到团队，不允许读取个人库。

```bash
python3 scripts/resolve_review_scope.py \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid> \
  --question "<用户问题>"
```

2. 读取 catalog。
3. OpenClaw 选择相关 concept/review/project/summary 页面。
4. 精读页面。
5. 只基于精读内容生成综述/建议。
6. 默认保存回知识库。

## 保存综述

```bash
python3 scripts/save_review.py \
  --owner <owner> --repo <repo> \
  --title "<主题>·综述" \
  --review_file /tmp/paperkb/draft_review.md \
  --brief "<一句话简介>" \
  --scope team \
  --project_id <project_id>
```

## 保存 onboarding

```bash
python3 scripts/generate_onboarding.py \
  --owner <owner> --repo <repo> \
  --title "<方向>新人入门路线" \
  --file /tmp/paperkb/draft_onboarding.md \
  --brief "<一句话简介>" \
  --project_id <project_id>
```

## 回答要求

- 必须有来源小节。
- 知识库资料不足时明确说明不足。
- 不允许补通用知识。

## 脚本清单

- `resolve_review_scope.py`：解析私聊/群聊综述范围
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `save_review.py`：保存综述
- `generate_onboarding.py`：保存 onboarding 文档
