# Troubleshooting and Optimization

Use this file for debugging, performance tuning, and best practices.

## Table of Contents

- 故障排查决策树
- 性能优化指南
- 最小复现模板
- 最佳实践

## 故障排查决策树

### 症状：节点重叠

```
节点重叠 (Nodes Overlapping)
├── 原因 1: 默认 padding 不足
│   ├── 定位: 检查 options.paddingX / paddingY 值
│   └── 修复: 增大间距
│       ```typescript
│       const ascii = renderMermaidAscii(diagram, { 
│         paddingX: 8,  // 默认 5 → 增大到 8
│         paddingY: 6   // 默认 5 → 增大到 6
│       })
│       ```
│
├── 原因 2: 子图嵌套过深
│   ├── 定位: 检查是否多层 subgraph 嵌套
│   └── 修复: 简化子图结构，避免超过一层嵌套
│
└── 原因 3: 节点标签过长
    ├── 定位: 检查是否有超长标签 (>30字符)
    └── 修复: 缩短标签或使用换行
```

### 症状：边穿过节点

```
边穿过节点 (Edges Crossing Nodes)
├── 原因 1: 路由空间不足
│   ├── 定位: 观察边是否被迫穿过节点区域
│   └── 修复: 增大 paddingX/paddingY，提供更大路由空间
│
├── 原因 2: A* 启发式偏好锐角
│   ├── 定位: 边呈现过多直角转折
│   └── 修复: 在 pathfinder.ts 中调整启发式函数权重
│       ```typescript
│       // 增加对角线移动的权重，减少直角转折
│       if (absX === 0 || absY === 0) return absX + absY
│       return absX + absY + 0.5  // 原来是 +1，改为 +0.5
│       ```
│
└── 原因 3: 节点未正确标记为障碍物
    ├── 定位: 检查 grid.ts 中是否正确调用 reserveSpotInGrid
    └── 修复: 确保所有节点在 A* 前被标记为不可通行
```

### 症状：标签截断或错位

```
标签问题 (Label Issues)
├── 症状 A: 标签被截断
│   ├── 原因: 列宽不足以容纳标签
│   ├── 定位: 检查 determineLabelLine 计算的最大宽度
│   └── 修复: 
│       1. 增大 paddingX
│       2. 缩短标签文本
│       3. 在 grid.ts 中手动扩展列宽
│
└── 症状 B: 标签位置偏移
    ├── 原因: 标签未对齐到边的中点
    ├── 定位: 检查 labelLine 计算是否正确
    └── 修复: 确保选择最宽的边段放置标签
```

### 症状：边框错位或对齐异常（含中文标签）

```
对齐异常 (CJK Width Issues)
├── 原因 1: 终端/编辑器将中文字符按双宽渲染
│   ├── 定位: 同一示例在不同终端显示不一致
│   └── 修复: 使用等宽且支持 CJK 的字体（如 Sarasa Mono）
│
├── 原因 2: 字体并非严格等宽
│   ├── 定位: ASCII/Unicode 边框出现错位或拉伸
│   └── 修复: 切换为等宽字体，并关闭“可变宽度”显示
│
└── 原因 3: 终端编码不一致
    ├── 定位: Unicode 边框显示为乱码
    └── 修复: 改用 ASCII 模式 (useAscii: true) 或切换 UTF-8 终端
```

### 症状：渲染结果为空或报错

```
渲染失败 (Render Failure)
├── 错误: "Unsupported diagram type"
│   ├── 原因: 使用了不支持的图表类型
│   ├── 定位: 检查输入的 Mermaid 语法
│   └── 修复: 确认使用支持的类型 (flowchart/state/sequence/class/er)
│
├── 错误: 输出空字符串
│   ├── 原因 1: 输入为空或格式错误
│   ├── 定位: 检查输入字符串是否有效
│   └── 修复: 使用最小可运行示例测试
│       ```typescript
│       renderMermaidAscii('graph LR\n  A --> B')  // 最简单的测试
│       ```
│   └── 原因 2: 解析失败但未抛出错误
│       └── 修复: 检查 parser.ts 的错误处理逻辑
│
└── 错误: 字符显示异常 (乱码)
    ├── 原因: 终端不支持 UTF-8
    ├── 定位: 在其他终端测试或使用 useAscii: true
    └── 修复: 切换到 ASCII 模式
        ```typescript
        renderMermaidAscii(diagram, { useAscii: true })
        ```
```

## 性能优化指南

### 症状：渲染速度慢 (>500ms)

```
性能问题 (Performance Issues)
├── 原因 1: 图过大 (节点数 >30)
│   ├── 定位: 统计节点和边的数量
│   └── 修复:
│       1. 拆分为多个小图
│       2. 限制 A* 搜索深度
│       3. 使用更简单的布局策略
│
├── 原因 2: A* 算法复杂度过高
│   ├── 定位: 检查 pathfinder.ts 中的搜索范围
│   └── 修复:
│       1. 限制最大搜索步数
│       2. 优化启发式函数
│       3. 预计算常用路径
│
└── 原因 3: 画布合并操作频繁
    ├── 定位: 检查 canvas.ts 中 mergeCanvases 调用次数
    └── 修复: 批量合并，减少重复深拷贝
        ```typescript
        // 优化前: 多次合并
        let canvas = mkCanvas(w, h)
        for (const node of nodes) {
          canvas = mergeCanvases(canvas, node.canvas)  // 每次创建新画布
        }
        
        // 优化后: 单次合并
        const canvas = mkCanvas(w, h)
        mergeCanvasesInPlace(canvas, nodes.map(n => n.canvas))  // 原地合并
        ```
```

## 最小复现模板

当你需要报告问题或调试时，使用以下模板创建最小可复现示例：

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'

// 环境信息
const env = {
  version: '0.1.3',  // beautiful-mermaid 版本
  runtime: 'Node.js 18',  // 或 Bun 1.0
  options: {
    useAscii: false,
    paddingX: 5,
    paddingY: 5,
    boxBorderPadding: 1
  }
}

// 问题描述: [在此描述症状]

// 最小输入
const diagram = `
graph TD
  A[节点A] --> B[节点B]
`

// 实际输出
const result = renderMermaidAscii(diagram, env.options)
console.log(result)

// 预期输出: [在此描述期望的结果]
```

## 最佳实践

### 图表设计建议

1. **标签长度**: 保持节点标签在 10-20 字符内，过长会影响布局
2. **方向一致性**: 同一图表使用统一方向 (TD/LR)，避免混用
3. **子图使用**: 子图作为逻辑分组，避免跨子图边
4. **间距调整**: 复杂图增大 padding，简单图可减小以节省空间

### 字符模式选择

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 终端显示 | Unicode | 美观，现代终端都支持 |
| 日志文件 | ASCII | 最大兼容性，避免编码问题 |
| 代码注释 | ASCII | 确保所有编辑器正确显示 |
| 邮件/文档 | Unicode | 更好的阅读体验 |

### 调试技巧

1. **渐进式测试**: 从最简单的图开始，逐步增加复杂度
2. **对比测试**: 同时测试 ASCII 和 Unicode 模式，定位字符问题
3. **参数调整**: 固定图表，调整 padding 观察布局变化
4. **单元测试**: 为自定义图表类型编写快照测试

## 参考资料

- 布局算法细节: `core-systems.md`
- 图表实现: `diagrams.md`
- 字符表: `characters.md`
