---
name: excalidraw-diagram
description: "Generate Excalidraw hand-drawn diagrams from natural language. Use when asked to create diagrams, flowcharts, mind maps, architecture diagrams, ER diagrams, or sequence diagrams. Outputs .excalidraw JSON files. Triggers: draw diagram, create flowchart, visualize, architecture diagram, excalidraw."
license: MIT
metadata:
  author: WanSan Team (OpenClaw)
  version: 1.0.0
  created: 2026-04-03
---

# excalidraw-diagram

<!-- L1 元数据 -->
<!--
description: Generate Excalidraw hand-drawn diagrams from natural language. Use when asked to create diagrams, flowcharts, mind maps, architecture diagrams, ER diagrams, or sequence diagrams. Outputs .excalidraw JSON files. Triggers: draw diagram, create flowchart, visualize, architecture diagram, excalidraw.
-->

## 能力概述

将自然语言描述转为 Excalidraw 可视化图表（.excalidraw 文件），保存到当前工作目录或用户指定路径。

**支持图表类型：** 流程图 · 架构图 · 思维导图 · 关系图 · ER图 · 时序图 · 泳道图 · 类图 · 数据流图

---

## 执行步骤

### Step 1 — 理解需求
- 识别图表类型（如未明确，根据内容自动判断）
- 提取节点、关系、层次结构
- 确认文件名（用户未指定时用 `diagram-{YYYYMMDD-HHmm}.excalidraw`）
- 确认保存路径（用户未指定时保存到当前工作目录）

### Step 2 — 规划布局
参考 `references/diagram-templates.md` 对应模板，按以下规则布局：
- **水平间距：** 200–300px
- **垂直间距：** 100–150px
- **起点坐标：** x=100, y=100
- 流程图：从上到下或从左到右
- 思维导图：中心节点向四周辐射
- 时序图/泳道图：横向分列

### Step 3 — 生成 JSON
严格按照 [元素规范](references/element-spec.md) 构建 elements 数组，生成标准 .excalidraw 文件结构：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "openclaw-skill",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

### Step 3.5 — 文字元素叠加（关键！）

每个带文字的形状（rectangle/ellipse/diamond）除了形状自身的 text 属性外，
必须同时生成一个独立的 text 元素叠加在形状上方。

原因：Excalidraw 在 headless 浏览器导出 PNG 时，形状内嵌文字不渲染，
但独立 text 元素可以正常显示。双重文字确保在线编辑和导出都能看到文字。

text 元素坐标计算：
- x = 形状.x + 10
- y = 形状.y + (形状.height - 行数 × 22) / 2
- width = 形状.width - 20
- textAlign: "center"
- containerId: null（不绑定到容器）

示例：
```json
// 形状元素
{
  "id": "rect001",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 160, "height": 60,
  "label": { "text": "用户登录" }
}
// 叠加的独立 text 元素（必须同时生成）
{
  "id": "txt001",
  "type": "text",
  "x": 110,
  "y": 119,
  "width": 140,
  "text": "用户登录",
  "fontSize": 16,
  "fontFamily": 5,
  "textAlign": "center",
  "containerId": null
}
```

### Step 4 — 保存文件
```bash
# 写入文件（使用 write 工具）
# 路径：<用户指定目录或当前工作目录>/<filename>.excalidraw
```

### Step 4.5 — 导出 PNG（默认执行）

生成 .excalidraw 文件后，自动导出 PNG：

```bash
python3 ~/.openclaw/workspace/skills/excalidraw-diagram/scripts/export-png.py <input.excalidraw> <output.png>
```

- 依赖：`playwright`（`pip install playwright && playwright install chromium`）
- 需要联网（首次加载 CDN 资源约 15-30s）
- 输出 PNG 通常 > 50 KB，分辨率 1400×900

如果导出失败，告知用户手动在 excalidraw.com 打开文件导出。

### Step 5 — 回报结果
告知用户：
- 文件保存路径
- 图表包含的元素数量
- 如何在 Excalidraw 中打开（excalidraw.com 或桌面版）
- 如需导出 PNG，参考 [references/headless-export.md](references/headless-export.md)

---

## 元素快速参考

### 颜色方案（强制使用）
| 用途 | 颜色代码 |
|------|---------|
| 主要节点 Primary | `#a5d8ff` |
| 次要节点 Secondary | `#b2f2bb` |
| 重要/高亮 Important | `#ffd43b` |
| 警告/错误 Alert | `#ffc9c9` |
| 背景透明 | `"transparent"` |

### 字体规范（强制）
- `fontFamily: 5`（Excalifont，Excalidraw 官方手绘字体）
- 正文字号：`fontSize: 16`
- 标题字号：`fontSize: 20`
- 大标题：`fontSize: 24`

### 元素类型
| 形状 | type | 典型用途 |
|------|------|---------|
| 矩形 | `rectangle` | 流程步骤、模块、类 |
| 椭圆 | `ellipse` | 开始/结束节点、实体 |
| 菱形 | `diamond` | 判断条件、决策 |
| 箭头 | `arrow` | 连接、流向、关系 |
| 文本 | `text` | 标签、说明 |

详细属性见 [元素规范](references/element-spec.md)。

---

## 各图表类型要点

| 图表类型 | 主要形状 | 元素数量建议 | 方向 |
|---------|---------|------------|------|
| 流程图 | rectangle + diamond + arrow | 3–10 步 | 上→下 |
| 架构图 | rectangle + arrow | 5–15 节点 | 分层 |
| 思维导图 | ellipse + rectangle + arrow | 中心+4–6 分支 | 辐射 |
| 关系图 | ellipse/rectangle + arrow | 3–8 实体 | 自由 |
| ER 图 | rectangle + text + arrow | 3–8 表 | 网格 |
| 时序图 | rectangle + text + arrow | 3–6 参与者 | 左→右+时间轴 |
| 泳道图 | rectangle(lane) + arrow | 2–4 泳道 | 左→右 |
| 类图 | rectangle + text + arrow | 3–8 类 | 层次 |
| 数据流图 | ellipse + rectangle + arrow | 5–12 节点 | 自由 |

---

## ID 生成规则

每个元素需要唯一 ID，使用随机字符串（8位字母数字）：
```
"id": "abc12345"
```
箭头的 `startBinding.elementId` 和 `endBinding.elementId` 必须指向对应元素的 id。

---

## 常见错误预防

1. **箭头未绑定**：arrow 元素必须设置 `startBinding` 和 `endBinding`，否则连线会断开
2. **坐标重叠**：确保相邻元素之间有足够间距（最小 20px padding）
3. **文字溢出**：元素宽度 = 文字字符数 × 10 + 40（最小 120px）
4. **缺少 points**：arrow 类型必须包含 `points: [[0,0],[dx,dy]]`
5. **文字不显示（导出时）**：必须按 Step 3.5 为每个形状叠加独立 text 元素

---

## 示例参考

见 [references/examples.md](references/examples.md) — 包含各类图表的完整 prompt + 输出示例。
