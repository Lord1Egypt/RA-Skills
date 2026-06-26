# Powerpoint-Generator

> 专业 PPT 演示文稿全流程 AI 生成助手

**[English](README.md)** | 中文

---

**Powerpoint-Generator** 模仿专业 PPT 设计公司的完整工作流（报价万元/页级别），从需求调研到后处理 SVG+PPTX 自动化完成，输出专业级 HTML 演示文稿 + 可编辑矢量 PPTX。

---

## 最近更新

`2026-04-10 · v2.0`

- 新增 8 种主题风格（渐变蓝 / 暖阳夕照 / 北欧极简 / 赛博朋克 / 优雅金 / 深海蓝 / 复古胶片 / 稳重蓝）
- 新增 4 种卡片类型（feature_grid / image_text / data_highlight / stat_block）
- 移除 exec 绕过代码，强化降级策略
- 中英文 SKILL.md 分离

---

## 工作流

```
Step 1 需求调研  →  Step 2 资料搜集  →  Step 3 大纲策划
     ↓
Step 4 内容分配 + 策划稿  →  Step 5 风格 + 配图 + HTML 设计稿
     ↓
Step 6 后处理（HTML → SVG → PPTX）
```

---

## 效果展示

> 以「新一代小米 SU7 发布」为主题的示例输出（小米橙风格）：

| 封面页 | 配置对比页 |
|:---:|:---:|
| ![封面页](ppt-output/png/slide_01_cover.png) | ![配置对比](ppt-output/png/slide_02_models.png) |

| 动力续航页 | 智驾安全页 |
|:---:|:---:|
| ![动力续航](ppt-output/png/slide_03_power.png) | ![智驾安全](ppt-output/png/slide_04_smart.png) |

| 结束页 |
|:---:|
| ![结束页](ppt-output/png/slide_05_end.png) |

---

## 核心亮点

| 特性 | 说明 |
|------|------|
| **6 步专业 Pipeline** | 需求 → 搜索 → 大纲 → 策划 → 设计 → 后处理，模拟专业 PPT 公司完整工作流 |
| **16 种预置风格** | 暗黑科技 / 小米橙 / 蓝白商务 / 朱红宫墙 / 清新自然 / 紫金奢华 / 极简灰白 / 活力彩虹 / 渐变蓝 / 暖阳夕照 / 北欧极简 / 赛博朋克 / 优雅金 / 深海蓝 / 复古胶片 / 稳重蓝 |
| **7 种 Bento 布局** | 单一焦点 / 50/50 对称 / 非对称两栏 / 三栏等宽 / 主次结合 / 顶部英雄式 / 混合网格 |
| **12 种卡片类型** | text / data / list / tag_cloud / process / timeline / comparison / quote / stat_block / feature_grid / image_text / data_highlight |
| **智能配图** | AI 生成 / Unsplash 图库 + 5 种视觉融入技法（渐隐融合 / 色调蒙版 / 氛围底图 / 裁切视窗 / 圆形裁切） |
| **跨页叙事** | 密度交替节奏 / 章节色彩递进 / 封面-结尾呼应 / 渐进揭示 |
| **双 PPTX 导出** | SVG PPTX（文字可编辑）+ PNG PPTX（像素级还原）— HTML → SVG/PNG → PPTX 管线 |

---

## 快速开始

在对话中直接描述你的需求即可触发，Agent 会自动执行完整工作流：

> *"帮我做一个关于 2026 年具身智能发展趋势的 15 页路演 Deck，暗色科技风格"*

所有产物输出至 `ppt-output/`，包含网页预览和双格式 PPTX。

---

## 环境依赖

**必须：**
- **Node.js** >= 18
- **Python** >= 3.8
- **python-pptx / lxml / Pillow**

**一键安装：**
```bash
pip install python-pptx lxml Pillow
npm install puppeteer dom-to-svg
```

**可选（用于配图）：**
配置 `.env` 文件填入 `UNSPLASH_ACCESS_KEY`，或不配置则使用纯文字/数据驱动设计。

---

## 仓库结构

```
Powerpoint-Generator/
├── SKILL.md              # 主工作流指令（Agent 入口，英文）
├── skill_cn.md          # 主工作流指令（中文）
├── README.md             # 英文文档
├── README_CN.md          # 中文文档
├── .env.example          # 环境变量模板
├── references/
│   ├── prompts.md        # 5 套 Prompt 模板
│   ├── style-system.md   # 16 种风格 + CSS 变量
│   ├── bento-grid.md     # 7 种布局 + 12 种卡片
│   ├── method.md         # 核心方法论
│   └── pipeline-compat.md # 管线兼容性规则
└── scripts/
    ├── html_packager.py      # HTML 合并预览
    ├── html2svg.py          # HTML → SVG
    ├── html2png.py          # HTML → PNG（Puppeteer 截图）
    ├── svg2pptx.py          # SVG → PPTX（文字可编辑）
    ├── png2pptx.py          # PNG → PPTX（像素级还原）
    ├── contract_validator.py   # 合同校验
    ├── planning_validator.py   # Planning JSON 校验
    ├── milestone_check.py      # 里程碑验收
    ├── prompt_harness.py       # 动态 Prompt 生成
    ├── resource_loader.py      # 资源路由
    ├── visual_qa.py           # 视觉 QA（截图+审计）
    └── subagent_logger.py      # Subagent 运行时日志
```

---

## 使用示例

| 场景 | 说法 |
|------|------|
| 纯主题 | "帮我做个 PPT" / "做一个关于 X 的演示" |
| 带素材 | "把这篇文档做成 PPT" / "用这份报告做 slides" |
| 带要求 | "做 15 页暗黑风的 AI 安全汇报材料" |
| 隐式触发 | "我要给老板汇报 Y" / "做个培训课件" / "做路演 deck" |

---

## 特别鸣谢

本项目基于 [ppt-agent-skill](https://github.com/Akxan/ppt-agent-skill) 创作，感谢原项目作者的出色工作和开源精神。

## License

[MIT](LICENSE)
