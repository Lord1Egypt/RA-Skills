# Diagram Implementations

> **说明**: 本文档中的代码示例为**概念性伪代码和结构摘录**，旨在说明各图表类型的布局算法和渲染策略。实际实现可能与本文档略有差异，具体细节请参考 beautiful-mermaid 源码 (`src/ascii/*.ts`)。

Use this file when you need details about how each Mermaid diagram type is rendered to ASCII/Unicode.

## Table of Contents

- Flowchart / State Diagram
- Sequence Diagram
- Class Diagram
- ER Diagram
- 扩展指南：添加新图表类型

## Flowchart / State Diagram

**Rendering strategy:** grid layout + A* routing.

**Key characteristics:**
- Each node occupies a 3x3 grid block.
- Supports TD/LR/BT/RL directions (BT uses vertical flip).
- Handles collisions when placing nodes.

**Core flow (grid.ts → createMapping):**
1. Identify root nodes (no incoming edges).
2. Place nodes by level (LR/TD variants).
3. Compute column widths / row heights (label-length based).
4. Route edges via A*.
5. Determine label placement (widest segment).
6. Convert grid → drawing coordinates.
7. Generate node box drawings.
8. Compute subgraph bounding boxes.

```typescript
renderMermaidAscii('graph TD\n  A --> B')
```

## Sequence Diagram

**Rendering strategy:** column layout (actors) + row layout (messages).

**Key characteristics:**
- Each actor occupies a column; lifelines are vertical.
- Messages are rows; arrows connect lifelines.
- Not grid-based; uses linear layout.

**Layout algorithm:**
```typescript
// 1) actor columns
const actorIdx = new Map<string, number>()
diagram.actors.forEach((a, i) => actorIdx.set(a.id, i))

// 2) column gaps based on label width
for (const msg of diagram.messages) {
  const needed = msg.label.length + 4
  const numGaps = hi - lo
  const perGap = Math.ceil(needed / numGaps)
}

// 3) message vertical positions
// - self message: 3 rows
// - normal message: 2 rows
```

**Special cases:**
- Block groups (loop/alt/opt/par)
- Notes around actors
- Self messages drawn with a right-side loop

## Class Diagram

**Rendering strategy:** layered layout + UML markers.

**Key characteristics:**
- Top-down layers (parent above child).
- Multi-compartment class boxes (header/attributes/methods).
- All relationship types place nodes on different layers.

**UML markers:**
```
inheritance: △
realization: ▽
composition: ◆
aggregation: ◇
association: ▶
dependency: ▶ (dashed)
```

**Layout algorithm:**
```typescript
// 1) build hierarchy
for (const rel of diagram.relationships) {
  const isHierarchical = rel.type === 'inheritance' || rel.type === 'realization'
  const parentId = isHierarchical && rel.markerAt === 'to' ? rel.to : rel.from
  parents.get(parentId)!.add(childId)
}

// 2) BFS level assignment
const level = new Map<string, number>()
const roots = diagram.classes.filter(c => !parents.has(c.id))

// 3) horizontal placement per level
for (let lv = 0; lv <= maxLevel; lv++) {
  const group = levelGroups[lv]
  for (const id of group) {
    const cls = classById.get(id)
    // place at current X; Y = level row
  }
  currentY += maxH + vGap
}
```

## ER Diagram

**Rendering strategy:** grid layout + crow's foot notation.

**Key characteristics:**
- Entities are two-section boxes (header + attributes).
- Entities placed in rows (grid-like layout).
- Crow's foot markers at relationship endpoints.

**Crow's foot markers:**
```
one (||):       ──║── or --||--
zero-one (o|):  ──o║── or --o|--
many (}):      ──╢── or --<|-- (or }|)
zero-many (o{): ──o╢── or --o<-- (or o{)
```

**Layout algorithm:**
```typescript
// 1) grid placement (max sqrt(N) entities per row)
const maxPerRow = Math.max(2, Math.ceil(Math.sqrt(diagram.entities.length)))

for (const ent of diagram.entities) {
  const [entity, sections] = placed.get(id)
  entity.x = currentX
  entity.y = currentY
}

// 2) crow's foot routing
const sameRow = Math.abs(e1CY - e2CY) < Math.max(e1.height, e2.height)
if (sameRow) {
  // horizontal connection
} else {
  // vertical connection
}
```

---

## 扩展指南：添加新图表类型

如果你想为 beautiful-mermaid 添加新的图表类型支持，按以下步骤进行：

### 步骤清单

#### 1. 创建解析器 (Parser)

**涉及文件**: `src/parser.ts` 或新建 `src/<diagram-type>/parser.ts`

- [ ] 定义图表类型的 AST 结构（节点、边、属性）
- [ ] 实现语法解析函数，将 Mermaid 文本转为 AST
- [ ] 添加错误处理和验证逻辑

```typescript
// 示例：新图表类型的 AST 定义
interface NewDiagram {
  type: 'new-diagram'
  nodes: NewNode[]
  edges: NewEdge[]
  config?: DiagramConfig
}
```

#### 2. 实现布局引擎 (Layout)

**涉及文件**: `src/ascii/<diagram-type>.ts`

- [ ] 确定布局策略（网格/分层/力导向/线性）
- [ ] 实现节点位置计算
- [ ] 实现边路由算法
- [ ] 处理标签位置

**选择布局策略**:
- **Grid Layout**: 流程图、状态图、ER 图（节点对齐网格）
- **Layered Layout**: 类图（分层排列，父在上子在下）
- **Linear Layout**: 序列图（按时间线排列）

#### 3. 实现渲染器 (Renderer)

**涉及文件**: `src/ascii/<diagram-type>.ts`

- [ ] 绘制节点（使用 `draw.ts` 中的原语）
- [ ] 绘制边和箭头
- [ ] 绘制标签和注释
- [ ] 支持 ASCII 和 Unicode 两种模式

```typescript
// 示例：渲染函数结构
function renderNewDiagram(
  diagram: NewDiagram,
  options: AsciiRenderOptions
): string {
  // 1. 布局计算
  const layout = calculateLayout(diagram, options)
  
  // 2. 创建画布
  const canvas = mkCanvas(layout.width, layout.height)
  
  // 3. 绘制节点
  for (const node of layout.nodes) {
    drawNode(canvas, node, options.useAscii)
  }
  
  // 4. 绘制边
  for (const edge of layout.edges) {
    drawEdge(canvas, edge, options.useAscii)
  }
  
  // 5. 返回字符串
  return canvasToString(canvas)
}
```

#### 4. 注册到主入口

**涉及文件**: `src/ascii/index.ts`

- [ ] 在 `renderMermaidAscii` 中添加图表类型检测
- [ ] 添加对新图表类型的路由

```typescript
// src/ascii/index.ts
export function renderMermaidAscii(
  input: string,
  options?: AsciiRenderOptions
): string {
  const diagram = parseDiagram(input)
  
  switch (diagram.type) {
    case 'flowchart':
      return renderFlowchart(diagram, options)
    case 'sequence':
      return renderSequence(diagram, options)
    // ... 其他类型
    case 'new-diagram':  // ← 添加新类型
      return renderNewDiagram(diagram, options)
    default:
      throw new Error(`Unsupported diagram type: ${diagram.type}`)
  }
}
```

#### 5. 添加测试

**涉及文件**: `src/__tests__/<diagram-type>.test.ts`

- [ ] 编写解析器单元测试
- [ ] 编写布局引擎测试
- [ ] 编写渲染输出快照测试
- [ ] 添加边界情况测试（空图、单节点、复杂图）

#### 6. 更新文档

- [ ] 在 `SKILL.md` 中添加新图表类型到支持列表
- [ ] 在 `references/diagrams.md` 中添加实现细节
- [ ] 提供最小使用示例

### 设计原则

1. **渐进式渲染**: 先实现基础功能，再添加高级特性
2. **复用现有工具**: 优先使用 `draw.ts`、`canvas.ts`、`pathfinder.ts` 中的工具函数
3. **双模式支持**: 同时支持 ASCII 和 Unicode 输出
4. **可配置性**: 允许通过 `AsciiRenderOptions` 调整行为
5. **错误处理**: 提供清晰的错误信息，帮助用户调试语法问题

### 参考实现

研究现有图表类型的实现作为参考：
- **最简单**: Flowchart (`src/ascii/grid.ts`) - 基于网格的布局
- **中等**: Sequence (`src/ascii/sequence.ts`) - 线性布局
- **最复杂**: Class (`src/ascii/class-diagram.ts`) - 分层布局 + 多隔间节点
