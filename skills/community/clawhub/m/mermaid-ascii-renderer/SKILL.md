---
name: mermaid-ascii-renderer
description: >-
  使用 beautiful-mermaid 项目将 Mermaid 图表渲染为 ASCII 艺术。提供解析、布局算法和渲染操作的完整实现指南，支持流程图、状态图、序列图、类图和 ER 图表。当用户请求涉及以下场景时使用：（1）beautiful-mermaid 的 ASCII 渲染系统实现；（2）在终端/控制台输出 Mermaid 图表；（3）理解 A* 路径查找、网格布局、边路由等算法；（4）添加新的图表类型支持；（5）调试 ASCII 渲染问题（节点重叠、边穿过、标签位置）；（6）修改渲染逻辑或布局策略。
metadata:
  author: joe
  version: "1.1.0"
  title: mermaid-ascii-renderer
  description_zh: >-
    使用 beautiful-mermaid 项目将 Mermaid 图表渲染为 ASCII 艺术。提供解析、布局算法和渲染操作的完整实现指南，支持流程图、状态图、序列图、类图和 ER 图表。当 Claude 需要理解beautiful-mermaid 的 ASCII 渲染系统或在项目中使用 ASCII 渲染功能时使用。
---

# Mermaid ASCII 渲染器技能

用于在 beautiful-mermaid 项目中理解或使用 ASCII/Unicode 渲染（流程图、状态图、序列图、类图、ER 图）。

## 范围与限制

### 支持的图表类型

| 图表类型 | 支持状态 | 说明 |
|---------|---------|------|
| **Flowchart** (流程图) | ✅ 完全支持 | graph TD/LR/BT/RL, 子图, 多种节点形状 |
| **State Diagram** (状态图) | ✅ 完全支持 | stateDiagram-v2, [*] 起始/结束状态 |
| **Sequence Diagram** (序列图) | ✅ 完全支持 | 参与者、消息、循环/条件块、注释 |
| **Class Diagram** (类图) | ✅ 完全支持 | 类定义、属性、方法、继承/组合/关联关系 |
| **ER Diagram** (实体关系图) | ✅ 完全支持 | 实体、属性、Crow's Foot 关系标记 |

### 不支持的图表类型

- Gantt (甘特图)
- Pie Chart (饼图)
- Mindmap (思维导图)
- Timeline (时间线)
- User Journey (用户旅程图)
- Git Graph (Git 图表)
- C4Context/C4Container (C4 模型)

### 版本兼容性

- **基于版本**: beautiful-mermaid v0.1.x
- **Node.js**: >= 18.0.0
- **Bun**: >= 1.0.0
- **TypeScript**: >= 5.0.0

### 输出限制与边界条件

| 场景 | ASCII 模式 | Unicode 模式 |
|------|-----------|-------------|
| **长标签** (>20字符) | 自动扩展节点宽度，可能影响布局 | 同左 |
| **密集图** (>20节点) | 渲染时间增加，建议增大 padding | 同左 |
| **复杂路由** | 可能产生锐角，可调整 heuristic | 同左 |
| **终端兼容性** | 最佳兼容性，所有终端支持 | 需 UTF-8 支持终端 |
| **子图嵌套** | 支持一层子图，多层嵌套可能重叠 | 同左 |

> 说明：上述阈值为经验建议，实际表现受终端字体、CJK 字符宽度、图表结构影响。问题定位请参考 `references/troubleshooting.md`。

## 快速开始

### 安装

```bash
npm install beautiful-mermaid
# 或
bun add beautiful-mermaid
# 或
pnpm add beautiful-mermaid
```

### 基本使用

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'

const ascii = renderMermaidAscii(`graph LR\n  A --> B --> C`)
console.log(ascii)
```

**输出:**
```
┌───┐     ┌───┐     ┌───┐
│   │     │   │     │   │
│ A │────►│ B │────►│ C │
│   │     │   │     │   │
└───┘     └───┘     └───┘
```

### 常见使用方式

不同环境（Node/Bun/浏览器）、同步/异步差异与 SVG/ASCII 选择建议请参考：`references/usage.md`。

## 核心 API

### renderMermaidAscii

```typescript
function renderMermaidAscii(
  diagram: string,
  options?: AsciiRenderOptions
): string
```

将 Mermaid 图表渲染为 ASCII/Unicode 字符串（同步执行）。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `diagram` | `string` | ✅ | Mermaid 图表语法字符串 |
| `options` | `AsciiRenderOptions` | ❌ | 渲染选项配置 |

**AsciiRenderOptions 说明与使用示例**请参考：`references/usage.md`。

SVG/ASCII 选择建议、主题系统说明与多图类型示例分别见：`references/usage.md`、`references/theming.md`、`references/examples.md`。

## 项目结构参考

**beautiful-mermaid 源码结构** (简化版):
```
src/
  ascii/              # ASCII 渲染引擎
    index.ts          # ASCII 渲染 API 入口
    types.ts          # 类型定义
    canvas.ts         # 画布操作
    draw.ts          # 绘图原语
    grid.ts          # 网格布局
    pathfinder.ts    # A* 路径查找
    edge-routing.ts   # 边路由
    sequence.ts      # 序列图实现
    class-diagram.ts # 类图实现
    er-diagram.ts   # ER 图实现
    converter.ts     # 转换器
  index.ts           # 主 API 入口 (导出 renderMermaid, renderMermaidAscii)
  renderer.ts       # SVG 渲染
  parser.ts         # Mermaid 语法解析
  layout.ts         # 布局引擎
  theme.ts          # 主题系统
```

**完整细节请参考**: `references/core-systems.md`（低层系统）、`references/diagrams.md`（图表实现）

## 何时阅读参考文档

- 使用方式、API 选项、SVG/ASCII 选择：`references/usage.md`
- 多图类型最小示例与输出：`references/examples.md`
- 主题系统与配色策略（SVG）：`references/theming.md`
- 图表实现细节与布局算法：`references/diagrams.md`
- 低层渲染系统（类型/画布/绘图/路由）：`references/core-systems.md`
- Unicode/ASCII 字符表：`references/characters.md`
- 故障排查与性能建议：`references/troubleshooting.md`
- 外部链接与资料：`references/resources.md`
