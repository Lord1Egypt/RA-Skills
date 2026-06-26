# 改写记录 — Round 1

## 目标模式
- P01: 知识库基础设施缺失
- P02: 表达层未调用
- P03: 意图标记缺失
- P04: 搜索源未限定

## 改动清单
1. **SKILL.md 阶段①**：明确知识库路径 `knowledge/investor-education/wiki/`，增加"若目录不存在，直接跳至阶段②"的降级逻辑。
2. **SKILL.md 阶段②**：限定搜索源为官方域名（`site:nerc.edu.cn` 等），避免自媒体干扰。
3. **SKILL.md 阶段③**：增加"意图标记"指令，明确输出 `intent: plain/writes/card/wechat/multi`。
4. **SKILL.md 阶段④**：明确指令"调用 expression-layer，传入 content + intent"，不再直接输出 Markdown。
5. **SKILL.md 阶段⑤**：明确入库路径和元数据格式（使用频次/理解难度/关联偏误）。
6. **创建知识库骨架**：`knowledge/investor-education/{raw,wiki/{entities,concepts,summaries}}`
7. **导入种子数据**：3 个高频知识点 Wiki 页面（定投、市盈率、损失厌恶），含定义/逻辑/误区/关联偏误/元数据。

## 预期效果
- Prompt 1（定投）：阶段①命中 Wiki → 阶段③标记 intent: plain → 阶段④调用 expression-layer → 返回大白话 + 卡片。
- Prompt 2（北交所）：阶段①未命中 → 阶段②搜索官方源 → 阶段③标记 intent: writes → 阶段④调用 expression-layer → 返回文章。
- Prompt 3（公众号）：阶段③标记 intent: wechat → 阶段④调用 expression-layer → 返回公众号推文。
- 所有 Prompt：阶段⑤执行入库，追加元数据。
