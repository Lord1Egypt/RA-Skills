---
name: mermaid-renderer
description: 渲染 Mermaid 图表。当用户需要可视化展示流程图、时序图、类图、饼图、Git分支图等图表时使用。支持两种输出模式：1) 终端 ASCII 文本输出（默认）；2) 图片文件导出（指定 --image/--png 参数）。触发场景包括"画个流程图"、"生成时序图"、"渲染Mermaid图表"、"导出图表为图片"等。
---

# Mermaid 图表渲染器

将 Mermaid 语法图表渲染为终端 ASCII 文本或图片文件。

## 使用方式

### 基本用法

```
渲染以下 Mermaid 图表：
<mermaid代码>

[可选：导出为图片]
```

### 输出模式

| 模式 | 触发条件 | 输出 |
|------|----------|------|
| 终端 ASCII | 默认 | 直接显示在终端 |
| 图片导出 | 用户要求"图片"、"PNG"、"导出"、"保存为文件" | 生成 PNG 文件并上传 BOS |

## 执行流程

1. **解析用户输入**：提取 Mermaid 图表代码
2. **判断输出模式**：根据用户意图选择终端或图片
3. **终端模式**：使用 `python3.11 -m termaid` 渲染 ASCII
4. **图片模式**：调用 `scripts/render.py` 生成 PNG 并上传

## 支持的图表类型

- **流程图** (graph/flowchart)
- **时序图** (sequenceDiagram)
- **类图** (classDiagram)
- **饼图** (pie)
- **Git分支图** (gitGraph)
- **状态图** (stateDiagram)
- **ER图** (erDiagram)

详细语法参考见 `references/chart-types.md`。

## 示例

### 终端输出示例

```
渲染时序图：
sequenceDiagram
    participant 用户
    participant dodo
    用户->>dodo: 发送请求
    dodo-->>用户: 返回结果
```

### 图片导出示例

```
把下面的流程图导出为图片：
graph LR
    A[开始] --> B{判断}
    B -->|是| C[执行A]
    B -->|否| D[执行B]
```

## 技术依赖

- **termaid**：Python 包，用于终端 ASCII 渲染（需 Python 3.11+）
- **matplotlib**：Python 库，用于图片生成
