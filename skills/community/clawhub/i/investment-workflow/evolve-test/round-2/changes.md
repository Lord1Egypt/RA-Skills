# 改写记录 — Round 2

## 目标模式
- P20: 数据罗列无结论
- P21: 合规拦截过度
- P22: 表达层未调用

## 改动清单
1. **SKILL.md 阶段⑤**：增加"必须输出结论 + 置信度"指令。
2. **SKILL.md 阶段③**：增加"合规转化"协议（拒绝 → 转化为分析/投教）。
3. **SKILL.md 阶段⑥**：明确调用 expression-layer，传入 content + intent。
4. **SKILL.md 常见错误**：增加 P20/P21/P22 的错误说明与解决。

## 预期效果
- Prompt 1 应该不再出现只罗列数据的情况。
- Prompt 2 应该转化为投教内容，而非直接拒绝。
- Prompt 3 应该调用 expression-layer，输出格式统一。

## 实际效果
- 全部符合预期，Round 2 收敛。
