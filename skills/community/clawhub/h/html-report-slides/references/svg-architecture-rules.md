# SVG 架构图布局原则（容易返工，务必遵守）

## 基本设置

```html
<svg viewBox="0 0 1180 620" style="width:100%;height:auto;" font-family="Inter, 'PingFang SC', sans-serif">
  <defs>
    <!-- 箭头定义 -->
    <marker id="arrowBlue"    markerWidth="5" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 5 2, 0 4" fill="#5070ff"/>
    </marker>
    <marker id="arrowBlueRev" markerWidth="5" markerHeight="4" refX="0" refY="2" orient="auto">
      <polygon points="5 0, 0 2, 5 4" fill="#5070ff"/>
    </marker>
    <marker id="arrowGreen"   markerWidth="5" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 5 2, 0 4" fill="#10b981"/>
    </marker>
    <marker id="arrowOrange"  markerWidth="5" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 5 2, 0 4" fill="#f59e0b"/>
    </marker>
  </defs>
  ...
</svg>
```

## 1. 容器与层级规划

- **viewBox 标准**：`0 0 1180 620`
- **外层容器统一** x=30, width=1120（左右各留 30 边距）
- **分层从下到上排列**（y 值从大到小）：
  - 最底层（云产品）   y=530, height=70
  - 支撑层           y=420, height=80
  - Agent 层         y=300, height=95
  - 触达层           y=130, height=125
  - 用户层           y=20,  height=90

## 2. 方块均匀分布的正确算法

**不是简单排列方块**。必须：
1. 确定容器总宽度（1120）
2. 确定每个方块宽度
3. 计算 `剩余空间 = 容器宽 - Σ 方块宽`
4. 计算 `间隙 = 剩余空间 / (方块数 + 1)`（两端也留间距）
5. 按此间距依次摆放

### 嵌套容器
- 如果有"外部用户"这种包含子方块的容器，外层容器和内层方块要一起参与整层的均匀分布
- 内层子方块在外层容器里也要均匀分布

## 3. 连线必须对准方块中心

### 计算公式
```
centerX = rect.x + rect.width / 2
topY    = rect.y                    (顶边中点)
bottomY = rect.y + rect.height      (底边中点)
leftX   = rect.x                    (左边中点: y = rect.y + rect.height/2)
rightX  = rect.x + rect.width       (右边中点)
```

### 要求
- 起点和终点都要用上面公式算出来的精确坐标
- **不要凭感觉写坐标**
- 修改前先 search 确认 rect 的 x, y, width, height

### 示例
```html
<!-- 方块: <rect x="60" y="338" width="140" height="36"/> -->
<!-- 中心点: (60+140/2, 338+36/2) = (130, 356) -->
<!-- 顶部中点: (130, 338) 底部中点: (130, 374) -->
```

## 4. 连线样式规范

### 同层双向连线
```html
<line x1="..." y1="..." x2="..." y2="..."
      stroke="#5070ff" stroke-width="2"
      marker-start="url(#arrowBlueRev)"
      marker-end="url(#arrowBlue)"
      opacity="0.85"/>
```

### 跨层连线（贝塞尔曲线）
```html
<path d="M x1,y1 C cp1x,cp1y  cp2x,cp2y  x2,y2"
      fill="none"
      stroke="#5070ff"
      stroke-width="2"
      stroke-dasharray="7,4"
      marker-end="url(#arrowBlue)"
      opacity="0.85"/>
```

- 跨层用**虚线**（stroke-dasharray="7,4"）
- 同层用**实线**
- 透明度 0.8~0.85，避免太刺眼

### 连线标签
```html
<text x="..." y="..." font-size="13" fill="#5070ff" font-weight="700" font-style="italic">WB线</text>
```
标签放在连线中段附近，颜色用连线色。

## 5. 故事线配色（已固化）

| 故事线 | 颜色 | 用途 |
|---|---|---|
| WB 线 | `#5070ff`（蓝）| 内部产品协同链路 |
| claw 线 | `#10b981`（绿）| 分发触达链路 |
| skill 线 | `#f59e0b`（橙）| 外部自助链路 |

## 6. 层级配色

```
用户层:     绿   rgba(64,145,108,0.08 ~ 0.2),  text #95d5b2 / #a7f3d0
触达层:     蓝   rgba(80,112,255,0.06 ~ 0.2),  text #93b4ff / #a0b4ff
Agent 层:  紫   rgba(124,58,237,0.08 ~ 0.2), text #c4b5fd / #e0d4ff
支撑层:     橙   rgba(234,88,12,0.08 ~ 0.15), text #fdba74 / #fed7aa
云产品:     灰   rgba(71,85,105,0.25),         text #94a3b8
```

## 7. 虚线分组容器

用于表示逻辑分组（如"外部用户"、"IM 容器"、"官网容器"）：

```html
<rect x="..." y="..." width="..." height="..." rx="10"
      fill="rgba(80,112,255,0.04)"
      stroke="rgba(100,140,255,0.4)"
      stroke-width="1.5"
      stroke-dasharray="6,3"/>
```

## 8. 一次做对的检查清单

修改架构图后，必须逐项确认：

- [ ] 所有方块在容器内均匀分布（计算过间距）
- [ ] 所有连线起终点对准方块中心（用 rect 坐标算）
- [ ] 移动方块后检查所有关联连线（易漏）
- [ ] 嵌套分组的内外空间协调
- [ ] 层级配色与 references 一致
- [ ] 故事线颜色正确（WB蓝/claw绿/skill橙）
- [ ] 跨层用虚线、同层用实线
- [ ] 连线透明度 0.8~0.85
- [ ] 图例/标签颜色与连线一致
- [ ] 本地预览确认无错位

## 9. 常见 Bug

- **方块跑出容器**：检查 x+width 有没有超过容器右边界（1150）
- **连线歪了**：99% 是坐标没用 rect 中心算
- **修改一个方块忘了调相关连线**：每次移动方块必须 grep 该方块原坐标，确认没有别的连线引用
- **嵌套容器布局乱**：嵌套时内外 padding 一起算
