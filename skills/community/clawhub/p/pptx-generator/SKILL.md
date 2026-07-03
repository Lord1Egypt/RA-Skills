---
name: pptx-generator
description: 专业 PPT 生成器。11 种幻灯片类型、5 套配色、图表/表格/时间线/图片支持。JSON 驱动，生成标准可编辑 PPTX。PPT、幻灯片、演示文稿、PowerPoint。
version: 2.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install python-pptx"
---

# PPT Generator

专业 PPT 生成器。通过 JSON 描述生成标准、可编辑的 PowerPoint 演示文稿。

## 用法

```bash
python3 scripts/generate_pptx.py slides.json --out output.pptx
```

## JSON 结构

```json
{
  "style": "business_blue",
  "footer": "机密",
  "page_numbers": true,
  "output": "report.pptx",
  "slides": [
    {"type": "cover", "title": "标题", "subtitle": "副标题", "variant": "centered"},
    {"type": "section", "title": "第一部分"},
    {"type": "agenda", "title": "目录", "topics": ["主题1", "主题2"], "highlight": 0},
    {"type": "content", "title": "内容页", "items": ["要点1", "要点2"], "columns": 1},
    {"type": "two_column", "title": "双栏", "left": ["左栏"], "right": ["右栏"]},
    {"type": "table", "title": "表格", "headers": ["A","B"], "rows": [[1,2]]},
    {"type": "chart", "title": "图表", "chart_type": "bar|line|pie",
     "categories": ["Q1","Q2"], "series": [{"name":"S1","values":[10,20]}]},
    {"type": "timeline", "title": "时间线",
     "milestones": [{"label":"阶段1","desc":"描述"}]},
    {"type": "quote", "title": "", "quote": "内容", "attribution": "作者"},
    {"type": "image", "title": "图片", "image_path": "img.png", "overlay": false},
    {"type": "summary", "title": "总结", "points": ["要点"], "conclusion": "结论"},
    {"type": "contact", "title": "联系我们", "info": "邮箱/电话"}
  ]
}
```

## 幻灯片类型（11 种）

| 类型 | 功能 |
|------|------|
| cover | 封面，3 种变体：centered / left / split |
| section | 过渡页/章节分隔 |
| agenda | 目录页，支持高亮当前章节 |
| content | 内容页，支持单栏/双栏、多级列表 |
| two_column | 双栏对比 |
| table | 表格（隔行变色） |
| chart | 图表（柱状/折线/饼图） |
| timeline | 时间线/里程碑 |
| quote | 引用/强调 |
| image | 图片页，支持普通/全屏叠加两种模式 |
| summary | 总结页，底部结论框 |
| contact | 结尾/联系信息页 |

## 配色方案（5 套）

| 风格 | 适用场景 |
|------|----------|
| business_blue | 商业汇报，专业稳重 |
| academic_white | 学术论文，简洁规范 |
| creative_purple | 创意展示，时尚活力 |
| tech_dark | 技术分享，现代高端 |
| minimal_gray | 通用场景，简约百搭 |

## 能力变更（v2.0.0）

- **修复**: 副标题与标题共用 textbox 导致重叠
- **修复**: `layout` 参数声明但未使用
- **修复**: 图片幻灯片不检查文件是否存在
- **修复**: 标题栏硬编码 10 英寸宽度
- **新增**: 11 种幻灯片类型（原 7 种 → 11 种）
- **新增**: 分页目录页（agenda）
- **新增**: 封面 3 种变体（居中/居左/分割）
- **新增**: 图表支持（柱状图/折线图/饼图）
- **新增**: 时间线/里程碑
- **新增**: 引用/强调页
- **新增**: 结尾/联系信息页
- **新增**: 自动页码 + 页脚
- **新增**: 渐变色背景
- **新增**: 多级列表支持
- **新增**: 10 色完整调色板（原 5 色 → 10 色角色）
- **新增**: JSON 驱动生成管线
- **新增**: 错误跳过 + 逐页报告
