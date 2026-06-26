# 编辑分割（Editorial Split）

**气质：** 杂志感、强叙事、视觉冲击、对比强烈
**适用：** 案例分析、防御方案、风险评估、攻击原理
**推荐字体：** FP-2（Playfair Display + Source Sans 3）或 FP-5（Bebas Neue + Barlow）
**背景类型：** 左暗右亮双区（不适用暗色/亮色统一背景约束）
**主标题字号：** 44–54px，位于左栏
**页眉形式：** 无横向页眉，标题融入左栏；右栏顶部用小号路径标注

---

## 布局规则

不使用 A/B/C/D 标准布局，Lc 固定结构：

```
左栏 280–330px（暗色）| 斜切色带 24–32px | 右栏（余量，亮色）
```

- 左栏：eyebrow + 超大主标题 + 3–4 个统计项 + 标签组，通栏垂直排列
- 右栏：2×2 或 1×3 内容卡片 + 底部摘要条

---

## CSS 片段

```css
/* 分割背景三层 */
.bg-dark { position:absolute; top:0; left:0; width:1017px; height:720px; background: #111827; }
.bg-light {
  position:absolute; top:0; right:0; width:650px; height:720px;
  background: #f8f7f3;
  clip-path: polygon(60px 0, 100% 0, 100% 100%, 0 100%);
}
.accent-stripe {
  position:absolute; top:0; left:322px; width:28px; height:720px;
  background: linear-gradient(180deg, COLOR_TOP, COLOR_BOTTOM);
  clip-path: polygon(0 0, 100% 0, calc(100% - 28px) 100%, 0 100%);
}

/* 左栏超大标题 */
.big-title { font-size: 48px; font-weight: 900; line-height: 0.92; letter-spacing: -2px; color: #f9fafb; }

/* 左栏统计项 */
.ls-item { border-left: 2px solid ACCENT; padding: 3px 0 3px 14px; }
.ls-num  { font-size: 30px; font-weight: 900; line-height: 1; letter-spacing: -1px; }

/* 右栏卡片（三选一混搭）*/
.card-light {
  background: #fff; border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,.06), 0 0 0 1px rgba(0,0,0,.04);
  padding: 12px 14px;
}
.card-dark   { background: #1e293b; border-radius: 6px; padding: 12px 14px; }
.card-accent { background: ACCENT;  border-radius: 6px; padding: 12px 14px; }

/* 标签 */
.tag-accent {
  display:inline-block; padding:2px 7px; border-radius:2px;
  font-size:9px; font-weight:700; letter-spacing:.3px;
  background: ACCENT; color: #fff;
}
```
