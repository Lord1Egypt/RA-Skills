# Core Systems

> **说明**: 本文档中的代码示例为**概念性伪代码和结构摘录**，旨在说明核心系统的工作原理。实际实现可能与本文档略有差异，具体细节请参考 beautiful-mermaid 源码。

Use this file for low-level rendering internals: types, canvas, drawing primitives, grid layout, pathfinding, routing, and render options.

## Table of Contents

- Types
- Canvas
- Drawing Primitives
- Grid Layout
- Pathfinding (A*)
- Edge Routing
- Render Order (layering)
- Render Options

## Types

```typescript
interface GridCoord { x: number; y: number }
interface DrawingCoord { x: number; y: number }

export const Up = { x: 1, y: 0 }
export const Down = { x: 1, y: 2 }
export const Left = { x: 0, y: 1 }
export const Right = { x: 2, y: 1 }
export const UpperLeft = { x: 0, y: 0 }
export const UpperRight = { x: 2, y: 0 }
export const LowerLeft = { x: 0, y: 2 }
export const LowerRight = { x: 2, y: 2 }
export const Middle = { x: 1, y: 1 }

interface AsciiNode { name, displayLabel, index, gridCoord, drawing, drawing: Canvas, ... }
interface AsciiEdge { from, to, text, path, labelLine, startDir, endDir }
interface AsciiSubgraph { name, nodes, parent, children, minX, minY, maxX, maxY }

type Canvas = string[][]
```

## Canvas

```typescript
mkCanvas(width, height): Canvas
increaseSize(canvas, newWidth, newHeight): void
mergeCanvases(base, offset, useAscii, ...canvasesToMerge): Canvas
canvasToString(canvas): string
flipCanvasVertically(canvas): void
```

## Drawing Primitives

```typescript
drawBox(node, graph): Canvas
drawMultiBox(sections, useAscii, padding): Canvas
drawLine(canvas, from, to, offsetFrom, offsetTo, useAscii): DrawingCoord[]
drawArrow(graph, edge): [Canvas, Canvas, Canvas, Canvas]
drawCorners(graph, path): Canvas
```

## Grid Layout

```typescript
reserveSpotInGrid(graph, node, requested): GridCoord
gridToDrawingCoord(graph, coord, dir): DrawingCoord

createMapping(graph): void
// 1) roots → 2) placement → 3) column/row sizes → 4) A* edges
// 5) label line → 6) grid→drawing → 7) draw nodes → 8) subgraphs
```

## Pathfinding (A*)

```typescript
heuristic(a, b): number {
  const absX = Math.abs(a.x - b.x)
  const absY = Math.abs(a.y - b.y)
  if (absX === 0 || absY === 0) return absX + absY
  return absX + absY + 1
}

const MOVES = [
  { x: 0, y: -1 }, { x: 0, y: 1 },
  { x: -1, y: 0 }, { x: 1, y: 0 },
  { x: -1, y: -1 }, { x: 1, y: -1 },
  { x: -1, y: 1 },
]

getPath(graph, edge): GridCoord[]
// min-heap, costSoFar, cameFrom
```

## Edge Routing

```typescript
determineStartAndEndDir(edge): [preferred, alternative]
determinePath(graph, edge): void
determineLabelLine(graph, edge): void
```

Label placement picks the first segment wide enough for the label; otherwise the widest segment and expands the mid-column width.

## Render Order (layering)

1. Subgraph boxes
2. Node boxes
3. Edge paths
4. Edge corners
5. Box-start connections
6. Arrow heads
7. Edge labels
8. Subgraph labels

## Render Options

```typescript
interface AsciiRenderOptions {
  useAscii?: boolean;
  paddingX?: number;
  paddingY?: number;
  boxBorderPadding?: number;
}
```
