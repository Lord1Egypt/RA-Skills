# Profile 生成 Prompt（Profile Builder）

## 任务

根据 `profile_analyzer.md` 的结构化草案，生成最终的 `profile.md` 文件。

目标：写出**准确、可复用、可约束检索理解与回答风格**的人物画像，严格对齐 `docs/PRD.md` 的本地落盘格式。

资料来源优先级：
1) 人物记忆库
2) Wikipedia
3) 你自身的常识性背景知识（仅补充语境；不确定必须标注）

---

## 输出要求

- 语言：中文（除非用户要求其他语言）
- 不要写“小说化传记”；要写“可执行的认知约束与风格约束”
- 不要复制粘贴 Wikipedia 原文；必要引用保持极短
- 不要把推测写成事实；对争议或不确定内容要明确标注

---

## 输出模板（直接输出完整 Markdown 文件）

```md
# {display_name}

- slug: {slug}
- profile_version: {profile_version_or_local}

## Identity
{用 1-3 段 + 要点描述：是谁、时代/地区、领域与代表标签；事实优先}

## Mental Models
{用要点列出方法论/判断标准/常见取舍；尽量写成“当…时，倾向于…”}

## Expression Styles
{用要点描述表达风格；必要时给少量“短句级”示例（避免长引用）}

## Personality
{用要点描述性格维度与偏好；MBTI 等仅作框架，必须标注不确定性}

## Timeline
{按时间顺序列出关键节点；每条含时间与语境}

## Adjustments
（用户个人修订，由 Agent 在对话中记录）
```

---

## 关键写作约束（必须遵守）

1) 每一层至少 6 行有效信息（除非原材料不足；不足则写明“原材料不足”并列出缺口）。
2) Timeline 必须体现“观点/策略的语境变化”（如果 dynamic profile 提供）。
3) 不要在 profile 里写“我会怎么回答用户”；那属于 `SKILL.md` 运行规则。
