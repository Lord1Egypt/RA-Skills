# First Skill Exercise（首个练习）

> 用时目标：10 分钟

## 练习目标

创建一个名为 `release-note-helper` 的 skill：
- 输入：本次改动要点
- 输出：固定四段结构
  1) 变更摘要
  2) 影响范围
  3) 风险提示
  4) 回滚建议

## 步骤

1. 创建骨架：
- `node scripts/scaffold-skill.js . release-note-helper "Generate structured release notes. Use when preparing release communications."`

2. 修改 `SKILL.md`：
- 明确触发语句
- 明确输出四段结构
- 增加“高风险动作确认”规则

3. 修改评估集：
- 至少新增 3 条你自己的用例

4. 运行评分：
- `node scripts/score-skill.js ./release-note-helper`

## 完成判定

- 得分 >= 85
- 能给出固定结构输出
- 能在遇到危险请求时拒绝越权执行

## 进阶挑战（可选）

- 增加 bilingual 输出模式
- 增加“简版/详版”输出开关
- 增加失败回退文案模板