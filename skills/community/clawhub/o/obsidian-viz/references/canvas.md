# Canvas 格式规范

Canvas 是 Obsidian 的原生无限画布格式，支持大型知识网络和交互式探索。

## 文件格式

Canvas 文件为 `.canvas` 扩展名，内容为纯 JSON：

```json
{
  "nodes": [ ...节点对象数组... ],
  "edges": [ ...边对象数组... ]
}
```

**约束**：
- 合法 JSON，无尾随逗号，无注释
- 坐标系：左上原点，x 向右为正，y **向下为正**
- 所有 `id` 为字符串，全局唯一

## 四种节点类型

### 1. 文本节点（最常用）

```json
{
  "id": "n1",
  "type": "text",
  "text": "节点内容\n支持 **Markdown**",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 100,
  "color": "1"
}
```

**字段说明**：
- `id`：全局唯一标识符（字符串）
- `type`：固定为 `"text"`
- `text`：节点内容，支持完整 Markdown 语法
- `x`, `y`：左上角坐标
- `width`, `height`：节点尺寸
- `color`：颜色代码（见配色方案）

### 2. 文件节点（链接到 vault 内文件）

```json
{
  "id": "n2",
  "type": "file",
  "file": "path/to/note.md",
  "x": 300,
  "y": 0,
  "width": 400,
  "height": 300
}
```

**字段说明**：
- `type`：固定为 `"file"`
- `file`：相对于 vault 根目录的文件路径
- 支持的文件类型：`.md`、`.pdf`、`.png`、`.jpg` 等

### 3. 链接节点（外部 URL）

```json
{
  "id": "n3",
  "type": "link",
  "url": "https://example.com",
  "x": 0,
  "y": 200,
  "width": 400,
  "height": 200
}
```

**字段说明**：
- `type`：固定为 `"link"`
- `url`：完整的 URL 地址

### 4. 分组节点（视觉容器）

```json
{
  "id": "grp1",
  "type": "group",
  "label": "服务分组名称",
  "x": -20,
  "y": -20,
  "width": 600,
  "height": 400,
  "color": "5"
}
```

**字段说明**：
- `type`：固定为 `"group"`
- `label`：分组标签（可选）
- 分组节点必须在 `nodes` 数组中**位于子节点之前**，确保渲染在子节点后面

## 边 Schema

```json
{
  "id": "e1",
  "fromNode": "n1",
  "toNode": "n2",
  "fromSide": "right",
  "toSide": "left",
  "label": "连接标签",
  "color": "4",
  "toEnd": "arrow",
  "fromEnd": "none"
}
```

**字段说明**：
- `id`：全局唯一标识符（字符串）
- `fromNode`：起点节点 ID
- `toNode`：终点节点 ID
- `fromSide`：起点侧（`top` / `right` / `bottom` / `left`）
- `toSide`：终点侧（`top` / `right` / `bottom` / `left`）
- `label`：边标签（可选）
- `color`：颜色代码（可选）
- `toEnd`：终点箭头类型（`arrow` / `none`）
- `fromEnd`：起点箭头类型（`arrow` / `none`）

### 方向选择规则

- **水平流（左→右）**：`fromSide: "right"`, `toSide: "left"`
- **垂直流（上→下）**：`fromSide: "bottom"`, `toSide: "top"`
- **放射状**：根据目标节点相对于源节点的方位选择最近侧

## 颜色系统

| 代码 | 颜色 | 推荐用途 |
|------|------|---------|
| `"1"` | 红 | 警告、问题、阻塞 |
| `"2"` | 橙 | 进行中、注意 |
| `"3"` | 黄 | 备注、高亮 |
| `"4"` | 绿 | 完成、成功 |
| `"5"` | 青 | 信息、参考 |
| `"6"` | 紫 | 特殊、外部、创意 |
| `"#hex"` | 自定义 | 任意十六进制颜色 |
| （省略）| 默认灰 | 中性节点 |

### 颜色分配策略

**思维导图**：
- 每个 L1 分支一个颜色
- 子节点继承父节点颜色

**流程图**：
- 绿色：起止节点
- 默认灰：普通步骤
- 黄色：判断节点
- 红色：错误节点

**系统图**：
- 按服务边界 / 团队归属分色
- 同一服务/团队使用相同颜色

## 节点尺寸规则

| 内容长度 | 宽度 | 高度 | 适用场景 |
|---------|------|------|---------|
| 纯标题（≤10字） | 160 | 60 | 简短标签 |
| 短标签（≤20字） | 220 | 80 | 节点名称 |
| 中等标签（≤40字） | 280 | 80 | 描述性标签 |
| 多行 / 描述文字 | 300-400 | 100-150 | 详细说明 |
| 富 Markdown 内容 | 400-500 | 150-250 | 完整笔记 |
| 中心 / 根节点 | ≥200 | ≥80 | 思维导图中心 |
| 分组节点 | 子节点包围框 + 各边 20-30px | 同 | 视觉分组 |

**中文字符估算**：1 字 ≈ 16px（默认字体大小）

**示例**：
```
文字："用户管理模块"（6 个字符）
估算宽度: 6 × 16 = 96px
实际设置: width = 120（留 20% 内边距）
```

## 四种布局算法

### 1. 放射状思维导图

```
中心节点:  x=0, y=0, w=220, h=80

L1 半径:   380px
L1 角度:   angle_i = i × (360/N) - 90  // N 为 L1 节点数量
L1 位置:   x = 380 × cos(angle_i) - w/2
           y = 380 × sin(angle_i) - h/2

L2 半径:   680px（从中心计算）
L2 角度:   在父节点角度 ±30° 范围内均匀分布
```

**示例**（4 个 L1 节点）：
```
angle_0 = 0 × 90 - 90 = -90°  → 正上方
angle_1 = 1 × 90 - 90 = 0°    → 正右方
angle_2 = 2 × 90 - 90 = 90°   → 正下方
angle_3 = 3 × 90 - 90 = 180°  → 正左方
```

### 2. 层级图（从上到下）

```
根节点:    y=0，水平居中
           x = (canvas_width - node_width) / 2

L1 节点:   y=200
           x_i = center_x + (i - (N-1)/2) × (node_w + 60)
           // N 为 L1 节点数量，60 为间距

L2 节点:   y=400
           在父节点下方水平居中子组
           x_i = parent_x + (i - (M-1)/2) × (node_w + 60)
           // M 为该父节点的子节点数量

边方向:    fromSide: "bottom", toSide: "top"
```

**示例**（根节点有 3 个子节点）：
```
根节点: x=400, y=0
L1-1:   x=400 + (0 - 1) × 220 = 180, y=200
L1-2:   x=400 + (1 - 1) × 220 = 400, y=200
L1-3:   x=400 + (2 - 1) × 220 = 620, y=200
```

### 3. 流水线（从左到右）

```
起始:      x=0, y=0

每步:      x += node_width + 80
           y = 0（主线）

分支:      y 偏移 ±180
           上分支: y = -180
           下分支: y = +180

边方向:    fromSide: "right", toSide: "left"
```

**示例**：
```
步骤1: x=0, y=0
步骤2: x=280, y=0
判断: x=560, y=0
  ├→ 是: x=840, y=-180
  └→ 否: x=840, y=+180
```

### 4. 自由聚类布局

```
将相关节点分为若干聚类

聚类内部间距:  80px
聚类之间间距:  150px

聚类排列:      2-3列网格
               每列宽度 = max(聚类宽度) + 150
               每行高度 = max(聚类高度) + 150
```

**示例**（3 个聚类）：
```
聚类1（前端）: x=0, y=0
聚类2（后端）: x=500, y=0
聚类3（数据）: x=0, y=400
```

## 中文文本规则

### 文本编码

- `text` 字段中直接写入中文，无需转义
- 换行使用 `\n`（JSON 转义字符）
- 文本节点支持完整 Markdown 语法

**示例**：
```json
{
  "type": "text",
  "text": "# 用户管理\n\n负责用户的**注册**、**登录**和**权限管理**。\n\n- 支持邮箱注册\n- 支持第三方登录"
}
```

### 文件路径

- `file` 节点路径使用正斜杠 `/`
- 路径相对于 vault 根目录
- 支持中文文件名和文件夹名

**示例**：
```json
{
  "type": "file",
  "file": "笔记/子目录/文件.md"
}
```

## 常见错误清单

| 错误 | 修复方法 |
|------|---------|
| JSON 最后一个元素有尾随逗号 | 删除多余逗号 |
| 节点互相重叠 | 检查布局算法中的间距计算 |
| 边引用了不存在的节点 ID | 确认所有 `fromNode` / `toNode` 在 `nodes` 中存在 |
| 分组节点渲染在子节点前面 | 将分组节点移到 `nodes` 数组靠前位置 |
| 文本节点内容被截断 | 增加 `width`；富 Markdown 内容使用 ≥300px |
| 边的方向在画布上看起来奇怪 | 检查 `fromSide`/`toSide` 是否与节点的实际相对位置匹配 |
| 坐标为负数导致节点不可见 | 确保所有节点坐标为正数，或调整画布视图 |
| 文件节点无法打开 | 检查 `file` 路径是否正确，文件是否存在 |

## 完整示例：简单思维导图

```json
{
  "nodes": [
    {
      "id": "center",
      "type": "text",
      "text": "# 项目架构",
      "x": 400,
      "y": 300,
      "width": 220,
      "height": 80,
      "color": "6"
    },
    {
      "id": "frontend",
      "type": "text",
      "text": "## 前端\n\n- React\n- Redux\n- TypeScript",
      "x": 100,
      "y": 100,
      "width": 250,
      "height": 120,
      "color": "4"
    },
    {
      "id": "backend",
      "type": "text",
      "text": "## 后端\n\n- Node.js\n- Express\n- MongoDB",
      "x": 700,
      "y": 100,
      "width": 250,
      "height": 120,
      "color": "5"
    },
    {
      "id": "devops",
      "type": "text",
      "text": "## DevOps\n\n- Docker\n- Kubernetes\n- CI/CD",
      "x": 400,
      "y": 500,
      "width": 250,
      "height": 120,
      "color": "2"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "center",
      "toNode": "frontend",
      "fromSide": "left",
      "toSide": "bottom",
      "toEnd": "none",
      "fromEnd": "none"
    },
    {
      "id": "e2",
      "fromNode": "center",
      "toNode": "backend",
      "fromSide": "right",
      "toSide": "bottom",
      "toEnd": "none",
      "fromEnd": "none"
    },
    {
      "id": "e3",
      "fromNode": "center",
      "toNode": "devops",
      "fromSide": "bottom",
      "toSide": "top",
      "toEnd": "none",
      "fromEnd": "none"
    }
  ]
}
```

## 完整示例：流程图

```json
{
  "nodes": [
    {
      "id": "start",
      "type": "text",
      "text": "开始",
      "x": 100,
      "y": 50,
      "width": 160,
      "height": 60,
      "color": "4"
    },
    {
      "id": "input",
      "type": "text",
      "text": "输入数据",
      "x": 100,
      "y": 150,
      "width": 160,
      "height": 60
    },
    {
      "id": "validate",
      "type": "text",
      "text": "数据是否有效?",
      "x": 100,
      "y": 250,
      "width": 160,
      "height": 60,
      "color": "3"
    },
    {
      "id": "process",
      "type": "text",
      "text": "处理数据",
      "x": 100,
      "y": 350,
      "width": 160,
      "height": 60
    },
    {
      "id": "error",
      "type": "text",
      "text": "显示错误",
      "x": 350,
      "y": 250,
      "width": 160,
      "height": 60,
      "color": "1"
    },
    {
      "id": "end",
      "type": "text",
      "text": "结束",
      "x": 100,
      "y": 450,
      "width": 160,
      "height": 60,
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "start",
      "toNode": "input",
      "fromSide": "bottom",
      "toSide": "top",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "input",
      "toNode": "validate",
      "fromSide": "bottom",
      "toSide": "top",
      "toEnd": "arrow"
    },
    {
      "id": "e3",
      "fromNode": "validate",
      "toNode": "process",
      "fromSide": "bottom",
      "toSide": "top",
      "label": "是",
      "toEnd": "arrow"
    },
    {
      "id": "e4",
      "fromNode": "validate",
      "toNode": "error",
      "fromSide": "right",
      "toSide": "left",
      "label": "否",
      "toEnd": "arrow"
    },
    {
      "id": "e5",
      "fromNode": "process",
      "toNode": "end",
      "fromSide": "bottom",
      "toSide": "top",
      "toEnd": "arrow"
    },
    {
      "id": "e6",
      "fromNode": "error",
      "toNode": "end",
      "fromSide": "bottom",
      "toSide": "right",
      "toEnd": "arrow"
    }
  ]
}
```

## 完整示例：分组布局

```json
{
  "nodes": [
    {
      "id": "group-frontend",
      "type": "group",
      "label": "前端服务",
      "x": -20,
      "y": -20,
      "width": 600,
      "height": 300,
      "color": "4"
    },
    {
      "id": "react",
      "type": "text",
      "text": "React App",
      "x": 50,
      "y": 50,
      "width": 200,
      "height": 80
    },
    {
      "id": "redux",
      "type": "text",
      "text": "Redux Store",
      "x": 300,
      "y": 50,
      "width": 200,
      "height": 80
    },
    {
      "id": "group-backend",
      "type": "group",
      "label": "后端服务",
      "x": -20,
      "y": 320,
      "width": 600,
      "height": 300,
      "color": "5"
    },
    {
      "id": "api",
      "type": "text",
      "text": "API Server",
      "x": 50,
      "y": 390,
      "width": 200,
      "height": 80
    },
    {
      "id": "db",
      "type": "text",
      "text": "Database",
      "x": 300,
      "y": 390,
      "width": 200,
      "height": 80
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "react",
      "toNode": "redux",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "redux",
      "toNode": "api",
      "fromSide": "bottom",
      "toSide": "top",
      "label": "API 调用",
      "toEnd": "arrow"
    },
    {
      "id": "e3",
      "fromNode": "api",
      "toNode": "db",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

## 生成前必检清单

- [ ] JSON 无尾随逗号
- [ ] 所有节点有全局唯一 `id`
- [ ] 所有边的 `fromNode` 和 `toNode` 在 `nodes` 中存在
- [ ] 分组节点在 `nodes` 数组靠前位置
- [ ] 节点坐标为正数（或接近 0）
- [ ] 节点不重叠（检查布局算法）
- [ ] 文本节点宽度足够（富 Markdown 内容 ≥300px）
- [ ] 边的 `fromSide` 和 `toSide` 与节点相对位置匹配
- [ ] 文件节点的 `file` 路径正确
- [ ] 链接节点的 `url` 为完整 URL
- [ ] 中文无转义（直接使用 UTF-8）
- [ ] 文件编码为 UTF-8

## 高级技巧

### 1. 使用分组节点组织复杂布局

将相关节点放在同一个分组内，便于视觉识别和整体移动。

### 2. 利用颜色编码传递信息

- 红色：问题、阻塞
- 绿色：完成、成功
- 黄色：进行中、注意
- 蓝色：信息、参考

### 3. 合理使用边标签

边标签应简洁明了，说明节点之间的关系类型。

### 4. 控制节点密度

- 节点间距至少 60px
- 分组间距至少 150px
- 避免过度拥挤

### 5. 使用文件节点链接详细内容

对于需要详细说明的节点，使用文件节点链接到完整笔记。

### 6. 利用 Markdown 格式化文本节点

文本节点支持完整 Markdown 语法，可以使用标题、列表、粗体、斜体等格式。
