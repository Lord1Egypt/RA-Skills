# 调研模块

> **路径**：modules/researcher/
> **来源**：GitHub - novel-outline-researcher

## 模块说明

调研模块用于在用户提出创作需求后，进行市场调研和竞品分析，为创作提供方向指引。

## 核心功能

| 功能 | 说明 |
|------|------|
| 题材趋势分析 | 分析当前热门题材、平台偏好 |
| 竞品研究 | 分析同类型成功作品的特征 |
| 用户画像 | 分析目标读者群体特征 |
| 差异化建议 | 提供与竞品的差异化方向 |

## 输出格式

输出为 JSON 格式的调研报告，保存在 `research/{project-name}/research-report.json`

## 数据接口

```json
{
  "project_name": "项目名称",
  "created_at": "日期",
  "genre_analysis": {
    "current_trends": ["趋势1", "趋势2"],
    "platform_preference": "平台建议"
  },
  "competitor_analysis": [
    {
      "title": "竞品标题",
      "strengths": ["优势1", "优势2"],
      "differentiation_angles": ["角度1"]
    }
  ],
  "target_audience": {
    "age_range": "18-35",
    "preferences": ["偏好1", "偏好2"]
  },
  "writing_recommendations": ["建议1", "建议2"],
  "creative_directions": ["方向1", "方向2"]
}
```

## 触发词

- "调研"
- "市场分析"
- "竞品"
- "题材研究"
