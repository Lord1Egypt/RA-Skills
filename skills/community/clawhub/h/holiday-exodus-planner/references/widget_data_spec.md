# Widget 数据规范

生成报告后，应同时使用 `show_widget` 工具以可视化方式展示报告。

使用 `holiday-exodus-planner/assets/report_widget.html` 作为 `widget_path`，并通过 `data` 参数传入以下 JSON 结构：

```json
{
  "holiday_label": "2026 年五一劳动节  |  5 月 1 日 - 5 月 5 日",
  "verdict": "一句话结论文本",
  "final_verdict": "判官最终裁决文本",
  "evaluation": [
    {
      "dimension": "拥挤风险",
      "value": "高",
      "level": "high|mid|low",
      "score": 8,
      "desc": "具体说明"
    }
  ],
  "travel_windows": [
    {
      "label": "推荐方案（请 1 天假）",
      "tag": "推荐",
      "primary": true,
      "leave": "4 月 30 日（周四）",
      "depart": "4 月 30 日早班高铁",
      "return_date": "5 月 4 日晚班",
      "duration": "5 天 4 晚",
      "advantage": "错峰优势说明"
    }
  ],
  "destinations": [
    {
      "name": "泉州",
      "label": "主推荐",
      "primary": true,
      "tags": ["文化", "美食"],
      "reasons": ["理由1", "理由2"]
    }
  ],
  "budget": [
    {"item": "交通（往返）", "range": "¥600 - ¥1,200", "note": "说明"}
  ],
  "budget_note": "预算总结说明",
  "warnings": ["不建议方案1", "不建议方案2"],
  "actions": [
    {"timing": "现在就做", "action": "具体动作"}
  ]
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `holiday_label` | string | 报告头部显示的节假日信息 |
| `verdict` | string | 一句话结论文本 |
| `final_verdict` | string | 判官最终裁决文本 |
| `evaluation[].dimension` | string | 评估维度名称 |
| `evaluation[].value` | string | 评估结果文本 |
| `evaluation[].level` | string | `high`（红色/风险高）、`mid`（黄色/中等）、`low`（绿色/优势） |
| `evaluation[].score` | number | 0-10 的数值，用于雷达图。分数越高 = 风险/成本越高 |
| `evaluation[].desc` | string | 评估说明 |
| `travel_windows[].primary` | boolean | `true` 为推荐方案，`false` 为备选方案 |
| `travel_windows[].leave` | string | 请假日期（可选，不请假方案不填） |
| `destinations[].primary` | boolean | `true` 为主推荐，`false` 为备选 |
| `destinations[].tags` | string[] | 目的地标签 |
| `destinations[].reasons` | string[] | 推荐理由列表 |
| `budget[].item` | string | 预算项目名 |
| `budget[].range` | string | 预算范围 |
| `budget_note` | string | 预算总结说明 |
| `warnings` | string[] | 不建议方案列表 |
| `actions[].timing` | string | 时间标签（现在就做/今天内做/本周内做） |
| `actions[].action` | string | 具体动作描述 |

## Widget 展示模块

- 报告头部（节假日名称 + 一句话结论）
- 多维评估雷达图 + 评估卡片
- 出行窗口方案卡片
- 目的地推荐卡片
- 预算表格
- 不建议方案警告列表
- 判官最终裁决高亮
- 下一步动作清单
