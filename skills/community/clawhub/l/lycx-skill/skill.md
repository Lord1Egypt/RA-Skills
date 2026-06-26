# Skill: summarize_key_points
## 1. 基本信息
- 技能ID：skill_summary_001
- 版本：v1.0
- 描述：对长文本、文章、对话记录进行总结，并提取核心要点
- 适用场景：长文阅读、会议纪要、报告提炼
- 触发条件：用户包含“总结”“提炼”“要点”“太长帮我看”

## 2. 输入输出
- 输入：
  - text：字符串，待处理文本
  - length：可选，short/normal/detail
- 输出：
  - 总结（summary）
  - 要点列表（key_points）
  - 原文长度、输出长度

## 3. 执行流程
1. 检查文本是否为空、是否过长
2. 调用大模型做总结
3. 按列表格式提取要点
4. 返回结构化结果

## 4. 约束
- 不修改原意
- 不编造信息
- 敏感内容拒绝处理

## 5. 示例
用户：帮我总结这段内容
AI：调用 summarize_key_points → 返回 summary + key_points