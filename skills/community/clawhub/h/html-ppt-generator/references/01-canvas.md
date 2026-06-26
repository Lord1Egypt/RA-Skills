# 01 · 画布与结构规则

---

## 尺寸来源

用户 PPT 画布为 **10.59" × 7.499"**（非默认 13.33"×7.5"）。

```
宽：10.59 × 96dpi = 1016.64 → 取 1017px
高：7.499 × 96dpi = 719.90  → 取  720px
比值：1.4125 ≈ √2（接近 A4 横向）
```

**所有页面统一使用 1017×720px，禁止使用其他值。**

---

## 四区结构

```
┌─────────────────────────────────┐  ← 720px 总高
│  Header   · 72px                │  页眉
├─────────────────────────────────┤
│                                 │
│  Content  · 580px               │  主内容
│                                 │
├─────────────────────────────────┤
│  Summary  · 48px                │  摘要栏
├─────────────────────────────────┤
│  Footer   · 20px                │  页脚
└─────────────────────────────────┘
```

### 基础 CSS（所有模板共用，不得修改）

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  width: 1017px;  height: 720px;
  min-width: 1017px; max-width: 1017px;
  min-height: 720px; max-height: 720px;
  overflow: hidden;
  font-size: 12px; line-height: 1.45;
}

/* 四区 */
.hd {
  height: 72px;
  padding: 0 25px;
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.ct {
  height: 580px;
  padding: 0 25px;          /* ← 仅左右，绝不加 padding-top/bottom */
  overflow: hidden;
  flex-shrink: 0;
}
.sm {
  height: 48px;
  padding: 0 25px;
  display: flex; align-items: center; gap: 8px;
  flex-shrink: 0;
}
.ft {
  height: 20px;
  padding: 0 25px;
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
```

> ⚠ `.ct` 的 `padding-top` / `padding-bottom` 绝对禁止——会把内容区压缩并产生上方空白。
> 若需要内容区内边距，在布局容器上加 `padding-top`，不在 `.ct` 上加。

---

## 🔒 .ct 内部布局容器的强制约束（新增）

> 问题根源：布局容器（如 `.layout-l` / `.layout-g` 等）在 `.ct` 内部使用 `height: 100%` + `padding-top` 时，
> 实际高度 = 580px + padding-top，导致内容溢出被摘要栏覆盖。

### 铁律 4：布局容器高度必须内包 padding

```css
/* ❌ 错误写法 —— padding-top 会撑高容器 */
.layout-x {
  height: 100%;      /* = 580px */
  padding-top: 8px;  /* 实际变成 588px → 溢出 */
}

/* ✅ 正确写法 —— padding 计入行高计算 */
.layout-x {
  height: calc(580px - 8px);  /* 主动减去 padding */
  padding-top: 8px;
  /* 或 */
  grid-template-rows: 8px 1fr;  /* 将 padding 作为第一行 */
}
```

### 铁律 5：Grid + Flex 混用时必须显式约束行高

```css
/* ❌ 错误写法 —— flex: 1 会按内容撑高 */
.left-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.card { flex: 1; }  /* 三张卡片总高 = 内容高度，可能 > 580px */

/* ✅ 正确写法 —— 显式指定行高或约束 */
.left-grid {
  display: grid;
  grid-template-rows: repeat(3, 176px);  /* (580 - gap×2) / 3 */
  gap: 8px;
}
/* 或 */
.card {
  flex: none;
  height: 176px;  /* 固定高度 */
  min-height: 0;  /* ← 关键：允许 flex 收缩 */
}
```

### 铁律 6：.ct 内所有直接子元素必须满足以下之一

```
□ 显式 height 值（非 100%）
□ grid-template-rows 显式定义每行高度
□ flex 子元素有 `min-height: 0` + 固定高度或 flex-basis
□ 通过空间计算验证：内容总高 ≤ 580px - padding - gaps
```

---

## 可用内容宽度

```
总宽 1017px − 左右 padding 25×2 = 967px 可用内容宽
```

---

## 字号上限（所有模板通用）

| 区域 | 最大字号 | 说明 |
|------|---------|------|
| 页面大标题（展示字体版） | 32–54px | 仅 部分TC风格使用 |
| 页眉主题文字 | 17px | 普通页眉 |
| 卡片标题 | 13px | |
| 正文 / 摘要 | 12px | |
| 图表标签 / 页脚 | 9–11px | |
| 大数字 KPI | 26–44px | 每页 ≤ 4 个 |

---

## 溢出检测规则

运行截图时，若 `scrollWidth > 1017` 或 `scrollHeight > 720`，输出 `⚠ 溢出` 警告。
常见原因与修复：

| 原因 | 修复 |
|------|------|
| `.ct` 有 `padding-top/bottom` | 删除，移至布局容器 |
| 子元素有 `min-height` 未约束 | 改为 `height: 100%` |
| 字号超过 13px 导致文字撑高 | 降低字号 |
| 网格 gap 过大 | gap ≤ 8px |
| 固定高度 + 内容过多 | 精简内容或减小字号 |

---

## 页脚进度条（通用片段）

```html
<div style="display:flex;align-items:center;gap:6px;">
  <div style="width:90px;height:3px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;">
    <div style="width:[N/M×100]%;height:100%;background:var(--p);border-radius:2px;"></div>
  </div>
  <span style="font-size:10px;color:var(--dt);">[N]/[M]</span>
</div>
```
