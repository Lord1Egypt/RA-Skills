# 11 · 高度验证速查

> Grid+Flex 混用时，内容溢出被摘要栏覆盖的根因与解决方案。

---

## 问题症状

```
现象：.ct 内的底部卡片被 48px 摘要栏覆盖，显示不全
根因：布局容器有效高度 > 580px，内容溢出被 overflow: hidden 截断
```

---

## 高度计算公式

### 布局容器有效高度

```
有效高度 = height + padding-top

❌ 错误写法：
.layout-x { height: 100%; padding-top: 8px; }
→ 有效高度 = 580px + 8px = 588px  ✗

✅ 正确写法：
.layout-x { height: calc(580px - 8px); padding-top: 8px; }
→ 有效高度 = 556px + 8px = 564px ✓
```

### 多卡垂直排列总高度

```
三卡总高 = 卡片数量 × (卡片高度 + gap) - gap(最后一个无 gap)

示例：3 张卡片，gap=8px
三卡总高 = 3 × (176px + 8px) - 8px = 544px ≤ 556px ✓

可用高度 = 580px - padding-top(8px) - gaps(8px×2) = 556px
每卡最大高度 = 556px / 3 ≈ 185px（含 gap 则 176px）
```

---

## 强制 CSS 模板

### 模板 1：Flex 容器三卡

```css
.layout-l {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 8px;
  padding-top: 8px;
  height: calc(580px - 8px);  /* ← 关键 */
}

.left-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card {
  flex: 1;
  min-height: 0;  /* ← 关键：允许 flex 收缩 */
  height: 176px;  /* ← 关键：显式固定高度 */
  overflow: hidden;
}
```

### 模板 2：Grid 容器三卡

```css
.layout-l {
  display: grid;
  grid-template-columns: 1fr 340px;
  grid-template-rows: repeat(3, 176px);
  gap: 8px;
  padding-top: 8px;
  height: calc(580px - 8px);
}

.left-grid {
  display: grid;
  grid-template-rows: repeat(3, 176px);  /* ← 关键：显式定义行高 */
  gap: 8px;
}

.card {
  min-height: 0;  /* 允许收缩 */
  overflow: hidden;
}
```

### 模板 3：双列 + 底部汇聚

```css
.layout-g {
  display: grid;
  grid-template-rows: 1fr 1fr 160px;  /* ← 显式定义三行高度 */
  gap: 8px;
  padding-top: 8px;
  height: calc(580px - 8px);
}

/* 验证：1fr+1fr+160px+8px×2 = 580px → 1fr = (580-8-160)/2 = 206px */
```

---

## 内容密度上限表

| 卡片类型 | 最大高度 | 适用场景 | 内容建议 |
|---------|---------|---------|---------|
| 标准卡 | 176px | 大多数内容页 | 标题 +60-80 字正文 + 数据块 |
| 紧凑卡 | 120px | 高密度对比页 | 标题 +40-60 字正文 |
| 全高卡 | 520px | 单卡片满屏 | 标题 +200-300 字正文 + 多图 |

---

## 快速自查清单（每页生成后必填）

```
□ 布局容器 height 是否为 calc(580px - padding-top)？
□ flex 卡片是否有 `min-height: 0` + 显式 `height`（非 100%）？
□ Grid 行高是否显式定义（非 `1fr` 自动撑高）？
□ 三卡总高是否 ≤ 556px（580 - padding - gaps）？
□ 卡片正文是否 ≤ 80 字（避免撑高）？
□ Chrome 截图无 ⚠ 溢出警告？
```

---

## 常见错误与修复

| 错误写法 | 问题 | 修复 |
|---------|------|------|
| `height: 100%` | 实际 = 580px + padding = 588px+ | `height: calc(580px - 8px)` |
| `flex: 1` 无 `min-height: 0` | flex 子元素按内容撑高 | 加 `min-height: 0` + 显式 `height` |
| `grid-template-rows: 1fr 1fr 1fr` | 1fr 按内容自动撑高 | 改为 `repeat(3, 176px)` |
| 卡片正文 > 80 字 | 内容撑高卡片 | 精简文字或减小字号 |
| 三卡总高 > 556px | 溢出被截断 | 降低卡片高度或减少卡片数量 |

---

## 高度计算模板（复制填写）

```
【本页高度验证】

布局容器：
  height: calc(580px - __px) = __px
  padding-top: __px
  有效高度：__ + __ = 580px ✓

内容区：
  卡片数量：__ 张
  gap: __px
  可用高度：580 - padding(__) - gaps(__×__) = __px
  每卡高度：__px / __ = __px

验证：
  卡片总高：__ × (__ + __) - __ = __px ≤ __px ✓
  卡片正文：≤ 80 字 ✓
```
