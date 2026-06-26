---
name: local-api-chart-generator
description: 专为调用本地数据接口并生成图表展示定制的 Skill。接收自然语言指令（如“我要最近一年燃油类型为天然气的扭矩占比”），自动提取参数，请求本地接口，生成 HTML 柱状图并返回完整的 HTML 源码。
version: 1.0.0
author: 小果
tags: [local-api, chart, echart, bar-chart, data-visualization]
---

# 本地接口数据图表生成器 (Local API Chart Generator)

**重要：这是一个专为 API 调用设计的技能，必须严格遵守以下执行流程。**

## 🔄 强制执行流程 (Strict Workflow)

### 第一步：提取参数
从用户指令中提取：
- **燃油类型（必传）**：如 `柴油,天然气`
- **时间范围（必传）**：转换为 `['开始日期', '结束日期']` 格式
- **马力（选传）**:如 `90`
- **排放（选传）**:如 `国六`
- **排量（选传）**:如 `7`

### 第二步：执行 Python 脚本
执行命令：
```bash
python3 /Users/laixufei/PycharmProjects/skills/local-api-chart-generator/build_chart.py --fueltype1 "燃油类型" --time '["开始日期", "结束日期"]'
```

如需带选传参数，可使用：
```bash
python3 /Users/laixufei/PycharmProjects/skills/local-api-chart-generator/build_chart.py --fueltype1 "燃油类型" --time '["开始日期", "结束日期"]' --horsepower "马力" --emission "排放" --displacement "排量"
```

### 第三步：提取并原样返回 HTML（关键！）
**严格约束：**
1. 从 Python 输出中提取 `---HTML_CODE_START---` 和 `---HTML_CODE_END---` 之间的内容。
2. **直接将这段 HTML 源码原封不动地放在回复的最前面**，不要添加任何额外的解释文字。
3. **禁止使用** `[embed]`、`MEDIA:` 或任何其他 OpenClaw 内部渲染语法。
4. **禁止对数据进行额外分析或总结**，只需返回 HTML 源码即可。

## ⚠️ API 调用模式
当通过 `/v1/chat/completions` API 调用时，回复格式必须为：
```
<!DOCTYPE html>
<html lang="zh-CN">
...完整 HTML 源码...
</html>
```

这样调用方可以直接从 `choices[0].message.content` 中获取 HTML 并在前端渲染。