---
name: market-research
version: 1.0.0
description: 亚马逊市场调研报告。用户给出类目名称和节点 ID，自动生成完整 HTML 报告（市场概览、价格、REVIEW、品牌、卖家、竞品 8 个维度）。触发词：市场调研、市调、market research、分析这个类目。
---

# 亚马逊市场调研报告

用户给出类目名称 + 节点 ID，一条命令生成完整报告。

## 触发方式

用户说出类目名和节点 ID 即可，例如：
- "Deck Boxes, 671804011"
- "帮我调研 Salon Chairs 15144890011"
- "市调一下 671804011"

## 执行

```
exec(
  command='bash {baseDir}/scripts/market-research.sh "类目名称" 节点ID',
  background=true,
  timeout=600
)
```

等 process poll 完成后，用 `open` 打开输出的报告文件。

## 输出

- 文件：`output/{类目名}-market-report.html`
- 内容：8 个分析维度（市场概览、上架时间、价格、REVIEW、品牌、卖家、竞品Top10、总体评价）
- 格式：带左侧导航的单页 HTML，含表格和图表
- 耗时：约 3-5 分钟

## 前置条件

- 环境变量 `LINKFOXAGENT_API_KEY` 已设置
- Python 3 可用
- 网络可访问 LinkFox Agent API
