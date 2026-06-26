---
name: ppt-agent
description: 基于 Bento Grid + SVG 的 PPT 生成 Agent。根据用户主题生成大纲、策划稿和可编辑 SVG 三步流程，最终输出可直接拖入 PowerPoint 的矢量页面。触发场景：用户要求生成 PPT、需要制作演示文稿、制作汇报/方案/课程类 PPT 时使用。
---

# ppt-agent

基于文章《应该是目前最强的PPT Agent，附上完整思路分享》的工作流实现的 PPT 生成 skill。

## 核心流程（4步）

```
Step 0 确认风格（style）  ← 新增：生成前必须先确认
Step 1 生成大纲（outline）
Step 2 生成策划稿（planning）
Step 3 生成设计稿 SVG（design）
```

**用户只需要：输入主题 → 确认风格 → 确认大纲 → 确认策划稿 → 下载 SVG → 拖入 PowerPoint**

## Step 0 — 确认风格（必须）

**在开始生成任何内容之前，必须先询问用户以下风格选项：**

1. **主题色**：军事蓝 / 商务蓝 / 危机红 / 能源橙 / 中性灰
2. **主次比例**：以数据为主 / 以叙事为主 / 均衡
3. **内容深度**：要点摘要 / 详细展开 / 专业深度
4. **受众对象**：高管决策层 / 专业分析师 / 公众传播

只有用户明确回复后，才进入 Step 1。不得跳过此步骤直接生成。

## 文件说明

- `prompts/outline.md` — 大纲生成提示词（基于金字塔原理）
- `prompts/planning.md` — 策划搞提示词（白板初稿，无样式）
- `prompts/design.md` — SVG 设计提示词（含 Bento Grid 布局规则）
- `scripts/generate_svg.py` — SVG 输出脚本（可选，用于批量生成）
- `examples/sample_topic.md` — 示例主题

## 使用方式

### Step 1 — 生成大纲

读取 `prompts/outline.md`，将内容作为系统提示词的一部分，结合用户主题，让模型生成 JSON 大纲。

### Step 2 — 生成策划稿

读取 `prompts/planning.md`，基于 Step 1 的大纲生成无样式的白板初稿，让用户确认内容布局是否正确。

### Step 3 — 生成 SVG 设计稿

读取 `prompts/design.md`，基于策划稿和用户提供的内容，生成整页 Bento Grid SVG。

最终 SVG 文件可直接拖入 PowerPoint（2016及以上），完全可编辑。

## Bento Grid 核心原则

1. **灵活性**：卡片数量不固定，1-N 张均可，取决于内容
2. **层级感**：用卡片大小建立视觉层级，最重要的信息放最大卡片
3. **留白**：卡片之间保持至少 20px 间距
4. **6种经典布局**：单一焦点、两栏对称、两栏非对称、三栏、主次结合、英雄式、混合网格

## 输出格式说明

- 最终输出为 **SVG**（非 HTML）
- SVG 画布尺寸：`viewBox="0 0 1280 720"`
- 中文字体使用系统默认字体，确保 PowerPoint 兼容性
- 如需 PPTX，可将 SVG 导入 Figma 或在线工具转换
