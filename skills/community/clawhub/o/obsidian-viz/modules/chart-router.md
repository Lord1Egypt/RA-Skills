# 图表工具选择模块 (Chart Router)

本模块负责根据内容类型选择最合适的可视化工具，并管理降级策略。

## 工具能力定位

### Mermaid
- **擅长**：语义图表（流程/序列/类图/ER/状态图/甘特图）
- **输出**：`.mmd` 文本文件，可版本控制
- **优势**：语法简洁、GitHub 原生支持、适合技术文档
- **限制**：布局自动化，自由度较低

### Excalidraw
- **擅长**：自由绘图（架构/拓扑/白板/手绘风格）
- **输出**：`.excalidraw` JSON 文件，可手动编辑
- **优势**：手绘风格、自由布局、视觉吸引力强
- **限制**：坐标计算复杂，需精确布局

### Canvas
- **擅长**：动态渲染（数据图表/仪表板/大型知识网络）
- **输出**：`.canvas` / `.html` / `.png`
- **优势**：交互式探索、支持大规模节点、动态渲染
- **限制**：Obsidian 特定格式，通用性较低

## 工具选择决策表

### 基于用户意图的路由

| 用户意图 | 选择工具 | 理由 |
|---------|---------|------|
| 手绘 / 草图 / 自由风格 / 概念图 | Excalidraw | 手绘风格最自然 |
| 技术文档 / GitHub 展示 / 演示文稿 | Mermaid | 文本格式易维护 |
| 大型知识网络 / 交互式探索 | Canvas | 支持大规模节点 |
| 动画演示 | Excalidraw | 支持动画模式 |
| 模糊请求（概念性话题） | Excalidraw | 默认手绘风格 |
| 模糊请求（技术性话题） | Mermaid | 默认技术图表 |

### 基于图表类型的路由

| 图表类型 | 优先工具 | 一级备选 | 二级备选 | 选择理由 |
|---------|---------|---------|---------|---------|
| 流程图（含判断分支） | Mermaid | Excalidraw | Canvas | mermaid flowchart 语法天然支持分支逻辑 |
| 思维导图 | Mermaid | Canvas | Excalidraw | mermaid mindmap 语法直接支持 |
| ER 图 / UML 类图 | Mermaid | Excalidraw | — | mermaid erDiagram / classDiagram 语义精准 |
| 时序图 / 甘特图 | Mermaid | Canvas | — | mermaid 原生支持 sequenceDiagram / gantt |
| 系统架构图 | Excalidraw | Canvas | Mermaid | 架构图需自由布局、云图标、分组框 |
| 网络拓扑图 | Excalidraw | Canvas | — | 节点自由摆放，连线样式丰富 |
| 数据可视化（柱/折/饼/散点） | Canvas | Mermaid | — | Canvas 可渲染动态、可交互的数据图表 |
| 仪表板 / 多图组合 | Canvas | Excalidraw | — | Canvas 支持多图层组合与动态渲染 |
| 复合/混合图 | Excalidraw | Canvas | — | 自由度最高，适合不规则布局 |
| 组织架构 / 系统分层 | Excalidraw | Mermaid | — | 层级清晰，手绘风格更友好 |
| 项目时间线 | Excalidraw | Mermaid | — | 时间轴可视化，Excalidraw 更灵活 |
| A vs B 对比 | Excalidraw | — | — | ���比图需自由布局 |
| 优先级矩阵 | Excalidraw | — | — | 矩阵布局需精确控制 |

## 降级策略

### 降级触发条件

1. **工具调用失败**：API 错误、超时、格式错误
2. **内容不适配**：节点数量超限、结构过于复杂
3. **用户明确要求**：指定使用某个工具

### 降级流程

```
优先工具失败
    ↓
自动切换一级备选
    ↓
一级备选失败
    ↓
自动切换二级备选
    ↓
全部失败
    ↓
输出纯文字结构摘要
    ↓
在输出中注明降级原因
```

### 降级输出示例

```markdown
## 图表生成结果

⚠️ **降级通知**：优先工具 Mermaid 生成失败（原因：节点数量超过 50 个），已自动切换到 Canvas。

**生成文件**：`output/system-architecture.canvas`

（Canvas 图表内容）
```

## 输出格式选择

### Obsidian 模式（默认）

**触发条件**：
- 用户未明确要求标准格式
- 用户提到 "Obsidian"、"在 Obsidian 打开"

**输出格式**：
- Mermaid → `.md` 文件（包含 mermaid 代码块）
- Excalidraw → `.md` 文件（包含 Excalidraw JSON + YAML frontmatter）
- Canvas → `.canvas` 文件

### 标准模式

**触发条件**：
- 用户明确要求 "标准格式"、"通用格式"
- 用户提到 "excalidraw.com"、"GitHub"、"导出"

**输出格式**：
- Mermaid → `.mmd` 文件
- Excalidraw → `.excalidraw` 文件
- Canvas → `.html` 文件（交互式）或 `.png` 文件（静态）

## 工具调用接口

### 调用 Mermaid

**传入参数**：
```json
{
  "chart_type": "flowchart | sequenceDiagram | stateDiagram-v2 | classDiagram | erDiagram | mindmap | gantt | timeline",
  "nodes": [
    {"id": "n1", "label": "节点1", "type": "rectangle | diamond | circle | ..."},
    {"id": "n2", "label": "节点2", "type": "..."}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "label": "连线标签", "style": "solid | dashed | thick"}
  ],
  "layout": "TB | LR | RL | BT",
  "output_format": "obsidian | standard"
}
```

**输出**：
- Obsidian 模式：`.md` 文件（包含 mermaid 代码块）
- 标准模式：`.mmd` 文件

### 调用 Excalidraw

**传入参数**：
```json
{
  "chart_type": "flowchart | hierarchy | timeline | comparison | matrix | relationship | free-layout | architecture | mindmap",
  "elements": [
    {"type": "rectangle | ellipse | diamond | arrow", "text": "...", "x": 0, "y": 0, "width": 200, "height": 80, "color": "..."}
  ],
  "layout_hint": "horizontal | vertical | radial | free",
  "output_format": "obsidian | standard | animation"
}
```

**输出**：
- Obsidian 模式：`.md` 文件（包含 Excalidraw JSON + YAML frontmatter）
- 标准模式：`.excalidraw` 文件
- 动画模式：`.excalidraw` 文件（元素按顺序排列）

### 调用 Canvas

**传入参数**：
```json
{
  "chart_type": "mindmap | flowchart | hierarchy | free-layout | data-visualization",
  "nodes": [
    {"id": "n1", "type": "text | file | link | group", "text": "...", "x": 0, "y": 0, "width": 250, "height": 100, "color": "1"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "n1", "toNode": "n2", "fromSide": "right", "toSide": "left", "label": "..."}
  ],
  "layout": "radial | hierarchical | pipeline | cluster",
  "output_format": "obsidian | html | png"
}
```

**输出**：
- Obsidian 模式：`.canvas` 文件
- HTML 模式：`.html` 文件（交互式）
- PNG 模式：`.png` 文件（静态预览）

## 节点数量限制

| 工具 | 推荐上限 | 硬性上限 | 超限处理 |
|------|---------|---------|---------|
| Mermaid | 30 | 50 | 降级到 Canvas 或提示用户拆分 |
| Excalidraw | 40 | 60 | 降级到 Canvas 或提示用户拆分 |
| Canvas | 100 | 200 | 提示用户拆分为多个 Canvas |

**超限警告示例**：

```markdown
⚠️ **节点数量警告**：检测到 65 个节点，超过 Mermaid 推荐上限（30 个）。
建议：
1. 拆分为多个子图
2. 使用 Canvas 工具（支持更大规模）
3. 简化图表，仅保留关键路径

是否继续使用 Mermaid 生成？（可能导致布局混乱）
```

## 特殊场景处理

### 动画模式

**触发条件**：用户提到 "动画"、"演示"、"逐步展示"

**处理方式**：
1. 强制使用 Excalidraw
2. 输出标准格式 `.excalidraw` 文件
3. 元素按出现顺序排列（标题 → 背景 → 节点 → 箭头）
4. 提示用户使用 excalidraw-animate 工具播放

### 多图组合

**触发条件**：用户提到 "仪表板"、"多图"、"组合"

**处理方式**：
1. 优先使用 Canvas
2. 将每个子图作为独立节点
3. 使用分组节点组织布局
4. 输出 `.canvas` 文件

### 中文内容

**处理规则**：
- 所有工具均原生支持中文，无需转义
- Mermaid：标签含中文或特殊字符时，用双引号包裹
- Excalidraw：fontFamily 固定为 5（Excalifont），autoResize 必须为 true
- Canvas：text 字段直接写入中文，换行使用 `\n`

## 错误处理

### 常见错误与修复

| 错误类型 | 可能原因 | 修复方法 |
|---------|---------|---------|
| Mermaid 语法错误 | 中文标签未加引号 | 自动添加双引号 |
| Excalidraw 坐标错误 | 箭头 points 计算错误 | 重新计算相对坐标 |
| Canvas JSON 错误 | 尾随逗号 | 自动清理 JSON |
| 文件无法打开 | 格式不符合规范 | 重新生成，严格遵循 reference |

### 错误输出示例

```markdown
## 图表生成失败

❌ **错误**：Mermaid 语法错误  
**原因**：节点标签 `C{是否成功?}` 含中文但未加引号  
**修复**：已自动修复为 `C{"是否成功?"}`  
**重试**：正在重新生成...

（重新生成的图表）
```

## 质量检查清单

生成文件前，必须检查：

### Mermaid
- [ ] 没有子图 ID 与节点 ID 重名
- [ ] 菱形 / 体育场形中的中文已加双引号
- [ ] 标签内无裸露特殊字符（括号、冒号、分号）
- [ ] 图内无重复节点 ID
- [ ] 使用 stateDiagram-v2，非 stateDiagram
- [ ] 已删除所有 click 事件（Obsidian 不支持）

### Excalidraw
- [ ] 文字未溢出形状（autoResize: true）
- [ ] 箭头已正确连接到节点（elementId 一致）
- [ ] 箭头 points 方向正确（相对坐标）
- [ ] 每个元素有全局唯一 ID
- [ ] fontFamily 为 5（Excalifont）
- [ ] 中文无乱码（UTF-8 编码，不转义 Unicode）
- [ ] Obsidian 模式：YAML frontmatter 正确，%% 分隔符存在

### Canvas
- [ ] JSON 无尾随逗号
- [ ] 节点不重叠（检查布局算法）
- [ ] 边引用的节点 ID 存在
- [ ] 分组节点在 nodes 数组靠前位置
- [ ] 文本节点宽度足够（富 Markdown 内容 ≥300px）
- [ ] 边的方向与节点相对位置匹配
