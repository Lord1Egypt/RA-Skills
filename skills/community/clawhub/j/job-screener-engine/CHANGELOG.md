# Changelog

## 1.0.1 (2026-05-12)

### 修复
- SKILL.md 补全 frontmatter 字段（version, homepage），满足 ClawHub 发布要求
- README.md 发布指引更新为 ClawHub 流程

## 1.0.0 (2026-05-12)

初始版本发布。

### 新增
- 6 维评分框架：薪资匹配度、公司规模、技术成长、工作节奏、稳定性、区域可行性
- 7 步评估工作流：解析 → 搜索 → 一票否决 → 评分 → 补缺 → 报告 → 对比
- 一票否决机制：不满足底线的岗位直接标记，跳过评分
- 面试练手独立评估：与"是否入职"解耦，独立判断面试价值
- 信息不足降级策略：最多 3 问 + 中间值兜底 + 诚实标注
- 资金来源稳定性判断：账面盈利 ≠ 资金稳定
- 多岗位对比排序：同分时按用户优先级排序
- 首次配置向导 `references/setup_wizard.md`
- 用户画像模板 `references/user_profile.TEMPLATE.md`
- 版本元数据 `_meta.json`
- 最小权限设置 `allowed-tools: Read, WebSearch`
