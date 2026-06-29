# 项目状态

## 基本信息
- 项目名称: {{project_name}}
- 创建时间: {{created_at}}
- 最后更新: {{updated_at}}

## 当前阶段
{{current_stage}}

## 活跃需求
{{#active_requirements}}
- [{{id}}] {{title}} - {{status}}
{{/active_requirements}}

## 已完成
{{#completed_requirements}}
- [{{id}}] {{title}} - 完成于 {{completed_at}}
{{/completed_requirements}}

## 数据资产索引
{{#data_assets}}
- [{{status}}] {{name}} - {{location}} - 更新于 {{updated_at}}
{{/data_assets}}

## 备注
{{notes}}

---

## 填写范例

```markdown
# 项目状态

## 基本信息
- 项目名称: 销售数据分析平台
- 创建时间: 2026-06-10
- 最后更新: 2026-06-15

## 当前阶段
数据分析 + 可视化报表开发

## 活跃需求
- [REQ-20260610-001] Q2 区域销售额分析 - In Progress
- [REQ-20260611-001] 可视化报表生成 - Review
- [REQ-20260612-001] 数据清洗流水线 - Created

## 已完成
- [REQ-20260610-002] 数据源接入 - 完成于 2026-06-12
- [REQ-20260610-003] 环境搭建 - 完成于 2026-06-10

## 数据资产索引
- [可用] sales_q2.csv - /data/sales/ - 更新于 2026-06-10
- [可用] regions.json - /data/config/ - 更新于 2026-06-10
- [待验证] predictions_q3.csv - /data/output/ - 更新于 2026-06-14

## 备注
本周重点：完成可视化报表 review，开始数据清洗流水线。
下周期待：Q3 预测模型验证。
```

