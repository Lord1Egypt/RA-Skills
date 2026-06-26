---
name: ppt-generator-pro
description: "生成专业演示文稿，支持 HTML 交互式幻灯片和 PowerPoint (.pptx) 两种格式。当用户需要制作 PPT、演示文稿、Slides、幻灯片、市场分析报告、产品介绍时触发。支持乔布斯风极简科技感设计，自动数据可视化，翻页导航功能。"
---

# PPT Generator Pro

生成专业演示文稿，支持 HTML 和 PPTX 两种输出格式。

## 触发条件

用户提到：PPT、演示文稿、Slides、幻灯片、市场分析、产品介绍、竞品分析、SWOT

## 输出格式

| 格式 | 特点 | 使用场景 |
|------|------|----------|
| **HTML** | 交互式、翻页动画、浏览器直接打开 | 演示、展示、在线分享 |
| **PPTX** | 可编辑、PowerPoint/WPS 打开 | 需要后续修改、正式交付 |

默认同时生成两种格式。

## 生成流程

### Step 1: 收集信息

- 主题/产品名称
- 需要包含的章节（产品定义、应用场景、市场数据、竞品分析等）
- 目标受众
- 风格偏好（默认：深色科技风）

### Step 2: 搜集数据

使用 `web_search` 搜索相关市场数据、行业报告、竞品信息。

### Step 3: 生成 HTML 幻灯片

使用 `scripts/gen_html.py` 生成交互式 HTML 演示。

```bash
python scripts/gen_html.py --title "标题" --output slides.html
```

### Step 4: 生成 PPTX 文件

使用 `scripts/gen_pptx.py` 生成 PowerPoint 文件。

```bash
python scripts/gen_pptx.py --title "标题" --output output.pptx
```

### Step 5: 截图展示

启动本地 HTTP 服务器，用内置浏览器截图展示给用户。

```bash
python -m http.server 8899 --directory <output_dir>
```

## 目录结构

```
ppt-generator-pro/
├── SKILL.md
├── scripts/
│   ├── gen_html.py      # HTML 幻灯片生成器
│   └── gen_pptx.py      # PPTX 生成器
└── templates/
    └── dark-tech.html   # HTML 模板
```

## 设计规范

| 项目 | 规范 |
|------|------|
| 背景色 | #0a0a0a |
| 主色调 | #FF6B35 (橙色) |
| 文字色 | #ffffff |
| 辅助色 | rgba(255,255,255,.7) |
| 卡片背景 | rgba(255,255,255,.04) |
| 圆角 | 18px |

## 注意事项

- 柱状图用 HTML 的 div 实现，不用 Canvas（兼容性好）
- PPTX 使用 python-pptx 库，需预先安装
- HTML 默认带翻页按钮和页码显示
- 章节之间保持视觉一致性
