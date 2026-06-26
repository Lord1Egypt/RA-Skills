---
name: info-visualize
version: 1.0.0
license: MIT
description: |
  信息可视化技能，将结构化数据渲染为深色主题的高质量图表和长图报告。
  支持两类输出：第一类是零依赖 SVG/HTML 交互式横向条形图，直接在浏览器打开；
  第二类是基于 Pillow 的 PNG 长图报告，含标题区、KPI 卡片、文字段落、表格、
  条形图、卡片组、时间线、页脚等模块，适合监控报告、日报、排行榜等场景。
  触发词：生成图表、做可视化、画条形图、生成长图、渲染报告、
  排行榜图、PNG报告、信息图、数据卡片、深色主题图表、
  make chart、visualize data、render report、bar chart、longform image
---

# info-visualize

将数据渲染为专业深色主题图表和长图报告的通用技能。

## 核心脚本

两个脚本均位于 `scripts/` 目录，按需选择：

| 脚本 | 输出格式 | 适用场景 | 依赖 |
|------|---------|---------|------|
| `svg_bar_chart.py` | SVG + HTML | 排行榜、对比图、任意条形图 | 无（纯标准库） |
| `png_longform.py` | PNG 长图 | 日报/周报、监控报告、综合信息图 | `pip install Pillow` |

## 工作流

### 1. SVG 横向条形图

**数据准备** — 将数据整理为标准 JSON：

```json
{
  "title": "A股涨幅 TOP 20",
  "subtitle": "2026-03-14  |  全市场 5481 只股票",
  "footer": "数据来源: Tushare Pro",
  "value_suffix": "%",
  "kpis": [
    {"label": "榜首涨幅", "value": "+20.01%"},
    {"label": "涨停个股", "value": "18"},
    {"label": "合计成交额", "value": "342.5 亿"}
  ],
  "items": [
    {"label": "中红医疗", "value": 20.01, "tag": "医疗保健", "extra": "300981.SZ"},
    {"label": "通裕重工", "value": 19.94, "tag": "工程机械", "extra": "300185.SZ"}
  ]
}
```

**调用方式**（命令行）：
```bash
python scripts/svg_bar_chart.py --input data.json --output chart.html --value-suffix %
```

**调用方式**（Python 导入）：
```python
from scripts.svg_bar_chart import build_svg_chart
items = [{"label": "标签", "value": 数字, "tag": "分类"}, ...]
config = {"title": "...", "subtitle": "...", "kpis": [...], "value_suffix": "%"}
svg_str, html_str = build_svg_chart(items, config)
with open("chart.html", "w", encoding="utf-8") as f:
    f.write(html_str)
```

**关键配置项**：
- `show_reference_line`: 在指定值处绘制垂直参考线（如涨停线10%）
- `reference_label`: 参考线标签
- `max_value_override`: 手动指定 X 轴最大值
- `bar_threshold_colors`: 按阈值分色，格式 `[(20, "#FF2244"), (10, "#FFAA00")]`

### 2. PNG 长图报告

**数据结构**：
```json
{
  "title": "报告标题",
  "subtitle": "2026-03-14 20:00 更新",
  "status_tag": {"text": "CRITICAL", "level": "critical"},
  "kpis": [
    {"label": "布伦特原油", "value": "$103/桶"},
    {"label": "风险等级", "value": "CRITICAL"},
    {"label": "海峡通行", "value": "2艘/日"}
  ],
  "sections": [
    {
      "type": "text",
      "title": "态势综述",
      "content": "当前局势摘要...\n第二段..."
    },
    {
      "type": "table",
      "title": "关键指标",
      "headers": ["指标", "当前值", "变化"],
      "rows": [["布伦特", "$103", "+21%"]]
    },
    {
      "type": "bar",
      "title": "各国影响",
      "value_suffix": "%",
      "items": [{"label": "中国", "value": 35}, {"label": "日本", "value": 25}]
    },
    {
      "type": "cards",
      "title": "风险要素",
      "items": [
        {"title": "封锁风险", "content": "说明文字", "level": "critical"},
        {"title": "储备缓冲", "content": "说明文字", "level": "warning"}
      ]
    },
    {
      "type": "timeline",
      "title": "近期事件",
      "events": [
        {"date": "2026-02-28", "text": "美以联合空袭伊朗"},
        {"date": "2026-03-01", "text": "海峡通行量骤降97%"}
      ]
    }
  ],
  "footer": "数据来源: Jane's / EIA / 新浪财经",
  "next_update": "下次更新: 明日 20:00"
}
```

**调用方式**（命令行）：
```bash
python scripts/png_longform.py --input report.json --output report.png
# 同时归档到指定目录：
python scripts/png_longform.py --input report.json --output report.png --archive "C:/Users/user/.ai-memory/news"
```

**调用方式**（Python 导入）：
```python
from scripts.png_longform import render_from_json, LongformRenderer
import json

with open("report.json") as f:
    data = json.load(f)
render_from_json(data, "report.png")
```

**section type 参考**：
- `text`：纯文字段落，支持 `\n` 换行
- `table`：表格，需 `headers`（列名列表）+ `rows`（二维列表）
- `bar`：横向条形图，需 `items`（`[{label, value, color?}]`）
- `cards`：双列卡片组，`level` 可选 `normal/warning/critical/info`
- `timeline`：时间线，需 `events`（`[{date, text}]`）

## 设计规范（深色主题）

所有输出遵循统一视觉规范，与用户已有报告风格完全一致：

- **画布宽度**：900px
- **背景色**：深海军蓝 `#0E1624`
- **强调色**：青绿 `#2EC4B6`（标题、圆点、边框）
- **数字色**：金黄 `#FFC83C`（KPI 大数字）
- **状态色**：红 `#E65050`（critical）/ 橙 `#FF8C28`（warning）/ 绿 `#3CC878`（normal）
- **字体**：微软雅黑 `msyhbd.ttc`（标题）+ `msyh.ttc`（正文）
- **顶部**：3px 青绿色分割线 + 深色 Header
- **底部**：报告时间 + WorkBuddy 水印

## 输出路径惯例

- 当前项目目录：`./chart.html` / `./report.png`
- 若用户有归档需求（如自动化任务）：额外复制到 `C:\Users\ToddC\.ai-memory\news\`

## 常见问题

**Q: SVG 在浏览器里空白？**  
A: 确保 HTML 中 SVG 已直接内嵌（inline SVG），不要使用 `<img src="chart.svg">`，后者在某些浏览器会有 CORS 限制。`svg_bar_chart.py` 默认输出 inline HTML，直接双击打开即可。

**Q: PNG 中文乱码？**  
A: 脚本自动按优先顺序搜索 `msyhbd.ttc → msyh.ttc → simhei.ttf → simsun.ttc`，Windows 系统通常自带。若仍乱码，确认 `C:\Windows\Fonts\msyh.ttc` 存在。

**Q: 如何调整条形图颜色？**  
A: 在 `items` 中为每项添加 `"color": "#FF5533"`；或在 config 中设置 `bar_threshold_colors`。
