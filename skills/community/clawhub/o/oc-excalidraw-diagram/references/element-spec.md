# Excalidraw 元素规范

## 基础结构

每个元素必须包含以下字段：

```json
{
  "id": "唯一ID（8位字母数字）",
  "type": "rectangle|ellipse|diamond|arrow|text",
  "x": 100,
  "y": 100,
  "width": 160,
  "height": 60,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": {"type": 3},
  "seed": 12345,
  "version": 1,
  "versionNonce": 12345,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

---

## 形状元素（rectangle / ellipse / diamond）

```json
{
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 60,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "roughness": 1,
  "roundness": {"type": 3},
  "text": "节点文字",
  "fontSize": 16,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

**注意：** 形状元素直接包含 `text`、`fontSize`、`fontFamily` 等文字属性（不需要单独 text 元素）。

### fillStyle 选项
- `"solid"` — 实心填充（推荐）
- `"hachure"` — 手绘斜线（Excalidraw 特色）
- `"cross-hatch"` — 交叉线
- `"dots"` — 点状

### roundness 选项
- `{"type": 3}` — 圆角（rectangle 推荐）
- `{"type": 2}` — 更圆的角
- `null` — 直角

---

## 箭头元素（arrow）

```json
{
  "type": "arrow",
  "id": "arr001",
  "x": 300, "y": 130,
  "width": 100, "height": 0,
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "roundness": {"type": 2},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": {
    "elementId": "源元素ID",
    "focus": 0,
    "gap": 8
  },
  "endBinding": {
    "elementId": "目标元素ID",
    "focus": 0,
    "gap": 8
  }
}
```

**points 计算：**
- `[0, 0]` = 箭头起点（相对坐标）
- `[dx, dy]` = 箭头终点（相对于起点的偏移）

**arrowhead 选项：**
- `"arrow"` — 普通箭头（推荐）
- `"bar"` — 横线
- `"dot"` — 圆点
- `null` — 无箭头

---

## 文本元素（text）

独立文本标签（用于注释、说明）：

```json
{
  "type": "text",
  "id": "txt001",
  "x": 150, "y": 80,
  "width": 200, "height": 25,
  "text": "标签内容",
  "fontSize": 16,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "containerId": null
}
```

---

## boundElements 绑定

当箭头连接到形状时，形状的 `boundElements` 需要记录箭头 ID：

```json
"boundElements": [
  {"type": "arrow", "id": "arr001"}
]
```

---

## 颜色速查

```
Primary（主要）:   #a5d8ff  浅蓝
Secondary（次要）: #b2f2bb  浅绿
Important（重要）: #ffd43b  黄色
Alert（警告）:     #ffc9c9  浅红
Neutral（中性）:   #f1f3f5  浅灰
Transparent:      transparent
Stroke:           #1e1e1e  深灰（默认线条）
```

---

## 元素尺寸参考

| 元素类型 | 推荐宽度 | 推荐高度 |
|---------|---------|---------|
| 普通节点 | 160–200px | 60px |
| 宽节点/模块 | 200–300px | 80px |
| 小节点 | 100–140px | 50px |
| 决策菱形 | 160px | 80px |
| 开始/结束椭圆 | 140px | 60px |
| 时序参与者 | 120px | 60px |
