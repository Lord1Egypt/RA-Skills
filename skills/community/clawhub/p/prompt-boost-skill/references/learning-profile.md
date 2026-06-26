# Learning Profile

若运行环境支持用户画像，本技能可记录每个用户的历史 query 模式。

## 可记录的偏好字段

- **top_domains**：高频领域列表，如 ["data-analysis", "tech-support"]
- **preferred_tools**：工具偏好，如 ["Python", "Pandas", "SQL", "Mermaid"]
- **preferred_outputs**：输出形式偏好，如 ["结构化方案", "表格", "流程图"]
- **clarification_tolerance**：追问容忍度，high / medium / low
- **default_assumptions**：默认假设（见下方）

## 默认假设示例

```json
{
  "analysis_style": "可视化+结构化",
  "coding_language": "Python",
  "document_style": "专业方案风格",
  "output_depth": "正式汇报"
}
```

## 使用原则

1. **当前意图优先**：当前输入与历史偏好冲突时，以当前输入为准
2. **历史只能作为默认值**：不能当成当前事实
3. **轻确认**：如依赖默认值，建议用一句话轻确认
4. **可纠正**：若用户本轮明确纠正，应更新画像

## 触发时机

- 用户在某一领域连续 3 次以上提问 → 更新 top_domains
- 用户明确偏好某种输出形式 → 更新 preferred_outputs
- 用户对某工具连续提及 → 更新 preferred_tools
